from moviepy.editor import *
from google.cloud import storage
import openai
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import datefinder
import datetime
import json
import pytube 

from pipelines import pipeline
from text2text.text_generator import TextGenerator
import nltk
from nltk.stem.porter import *
import spacy

import requests

from google.cloud import speech
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

def downloadYoutubeVideo(url):
    # where to save  
    savePath = "./" 
    try:  
        # object creation using YouTube which was imported in the beginning  
        yt = pytube.YouTube(url)  
    except:  
        print("Connection Error") # to handle exception  

    # filters out all the files with "mp4" extension  
    mp4files = yt.filter('mp4')  
    #to set the name of the file 
    yt.set_filename('sample')   
    # get the video with the extension and resolution passed in the get() function  
    d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)  
    try:  
        # downloading the video  
        d_video.download(savePath)  
    except:  
        print("Some Error!")  

    print('Task Completed!')


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=100000)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    transcript = ""
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        transcript += " " + result.alternatives[0].transcript
        print("Confidence: {}".format(result.alternatives[0].confidence))
    return transcript



def getDatesFromTranscript(text):
    spokenText = text.lower()

    today = datetime.datetime.now()
    if "tomorrow" in spokenText:
        date = today + datetime.timedelta(days=1)
        spokenText = spokenText.replace("tomorrow", date.strftime("%B %d"))
    if "today" in spokenText:
        date = today
        spokenText = spokenText.replace("today", date.strftime("%B %d"))
    if "yesterday" in spokenText:
        date = today + datetime.timedelta(days=-1)
        spokenText = spokenText.replace("yesterday", date.strftime("%B %d"))

    dates = datefinder.find_dates(spokenText)
    response = []
    for match in dates:
        if match >= today:
            response.append(match.isoformat())
    return list(dict.fromkeys(response))


def questionGeneration(text, num = 5):
    t2t_generator = TextGenerator(output_type="question")
    res = t2t_generator.predict([text] * num)
    ans = []
    que = []
    for r in res:
        if r[0] not in que:
            que.append(r[0])
            ans.append(r[1])
    return que, ans


# downloadYoutubeVideo("https://www.youtube.com/watch?v=6M5VXKLf4D4")

@app.route('/sendMoney', methods=['POST'])
def sendMoney():
    url = "https://api.sandbox.checkbook.io/v3/check/digital"
    arrivingRequest = json.loads(request.data.decode('utf-8'))

    payload = {
        "recipient": arrivingRequest.get('recipient'),
        "name": arrivingRequest.get('name'),
        "amount": float(arrivingRequest.get('amount')),
        "description": arrivingRequest.get('description')
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return response.text

@app.route('/getAudioAnalysis', methods=['POST'])
def getAudioAnalysis():
    arrivingRequest = json.loads(request.data.decode('utf-8'))
    print("Analysis request", arrivingRequest, "\n")
    videoPath = arrivingRequest.get('location')
    try:
        nameStartIndex = videoPath.rindex("/") + 1
    except:
        nameStartIndex = 0

    videoFileName = videoPath[nameStartIndex:]
    print("Fetching the video from ", videoPath, "\n")
    video = VideoFileClip(videoPath)
    audio = video.audio

    audioFileName = videoFileName.split(".")[0] + ".wav"

    audio.write_audiofile("./" + audioFileName) # 4.
    print("Extracted the audio from video and saving to ", audioFileName, "\n")

    sound = AudioSegment.from_wav("./" + audioFileName)
    sound = sound.set_channels(1)
    sound.export("./" + audioFileName, format="wav")
    print("Converted to one channel \n\n\n")

    upload_blob("audio-files-zoom", "./" + audioFileName, audioFileName)
    print("Uploaded to Google Cloud Storage", "\n\n\n")

    transcript = transcribe_gcs("gs://audio-files-zoom/" + audioFileName)
    print("Finished extracting the transcript from uploaded audio file", "\n")

    # transcript = "We are going to be talking about the Great Financial Crisis of 2008. This crisis occurerd when banks were suddenly out of money to hold liquidity reserves to pay new potential customers. This happened when they lent money to a lot of people who could not pay back their loans. This resulted in a loss of livelihood for a lot of people and resulted in the entire US economy going down. That's all for today. Please remember your assignments are due tomorrow and the final examination will be held on March 14th. Please also do remember to submit payment for the school trip. Thank you." 
    print(transcript)

    response = {"transcript": transcript}

    if arrivingRequest.get('summarize'):
        tldrPrompt = transcript + "\nIn summary, "
        completion = openai.Completion.create(
            engine="davinci", prompt=tldrPrompt, temperature=0.1, max_tokens=60,
            top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0 )
        print("Summary Generated", completion, "\n\n")
        response["summarize"] = completion["choices"][0]["text"]


    if arrivingRequest.get('simplify'):
        simplifyPrompt = "My second grader asked me what this passage means:\n\"\"\"\n" + \
                        transcript + \
                        "\n\"\"\"\nI rephrased it for him, in plain language a second grader can understand:\n\"\"\"\n",
        completion = openai.Completion.create(
            engine="davinci", prompt=simplifyPrompt, temperature=0, max_tokens=60,
            top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=["\"\"\""] )
        
        print("Simplification Generated", completion, "\n\n")
        response["simplify"] = completion["choices"][0]["text"]

    if arrivingRequest.get('dates'):
        dates = getDatesFromTranscript(transcript)
        print("Dates Generated ", dates, "\n\n")
        response["dates"] = dates

    if arrivingRequest.get('qna'):
        questions, answers = questionGeneration(transcript, num=5)
        print("Questions Generated ", questions, answers, "\n\n")
        response["qna"] = {"questions": questions, "answers": answers}
    
    if arrivingRequest.get('shrek') and "fauci" in arrivingRequest.get('location'):
        response["videoLink"] = "https://storage.googleapis.com/audio-files-zoom/fauciShrekGeneratedWithAudio.mp4"
    elif arrivingRequest.get('rapunzel') and "jairam" in arrivingRequest.get('location'):
        response["videoLink"] = "https://storage.googleapis.com/audio-files-zoom/jairamGeneratedWithAudio.mp4"
    elif arrivingRequest.get('moana') and "deepLecture" in arrivingRequest.get('location'):
        response["videoLink"] = "https://storage.googleapis.com/audio-files-zoom/deepLectureGeneratedWithAudio.mp4"
    else:
        response["videoLink"] = "https://storage.googleapis.com/audio-files-zoom/fauciShrekGeneratedWithAudio.mp4"

    # response = {"videoLink": "https://storage.googleapis.com/audio-files-zoom/fauciShrekGeneratedWithAudio.mp4", \
    #             "transcript": " Depending has become very prevalent and finds applications Divine ratio of areas such as speech \
    #             computer vision natural language processing like most of the state-of-the-art systems in these areas from even now \
    #             companies like Google Facebook, excetra use deep learning as the underlying solution to end. This course will learn some \
    #             of the foundational all the phone number to the block off deep learning in particular mean start right from the basics \
    #             and start on perception or a sigmoid new single neuron and Sunday. We try to go to multi-layer network of neurons are \
    #             multi-layer perceptron as it is commonly known so and you look at other things for training sets networks and their \
    #             specific backpropagation, which uses gradient descent. I didn't even look at several applications of feed-forward neural \
    #             networks Lake autoencoders and were two against one. Then we move on to the next type of neural networks, which is \
    #             recurrent neural networks, which find applications in areas where you have to deal with sequences. So sequences that \
    #             again omnipresent you have sequences in natural language text when you talk of a sentence you can think of it as a \
    #             sequence of words inside words themselves. You can think of them as sequence of characters.", "summarize": \
    #             "\u0e2d\u0e22\u0e32\u0e01\u0e40\u0e23\u0e35\u0e22\u0e19 Deep Learning \
    #             \u0e01\u0e47\u0e40\u0e25\u0e22\u0e2d\u0e22\u0e32\u0e01\u0e40\u0e23\u0e35\u0e22\u0e19\u0e01\u0e31\u0e1a Andrew Ng \
    #             \u0e17", "simplify": "The brain is made up of billions of neurons. Each neuron is connected to many other neurons. The \
    #             connections between neurons are called synapses. The connections between neurons are like a network. The brain is like a \
    #             computer. The brain is like a network of computers.\nThe brain is like a network", "dates": ["2021-02-14T00:00:00", "2021-03-15T00:00:00"], \
    #             "qna": {"questions": ["Recurrent neural networks find applications in what areas?", "What does a course begin with a \
    #             sigmoid new single neuron?", "Neural networks find applications in what?", "What kind of backpropagation does gradient \
    #             descent use?"], "answers": ["areas", "start", "language", "specific"]}}
    
    # response = jsonify(message=response)
    # response.headers.add("Access-Allow-Control-Origin", "*")
    return response

@app.route('/getTextCompletion', methods=['POST'])
def getTextCompletion():
    arrivingRequest = json.loads(request.data.decode('utf-8'))
    completion = openai.Completion.create(
    engine="davinci", prompt=arrivingRequest.get('text'), temperature=0, max_tokens=10,
    top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=["\"\"\""] )
    return completion

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
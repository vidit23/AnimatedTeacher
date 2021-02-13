from moviepy.editor import *
from google.cloud import storage
import openai
from flask import Flask
from flask import request
import datefinder
import datetime
import json
import pytube 

from pipelines import pipeline
from text2text.text_generator import TextGenerator
import nltk
from nltk.stem.porter import *
import spacy

from google.cloud import speech
from pydub import AudioSegment

app = Flask(__name__)


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



def getDates(text):
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
        response.append(match.isoformat())
    return response


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

# # text = "for this introduction to the coasts on deep learning which will be offered to rain. So are they planning has become very prevalent and it is finds application to Divine ratio of areas such as speech computer vision natural language processing like most of the state-of-the-art systems in these areas from companies hey Google Facebook excetra use deep learning as the underlying Solution on some of the foundational all the phone number to the blocks of deep learning in particular start right from the basics and starts on perception or a sigmoid new single neuron and Sunday we try to go to multi-layer network of neurons and multi-layer perceptron as it is commonly known so and you look at other things for training sets networks and their specific backpropagation which uses gradient descent and then look at several applications. tl;dr: "
# datePrompt = "\n Tomorrow is"

# print(questionGeneration(text, n=5))
# # print(openai.Engine.list())


# print(openai.Completion.create(
#   engine="davinci",
#   prompt=text + datePrompt,
#   temperature=0.4,
#   max_tokens=20
# ))

@app.route('/getAudioAnalysis', methods=['GET'])
def getAudioAnalysis():
    videoPath = request.args.get('location')
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

    # transcript = "Depending has become very prevalent and finds applications Divine ratio of areas such as speech computer vision natural \
    #             language processing like most of the state-of-the-art systems in these areas from even now companies like Google \
    #             Facebook, excetra use deep learning as the underlying solution and the schools will learn some of the foundational all \
    #             the phone number to the block off deep learning in particular mean start right from the basics and start on Pacific or a \
    #             sigmoid new single neuron and Sunday. We try to go to multi-layer network of neurons are multi-layer perceptron as it is \
    #             commonly known so and you look at other things for training sets networks and their specific backpropagation, which uses \
    #             gradient descent. I didn't even look at several applications of feed-forward neural networks Lake autoencoders and were \
    #             two against one. Then we move on to the next type of neural networks, which is recurrent neural networks, which find \
    #             applications in areas where you have to deal with sequences. So sequences that again omnipresent you have sequences in \
    #             natural language text when you talk of a sentence you can think of it as a sequence of words inside words themselves. \
    #             You can think of them as sequence of characters."

    # if 

    return transcript




# print(openai.Completion.create(
#     engine="davinci",
#     prompt="hi, my name is",
#     max_tokens=16
# ))

if __name__ == '__main__':
    app.run()
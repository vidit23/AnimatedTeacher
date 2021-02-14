# Animated Teacher

## Inspiration
Attending college classes online, we found ourselves easily distracted as well as missing quite a few important details and deadlines mentioned in class. We can only imagine this effect is compounded in children attending school from home. We read various studies like [Animating Student Engagement](https://journal.alt.ac.uk/index.php/rlt/article/view/2124/2514) which show that using animations increases student engagement and retention of complex concepts. However, creating animations is time-consuming and expensive. Thus, we decided to tackle this problem using the wide variety of class sessions available online and recent advances in Deep Learning. We also wanted to make it easier for parents to monitor the requirements for their children's classes by extracting deadlines and payment requests mentioned in class.

Despite having the potential to change the education industry, we also believe that we can use this solution to bring about engagement from a younger audience in pressing issues. We can create videos of cartoon characters advocating for vaccines and sustainability. Our idea can be used to simplify complex concepts being taught in videos online. We also believe that this project can help students with hearing disabilities, ADHD, etc who have trouble listening to class. This can also go a long way towards helping students with low internet speeds in rural areas as most processing happens in the background with the output only text and a lesser aspect ratio video.

This project also gave us some hilarious results. With Shrek (in an old man voice) talking about diseases and vaccines and Ben 10 teaching us Deep Learning. [Found Here](https://youtu.be/4dyjVuCZKCk) 

## How to Run
```
conda create --name animated
conda activate animated
pip install -r requirements.txt
python server.py
```

```
cd frontend
npm -i
npm start
```

## What it does
Our solution takes as input the recorded classroom link and returns after processing 
1. A video of the teacher but replaced with the child's favorite cartoon character. 
2. A summary of the class so it is easy to access the parts of the class that the child wants to revisit.
3. A simplified version of what was covered in class for quick and easy consumption and understanding.
4. A list of deadlines mentioned in class so students never miss an assignment or homework.
5. A list of five questions/answers for the students to quiz themselves using the information discussed in class
6. An option for tracking payment requirements mentioned in class and paying using Checkbook.

## How we built it
We first take the classroom recording and using face tracking, cut out a 256x256 section of the video (this is the most resource-intensive part of this application). The video and audio channels are then separated into different pipelines as shown below. The video and the cartoon's image are fed into the model described in [First Order Motion Model for Image Animation](https://papers.nips.cc/paper/2019/file/31c0b36aef265d9221af80872ceb62f9-Paper.pdf) to get the generated video. The audio is converted into a transcript using the [Google APIs](https://cloud.google.com/speech-to-text). The text is then analyzed using OpenAI APIs to generate the summary and the simplification of the entire class. We use the text2text generator to design questions based on what was taught in class. We also analyze for payment request mentioned in the recording to make it easy for parents to pay. Moreover, we designed a custom deadline extractor to identify important dates mentioned in the recording. All of this is shown in the web interface.

## Challenges we ran into
1. Setting up the environment for the First Order model and text2text generator with outdated requirements and running it without a GPU.
2. Setting up the pipeline and utilizing the APIs.
3. Converting the video to a 256x256 aspect ratio with a key object in the middle.

## Accomplishments that we're proud of
1. Managing our own deadlines while building the application. 
2. Utilizing various models to come up with a comprehensive product.
3. This was the first time using React and Google Cloud for both of us as well as building the front end.
4. We finally got to use the models we learned about in class

## What we learned
1. It was eye-opening to see the capabilities of the OpenAI API and using text manipulation for summary and simplification generation. 
2. Building a parallel application in Python.
3. Time management and focusing on key features.

## What's next for Animated Teachers
We would like to optimize the pipeline so that it can run in realtime as well as convert the voice of the teacher into a specific character for a more immersive experience. We would also like to index all the data generated so users can search to find classes on concepts they are specifically looking for.

# Animated Teacher

## Inspiration
Attending college classes online, we found ourselves easily distracted as well as missing quite a few important details and deadlines mentioned in class. We can only imagine this effect is compounded in children attending school from home. We read various studies like [Animating Student Engagement](https://journal.alt.ac.uk/index.php/rlt/article/view/2124/2514) which show that using animations increases student engagement and retention of complex concepts. However, creating animations is time-consuming and expensive. Thus, we decided to tackle this problem using the wide variety of class sessions available online and recent advances in Deep Learning.

## What it does
Our solution takes as input the recorded classroom link and returns after processing 
1. A video of the teacher but replaced with the child's favorite cartoon character. 
2. A summary of the class so it is easy to access the parts of the class that the child wants to revisit.
3. A simplified version of what was covered in class for quick and easy consumption and understanding.
4. A list of deadlines mentioned in class so students never miss an assignment or a homework.
5. A list of five questions/answers for the students to quiz themselves using the information discussed in class

## How we built it
We first take the classroom recording and using face tracking, cut out a 256x256 section of the video (this is the most resource-intensive part of this application). The video and audio channels are then separated into different pipelines as shown below. The video and the cartoon's image are fed into the model described in [First Order Motion Model for Image Animation](https://papers.nips.cc/paper/2019/file/31c0b36aef265d9221af80872ceb62f9-Paper.pdf) to get the generated video. The audio is converted into a transcript using the [Google APIs](https://cloud.google.com/speech-to-text). The text is then analyzed using OpenAI APIs to generate the summary and the simplification of the entire class. We use the text2text generator to design questions based on what was taught in class. Moreover, we designed a custom deadline extractor to identify important dates mentioned in the recording. All of this is shown in the web interface.

## Challenges we ran into
1. Setting up the environment for the Deep learning with outdated requirements
2. Setting up the pipeline and utilizing the APIs
3. Converting the video to a 256x256 aspect ratio with keyframes

## Accomplishments that we're proud of
Managing our own deadlines while building the application. 
Utilizing various models to come up with a comprehensive product.

## What we learned

## What's next for Animated Teachers
We would like to optimize the pipeline so that it can run in realtime as well as convert the voice of the teacher into a specific character for a more immersive experience. 

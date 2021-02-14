from moviepy.editor import *

name = "jairam"

videoclip = VideoFileClip(name + "Generated.mp4")
audioclip = VideoFileClip(name + ".mp4")

# new_audioclip = CompositeAudioClip([audioclip])
videoclip.audio = audioclip.audio
videoclip.write_videofile(name + "GeneratedWithAudio.mp4")
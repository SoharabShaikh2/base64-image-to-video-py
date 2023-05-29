import base64

import imageio
import moviepy.video.fx.all as vfx
import json

from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.io.AudioFileClip import AudioFileClip

from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip


# for i in data["wbw"]:
# print(i)

# print(jsonData)


def convertAyatToVideo(jsonData, name, surah, ayat):
    screensize = (980, 1860)
    clip = VideoFileClip("back.mp4", audio=False)
    mainAudio = AudioFileClip("back_mp3.mp3")

    # clip_resized = clip.fx(vfx.resize, width=1080, height=1920)

    audio = AudioFileClip(jsonData["mp3"])
    audio1 = audio.set_start(0)
    videoDuration = audio.duration + (len(jsonData["childs"]) * 6) + 1

    clip1 = vfx.loop(clip, duration=videoDuration)
    mainAudio1 = vfx.loop(mainAudio, duration=videoDuration)
    mainAudio1 = mainAudio1.fx(volumex, 0.4)

    '''margin_int = 800
    font_size = 70
    font_size_ar = 100
    if len(jsonData["wbw"]) > 8:
        margin_int = 1000
        font_size = 50
        font_size_ar = 70
    else:
        margin_int = 700
        font_size = 70
        font_size_ar = 100
'''
    clipArray = []
    audioArry = []
    clipArray.append(clip1)
    audioArry.append(mainAudio1)
    audioArry.append(audio1)

    mask_Clip = TextClip('Surah: ' + surah + ', Ayat: ' + ayat, fontsize=30, color='white')
    mask_Clip = mask_Clip.set_duration(videoDuration - 1).set_start(1)
    mask_Clip = mask_Clip.set_position((0.07, 0.95), relative=True).set_opacity(0.6)
    # mask_Clip = mask_Clip.fx(vfx.margin, bottom=10, opacity=0)
    clipArray.append(mask_Clip)

    imgdata1 = base64.b64decode(jsonData["arabic_img"])
    img1 = imageio.imread(imgdata1)

    txt_clip = ImageClip(img1).set_duration(audio.duration + 1).set_start(0)
    txt_clip_new = vfx.fadein(txt_clip, 1)
    txt_clip_new = vfx.fadeout(txt_clip, 0.5)
    clipArray.append(txt_clip_new)

    wordBword = jsonData["childs"]
    i = 0
    while i < len(wordBword):
        print(wordBword[i])
        time = 0
        if i == 0:
            time = audio.duration + 1
        else:
            time = audio.duration + (i * 6)

        child_imgdata1 = base64.b64decode(wordBword[i]["ar_img"])
        child_img1 = imageio.imread(child_imgdata1)
        child_clip1 = ImageClip(child_img1).set_duration(5).set_start(time)
        child_clip1_new = vfx.fadein(child_clip1, 1)
        child_clip1_new = vfx.fadeout(child_clip1, 0.5)
        clipArray.append(child_clip1_new)

        child_audio = AudioFileClip(wordBword[i]["mp3"])
        child_audio1 = child_audio.set_start(time)
        audioArry.append(child_audio1)

        i += 1

    audioMixed = CompositeAudioClip(audioArry)
    # Overlay the text clip on the first video clip
    video = CompositeVideoClip(clipArray)
    video = video.set_audio(audioMixed)
    # showing video
    video.write_videofile(name)


def makeVideo():
    surah = 1
    f = open("001.json", encoding="utf-8")
    data = json.load(f)
    # print(data)
    f.close()
    jsonData = data
    i = 0
    while i < 7:
        print(jsonData[i]["mp3"])
        name = '00' + str(surah) + '_00' + str(surah) + '00' + str(i + 1) + '.mp4'
        convertAyatToVideo(jsonData[i], name, str(surah), str(i + 1))
        i += 1


def loopFile():
    surah = 2
    i = 1
    while i < 1:
        url = '00' + str(surah) + '/' + 'Surah_00' + str(surah) + '00' + str(i) + '.json'
        name = '00' + str(surah) + '_00' + str(surah) + '00' + str(i) + '.mp4'
        makeVideo()
        i += 1


makeVideo()

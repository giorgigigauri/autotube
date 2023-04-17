from moviepy.editor import *
import random
import os
from gtts import gTTS
import mutagen
from mutagen.mp3 import MP3
from datetime import date
import time
import calendar

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def GetDaySuffix(day):
    if day == 1 or day == 21 or day == 31:
        return "st"
    elif day == 2 or day == 22:
        return "nd"
    elif day == 3 or day == 23:
        return "rd"
    else:
        return "th"

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
music_path = os.path.join(dir_path, "Music/")

def add_return_comment(comment):
    need_return = 30
    new_comment = ""
    return_added = 0
    return_added += comment.count('\n')
    for i, letter in enumerate(comment):
        if i > need_return and letter == " ":
            letter = "\n"
            need_return += 30
            return_added += 1
        new_comment += letter
    return new_comment, return_added
def getUniqId():
    current_GMT = time.gmtime()

    time_stamp = calendar.timegm(current_GMT)
    return str(time_stamp)

class CreateMovie():

    @classmethod
    def CreateVideoAudio(self, text, start = 0):

        audioPath = "audio/"+getUniqId()+"tts.mp3"
        tts = gTTS(text=text, lang='en', tld='com.au', slow=False)
        tts.save(audioPath)
        audio = MP3(audioPath)
        ## could use some fancying up but works ^

        music_file = audio
        music = AudioFileClip(audioPath)
        music = music.set_start(start,int(audio.info.length))
        music = music.volumex(1)
        music = music.set_duration(int(audio.info.length))
        return music

    @classmethod
    def CreateVideoText(cls, text, xPos, yPos, start, duration):
        txt = TextClip(text, font='Courier',
                       fontsize=40, color='#FFF',  bg_color='#00FF00')
        txt = txt.on_color(col_opacity=.3)
        txt = txt.set_position((xPos, yPos))

        txt = txt.set_start(0,start)  # (min, s)
        txt = txt.set_duration(duration)
        txt = txt.crossfadein(0.95)
        txt = txt.crossfadeout(0.95)
        return txt


    @classmethod
    def CreateMP4(cls, post_data):
        text = post_data['Best_comment']


        clip = VideoFileClip('minecraft.mp4').subclip(0,20)
        textClip =  cls.CreateVideoText(text, 10, 50, 0,20)
        textAudio = cls.CreateVideoAudio(text, 0)
        clip = clip.set_audio(textAudio)
        clip = CompositeVideoClip([clip, textClip])
        clip.write_videofile(getUniqId() + "output.mp4", fps=24)
        return 'Done'

        colors = ['PeachPuff3', 'OrangeRed3', 'silver', 'yellow', 'LightGreen', 'LightSkyBlue', 'LightPink4', 'SkyBlue2', 'MintCream','LimeGreen', 'WhiteSmoke', 'HotPink4']
        random.shuffle(colors)
        text_clips = []
        notification_sounds = []

        return_comment, return_count = add_return_comment(post['Best_comment'])
        text1 = return_comment
        addText1 = cls.AddText(text1)

        return_comment, _ = add_return_comment(post['best_reply'])
        text2 = return_comment
        txt = TextClip(return_comment, font='Courier',
        fontsize=38, color=colors.pop(), bg_color='#005BBB')
        txt = txt.on_color(col_opacity=.3)
        txt = txt.set_position((15,135 + (return_count * 50)))
        txt = txt.set_start((0, 5 + (i * 12))) # (min, s)
        txt = txt.set_duration(7)
        txt = txt.crossfadein(0.9)
        txt = txt.crossfadeout(0.9)
        text_clips.append(txt)

        text1_audio = gTTS(text=text1, lang='en', tld='com.au', slow=False)
        text1_audio.save("Music/notification1.mp3")

        text2_audio = gTTS(text=text2, lang='en', tld='ie', slow=False)
        text2_audio.save("Music/notification2.mp3")


        text1_audio_length = MP3("Music/notification1.mp3")
        text1_audio_length = int(text1_audio_length.info.length)

        text2_audio_length = MP3("Music/notification1.mp3")
        text2_audio_length = int(text2_audio_length.info.length)

        notification = AudioFileClip(os.path.join(music_path, f"notification1.mp3"))
        notification = notification.set_start((0, 0 + (i * 12)))
        notification_sounds.append(notification)
        notification = AudioFileClip(os.path.join(music_path, f"notification2.mp3"))
        notification = notification.set_start((0, (text1_audio_length + 3) + (i * 12)))
        notification_sounds.append(notification)

        music_file = os.path.join(music_path, f"music5.mp3")
        music = AudioFileClip(music_file)
        music = music.set_start((0,0))
        music = music.volumex(.1)
        music = music.set_duration(59)

        new_audioclip = CompositeAudioClip([music]+notification_sounds)
        clip.write_videofile(f"video_clips.mp4", fps = 24)

        clip = VideoFileClip("video_clips.mp4",audio=False)
        # clip = CompositeVideoClip([clip] + text_clips)
        clip = CompositeVideoClip([clip])
        clip.audio = new_audioclip
        clip.write_videofile("video.mp4", fps = 24)


        if os.path.exists(os.path.join(dir_path, "video_clips.mp4")):
            os.remove(os.path.join(dir_path, "video_clips.mp4"))
        else:
            print(os.path.join(dir_path, "video_clips.mp4"))

if __name__ == '__main__':
    print(TextClip.list('color'))
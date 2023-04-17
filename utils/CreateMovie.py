from moviepy.editor import *
import random
import os
from gtts import gTTS
import mutagen
from mutagen.mp3 import MP3
from datetime import date
import time
import calendar
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, ImageClip, TextClip
import textwrap

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def create_rectangle(width, height, color, position):
    return ColorClip(size=(width, height), color=color).set_position(position)


def wrap_text(text, max_width, font, fontsize):
    wrapper = textwrap.TextWrapper(width=max_width)
    wrapped_text = wrapper.fill(text=text)
    return TextClip(wrapped_text, font=font, fontsize=fontsize, color="black")


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
    def CreateVideoAudio(self, text, start=0):
        audioPath = "audio/" + getUniqId() + "tts.mp3"
        tts = gTTS(text=text, lang='en', tld='com.au', slow=False)
        tts.save(audioPath)
        audio = MP3(audioPath)
        ## could use some fancying up but works ^

        music_file = audio
        music = AudioFileClip(audioPath)
        music = music.set_start(start, int(audio.info.length))
        music = music.volumex(1)
        music = music.set_duration(int(audio.info.length))
        return music

    @classmethod
    def CreateVideoText(cls, text, xPos, yPos, start, duration):
        txt = TextClip(text, font='Courier',
                       fontsize=40, color='#FFF', bg_color='#00FF00')
        txt = txt.on_color(col_opacity=.3)
        txt = txt.set_position((xPos, yPos))

        txt = txt.set_start(0, start)  # (min, s)
        txt = txt.set_duration(duration)
        txt = txt.crossfadein(0.95)
        txt = txt.crossfadeout(0.95)
        return txt

    @classmethod
    def CreateMP4(cls, post_data):
        text = post_data['title']

        clip = VideoFileClip('minecraft.mp4').subclip(0, 20)
        clip = cls.AddVideoTitleText(clip, 'reddit-logo.png', text)
        #todo::
        # cls.addSubTextsVideo([texts])
        textAudio = cls.CreateVideoAudio(text, 0)
        clip = clip.set_audio(textAudio)
        clip.write_videofile(getUniqId() + "output.mp4", fps=24)
        return 'Done'

    @classmethod
    def AddVideoTitleText(cls, video, logo, text):
        video_width, video_height = video.size
        logo = ImageClip(logo).resize(height=30, width=30)
        padding = 20

        max_text_width = 60
        title = wrap_text(text, max_text_width, font="Arial", fontsize=12)

        title_width, title_height = title.size

        rectangle_width, rectangle_height = title_width + (padding*2) + logo.size[0], title_height + (padding*2)
        title_x, title_y = (video_width - rectangle_width) / 2, (video_height - rectangle_height) / 2
        rectangle_position = (title_x - padding, title_y - padding)
        rect_x, rect_y = rectangle_position
        rectangle = create_rectangle(width=rectangle_width, height=rectangle_height, color=(240, 240, 240, 4),
                                     position=rectangle_position, )

        logo_x = title_x - 40
        logo_y = title_y + (title_height - logo.size[1]) / 2

        logo_clip = logo.set_duration(video.duration).set_position((logo_x, logo_y))
        title_clip = title.set_duration(video.duration).set_position((title_x, title_y))
        rectangle_clip = rectangle.set_duration(video.duration).set_position((rect_x, rect_y))

        return CompositeVideoClip([video, rectangle_clip, logo_clip, title_clip],
                                  use_bgclip=True)

    # def AddVideoSubtitleText(self):
    #
    # def GetVideoBackgroundVideo(self):


if __name__ == '__main__':
    print(TextClip.list('color'))

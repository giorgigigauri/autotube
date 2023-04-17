from moviepy.editor import *
import random
import os
from gtts import gTTS
import mutagen
from mutagen.mp3 import MP3

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
        

class CreateMovie():

    @classmethod
    def CreateMP4(cls, post_data):

        clips = []
        for post in post_data:
            if "gif" not in post['image_path']:
                clip = ImageSequenceClip([post['image_path']], durations=[12])
                clips.append(clip)
            else:
                clip = VideoFileClip(post['image_path'])
                clip_lengthener = [clip] * 60
                clip = concatenate_videoclips(clip_lengthener)
                clip = clip.subclip(0,12)
                clips.append(clip)
        
        # After we have out clip.
        clip = concatenate_videoclips(clips)

        # Hack to fix getting extra frame errors??
        clip = clip.subclip(0,60)

        colors = ['yellow', 'LightGreen', 'LightSkyBlue', 'LightPink4', 'SkyBlue2', 'MintCream','LimeGreen', 'WhiteSmoke', 'HotPink4']
        colors = colors + ['PeachPuff3', 'OrangeRed3', 'silver']
        random.shuffle(colors)
        text_clips = []
        notification_sounds = []
        for i, post in enumerate(post_data):
            return_comment, return_count = add_return_comment(post['Best_comment'])
            text1 = return_comment
            txt = TextClip(return_comment, font='Courier',
                        fontsize=40, color=colors.pop(), bg_color='#005BBB')
            txt = txt.on_color(col_opacity=.3)
            txt = txt.set_position((5,50))
            txt = txt.set_start((0, 3 + (i * 12))) # (min, s)
            txt = txt.set_duration(7)
            txt = txt.crossfadein(0.9)
            txt = txt.crossfadeout(0.9)
            text_clips.append(txt)
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
        #clip = CompositeVideoClip([clip] + text_clips)
        clip = CompositeVideoClip([clip])
        clip.audio = new_audioclip
        clip.write_videofile("video.mp4", fps = 24)

        
        if os.path.exists(os.path.join(dir_path, "video_clips.mp4")):
            os.remove(os.path.join(dir_path, "video_clips.mp4"))
        else:
            print(os.path.join(dir_path, "video_clips.mp4"))

if __name__ == '__main__':
    print(TextClip.list('color'))
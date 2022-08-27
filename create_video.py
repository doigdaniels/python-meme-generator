from moviepy.editor import *
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO
from time import sleep
import create_img
import random


def gen_video():
    thumbnail, uncannyness = create_img.generate()
    duration = random.randrange(20, 30)
    clip = ImageClip(thumbnail, duration=duration)
    clip = clip.set_audio(AudioFileClip(
        f"audio/{uncannyness}.mp3").set_duration(duration))
    return clip


def gen_compl_video():
    def gen_clip(i):
        thumbnail = create_img.generate(uncannyness=i)[0]
        duration = random.randrange(7, 15)
        clip = ImageClip(thumbnail, duration=duration)
        clip = clip.set_audio(AudioFileClip(
            f"audio/{i}.mp3").set_duration(duration))
        sleep(0.3)
        return clip

    clips = [gen_clip(i) for i in range(7)]
    return concatenate_videoclips(clips)


if __name__ == "__main__":
    # video = gen_video()
    video = gen_compl_video()
    video.write_videofile("output.mp4", threads=4, fps=24)
    video.close()

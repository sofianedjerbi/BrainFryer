import logging
import os
import random
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, vfx

logger = logging.getLogger(__name__)

class BackgroundAgent:
    def __init__(self, image_path, audio_path):
        self.image_path = image_path
        self.audio_path = audio_path
    
    def generate(self, duration, url, music_url):
        logger.debug(f"Getting from \"{url}\"")
        final_video_path = f"{self.image_path}/background.mp4"
        yt = YouTube(url)

        stream = yt.streams.get_highest_resolution()
        stream.download()

        downloaded_file_path = stream.default_filename
        clip = VideoFileClip(downloaded_file_path)
        clip = clip.fx(vfx.speedx, 1.3)

        max_start = clip.duration - duration
        random_start = random.uniform(0, max_start)

        w, h = clip.size
        new_height = h - (h % 2)
        new_width = int(h * 9 / 16)  # 16:9 aspect ratio
        new_width -= new_width % 2 
        crop_x_center = w / 2
        clip_cropped = clip.crop(x_center=crop_x_center, width=new_width, height=new_height)
        clip_cropped = clip_cropped.without_audio()
        clip_final = clip_cropped.subclip(random_start, random_start + duration) 
        clip_final.write_videofile(
            final_video_path,
            codec="libx264", 
            audio_codec="aac",
            ffmpeg_params=["-profile:v", "baseline", "-pix_fmt", "yuv420p"],
            fps=30,
            verbose=False
        )
        clip.close()
        os.remove(downloaded_file_path)

        download_path = f"{self.audio_path}/background.mp4"
        yt = YouTube(music_url)
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(filename=download_path)
        video_clip = AudioFileClip(out_file)
        final_file = out_file.replace(".mp4", ".mp3")
        video_clip.write_audiofile(final_file, verbose=False)
        video_clip.close()
        os.remove(out_file)

        logger.debug(f"Downloaded and converted to MP3: {final_file}")

import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip, ImageClip, concatenate_videoclips

class Combiner:
    def __init__(self, audio_dir, images_dir, output_file):
        self.audio_dir = audio_dir
        self.images_dir = images_dir
        self.output_file = output_file

    def process_files_reddit(self):
        background_clip = VideoFileClip(f"{self.images_dir}/background.mp4")
        background_music = AudioFileClip(f"{self.audio_dir}/background.mp3").volumex(0.04)
        
        audio_files = sorted([f for f in os.listdir(self.audio_dir) if f.endswith('.mp3') and f.replace('.mp3', '').isdigit()])

        final_clips = []
        current_time = 0

        for i, _ in enumerate(audio_files):
            audio_clip = AudioFileClip(f'{self.audio_dir}/{i}.mp3').volumex(1.25)

            image_path = f'{self.images_dir}/reddit_{i}.png'
            img_clip = ImageClip(image_path).set_duration(audio_clip.duration)
            
            new_width = background_clip.size[0] * 0.85
            aspect_ratio = img_clip.size[1] / img_clip.size[0]
            new_height = new_width * aspect_ratio
            img_clip = img_clip.resize(width=new_width, height=new_height)
            img_clip = img_clip.set_pos('center')
            
            img_clip = img_clip.set_audio(audio_clip)

            clips = [
                background_clip.subclip(current_time, current_time + audio_clip.duration),
                img_clip.set_position("center"),
            ]

            pic_path = f'{self.images_dir}/illustration_{i}.png'
            if os.path.exists(pic_path):
                pic_clip = ImageClip(pic_path).set_duration(audio_clip.duration)
                
                new_width = background_clip.size[0] * 0.6
                aspect_ratio = pic_clip.size[1] / pic_clip.size[0]
                new_height = new_width * aspect_ratio
                pic_clip = pic_clip.resize(width=new_width, height=new_height)
                pic_clip = pic_clip.set_pos('center')

                # Adjusted to include the margin and position
                clips.append(pic_clip.margin(top=32, opacity=0).set_position(("center", "top")))

            composite_clip = CompositeVideoClip(
                clips,
                size=background_clip.size
            ).set_duration(audio_clip.duration).set_audio(audio_clip)

            final_clips.append(composite_clip)
            current_time += audio_clip.duration

        final_video = concatenate_videoclips(final_clips, method="compose", bg_color=None, padding=0)
        background_music = background_music.audio_loop(duration=final_video.duration)

        final_audio = CompositeAudioClip([final_video.audio, background_music])
        final_video = final_video.set_audio(final_audio)
        final_video.write_videofile(
            self.output_file, 
            codec="libx264", 
            audio_codec="aac",
            ffmpeg_params=["-profile:v", "baseline", "-pix_fmt", "yuv420p"],
            fps=30
        )

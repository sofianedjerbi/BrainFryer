import os
from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, ColorClip

class SubtitleAgent:
    def __init__(self, output_file, model):
        self.output_file = output_file
        self.model = WhisperModel(model)
    
    def generate_subtitles(self):
        segments, _ = self.model.transcribe(self.output_file, word_timestamps=True)

        video = VideoFileClip(self.output_file)
        height = video.size[1] // 4
        font_size = video.size[1] // 26
        clips = [video]

        for segment in segments:
            for word in segment.words:
                start_time, end_time = word.start, word.end
                text = word.word.strip()

                txt_clip = (TextClip(
                                text,
                                fontsize=font_size,
                                color='white',
                                font='Arial-Bold'
                            )
                            .set_position(('center', 'bottom'))
                            .margin(bottom=height, opacity=0)
                            .set_duration(end_time - start_time)
                            .set_start(start_time))
                
                txt_width, txt_height = txt_clip.size
                
                bg_clip = (ColorClip(
                               size=(txt_width + 24, font_size + 10),  # Match the size with your text clip or the desired background size
                               color=(0, 0, 0, 128),  # RGBA (Black with 50% opacity), adjust the alpha value (0-255) for different opacities
                               duration=txt_clip.duration
                           )
                           .set_position(('center', 'bottom'))
                           .margin(bottom=height, opacity=0)
                           .set_start(start_time))

                clips.append(bg_clip)
                clips.append(txt_clip)

        final_clip = CompositeVideoClip(clips)

        dir_name, file_name = os.path.split(self.output_file)
        final_output = os.path.join(dir_name, "subtitled_" + file_name)
        final_clip.write_videofile(
            final_output,
            codec="libx264", 
            audio_codec="aac",
            ffmpeg_params=["-profile:v", "baseline", "-pix_fmt", "yuv420p"],
            fps=30,
            verbose=False
        )

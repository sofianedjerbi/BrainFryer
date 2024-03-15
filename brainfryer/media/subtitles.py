import re
from faster_whisper import WhisperModel


class SubtitleAgent:
    def __init__(self, output_file, model):
        self.output_file = output_file
        self.model = WhisperModel(model)
    
    def generate_subtitles(self):
        segments, info = self.model.transcribe(self.output_file, word_timestamps=True)

        video = VideoFileClip(self.output_file)
        clips = [video]  # Start with the original video clip

        # Iterate through each segment to overlay the subtitles
        for segment in segments:
            start_time, end_time = segment['start'], segment['end']  # Assuming these keys exist in your segments
            text = segment['text']  # Assuming this key exists for the transcribed text
            # Create a text clip for each segment
            txt_clip = (TextClip(text, fontsize=24, color='white', font='Arial-Bold')
                        .set_position(('center', 'bottom'))
                        .margin(bottom=32, opacity=0)
                        .set_duration(end_time - start_time)
                        .set_start(start_time))
            clips.append(txt_clip)

        # Overlay the text clips on the original video clip
        final_clip = CompositeVideoClip(clips)

        # Write the result to a file
        final_output = "subtitled_" + self.output_file
        final_clip.write_videofile(
            final_output,
            codec="libx264", 
            audio_codec="aac",
            ffmpeg_params=["-profile:v", "baseline", "-pix_fmt", "yuv420p"],
            fps=30
        )

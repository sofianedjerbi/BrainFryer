import os
import random
import requests
from datetime import datetime
from tqdm import tqdm

from brainfryer.media.text import *
from brainfryer.media.image import *
from brainfryer.media.tts import *
from brainfryer.media.reddit import *
from brainfryer.media.combiner import *
from brainfryer.media.background import *

class VideoCreator:
    def __init__(self, key, image_model, text_model, tts_model):
        if not os.path.exists("generated"):
            os.makedirs(f"generated/")

        current_time = datetime.now()
        self.base_dir = "generated/" + current_time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
        self.image_dir = self.base_dir + "images/"
        self.audio_dir = self.base_dir + "audio/"
        os.makedirs(self.base_dir)
        os.makedirs(self.image_dir)
        os.makedirs(self.audio_dir)

        self.text_agent = TextAgent(key, text_model)
        self.image_agent = ImageAgent(key, image_model, self.text_agent)
        self.tts_agent = TTSAgent(key, tts_model)
        self.reddit_agent = RedditAgent(self.image_dir)
        self.background_agent = BackgroundAgent(self.image_dir, self.audio_dir)
        self.combiner = Combiner(self.audio_dir, self.image_dir, self.base_dir + "output.mp4")

    def parse_reddit_comments(self, reddit_url):
        print("Parsing Reddit post...")
        title, comments = self.reddit_agent.parse_reddit_post(reddit_url)
        print(f"Reddit post parsed: {len(comments)} comments parsed")
        return title, comments

    def generate_tts(self, title, comments):
        print("Generating TTS...")
        self.tts_agent.generate_and_save("alloy", f"{title}?", self.audio_dir + "0.mp3")
        i = 1
        for text in tqdm(comments, desc="Generating TTS files"):
            voice = random.choice(["echo", "fable", "onyx", "nova", "shimmer"])
            self.tts_agent.generate_and_save(voice, text, self.audio_dir + f"{i}.mp3")
            i += 1
        print("TTS generated!")

    def generate_illustrations(self, title, comments):
        print("Generating illustrations...")
        helper = "create a very short dall-e 3 prompt to illustrate the following sentence,\
                  focus on key elements only, text on image is forbidden. Pay attention to content policy (kissing ...) (prompt content only, no json): "
        
        url = self.image_agent.generate(self.text_agent.send_message(helper + title))
        response = requests.get(url)
        with open(self.image_dir + "illustration_0.png", 'wb') as file:
            file.write(response.content)
        i = 1
        for text in tqdm(comments, desc="Generating illustrations"):
            url = self.image_agent.generate(self.text_agent.send_message(helper + text))
            response = requests.get(url)
            with open(self.image_dir + f"illustration_{i}.png", 'wb') as file:
                file.write(response.content)
            i += 1
        print("Illustrations generated!")

    def generate_background(self, background_url, background_music_url):
        print("Generating background...")
        mp3_files = [file for file in os.listdir(self.audio_dir) if file.endswith('.mp3')]

        total_duration = 0.0
        for mp3_file in mp3_files:
            file_path = os.path.join(self.audio_dir, mp3_file)
            audio_clip = AudioFileClip(file_path)
            total_duration += audio_clip.duration
            audio_clip.close()

        total_duration += 0.2 * (len(mp3_files) - 1)
        print("Downloading & formatting background...")
        self.background_agent.generate(total_duration, background_url, background_music_url)
        print("Background generated!")

    def render_video(self):
        print("Rendering...")
        self.combiner.process_files_reddit()
        print("Video rendered!")
        print(self.base_dir + "output.mp4")

    def generate_from_reddit_comments(self, reddit_url, background_url, background_music_url, create_images):
        title, comments = self.parse_reddit_comments(reddit_url)
        self.generate_tts(title, comments)
        if (create_images):
            self.generate_illustrations(title, comments)
        self.generate_background(background_url, background_music_url)
        self.render_video()

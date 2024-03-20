import logging
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
from brainfryer.media.subtitles import *

logger = logging.getLogger(__name__)

class VideoCreator:
    def __init__(
            self,
            key,
            image_model,
            text_model,
            tts_model,
            subtitles_model,
            dall_e,
            stable_diffusion_host,
            stable_diffusion_port
        ):
        if not os.path.exists("generated"):
            os.makedirs(f"generated/")

        current_time = datetime.now()
        self.base_dir = "generated/" + current_time.strftime("%Y-%m-%d_%H-%M-%S") + "/"
        self.image_dir = self.base_dir + "images/"
        self.audio_dir = self.base_dir + "audio/"
        self.output = self.base_dir + "output.mp4"
        os.makedirs(self.base_dir)
        os.makedirs(self.image_dir)
        os.makedirs(self.audio_dir)

        logger.info("Binding to APIs...")
        agent_nb = 7
        with tqdm(total=agent_nb, desc="Binding to APIs") as pbar:
            self.text_agent = TextAgent(key, text_model)
            pbar.update(1)
            if dall_e:
                self.image_agent = ImageAgentDallE(key, image_model, self.text_agent)
            else:
                self.image_agent = ImageAgentStableDiffusion(stable_diffusion_host, stable_diffusion_port)
            pbar.update(1)
            self.tts_agent = TTSAgent(key, tts_model)
            pbar.update(1)
            self.reddit_agent = RedditAgent(self.image_dir)
            pbar.update(1)
            self.background_agent = BackgroundAgent(self.image_dir, self.audio_dir)
            pbar.update(1)
            self.subtitle_agent = SubtitleAgent(self.output, subtitles_model)
            pbar.update(1)
            self.combiner = Combiner(self.audio_dir, self.image_dir, self.output)
            pbar.update(1)
        logger.info("Binded!")

    def parse_reddit_comments(self, reddit_url, max_comment_number):
        logger.info("Parsing Reddit post...")
        title, comments = self.reddit_agent.parse_reddit_post(reddit_url, max_comment_number)
        logger.info(f"Reddit post parsed: {len(comments)} comments parsed")
        return title, comments

    def generate_tts(self, title, comments):
        logger.info("Generating TTS...")
        self.tts_agent.generate_and_save("alloy", f"{title}?", self.audio_dir + "0.mp3")
        i = 1
        for text in tqdm(comments, desc="Generating TTS files"):
            voice = random.choice(["echo", "fable", "onyx", "nova", "shimmer"])
            self.tts_agent.generate_and_save(voice, text, self.audio_dir + f"{i}.mp3")
            i += 1
        logger.info("TTS generated!")

    def generate_illustrations(self, title, comments):
        logger.info("Generating illustrations...")
        helper = "create a very short dall-e 3 prompt to illustrate the following sentence, " \
            "focus on key elements only, text on image is forbidden. Make it follow dall-e content policy if needed. " \
            "(prompt content only, no json): "
        self.image_agent.generate(
            self.text_agent.send_message(helper + title),
            self.image_dir + "illustration_0.png"
        )
        i = 1
        for text in tqdm(comments, desc="Generating illustrations"):
            url = self.image_agent.generate(
                self.text_agent.send_message(helper + text),
                self.image_dir + f"illustration_{i}.png"
            )
            i += 1
        logger.info("Illustrations generated!")

    def generate_background(self, background_url, background_music_url):
        logger.info("Generating background...")
        mp3_files = [file for file in os.listdir(self.audio_dir) if file.endswith('.mp3')]

        total_duration = 0.0
        for mp3_file in mp3_files:
            file_path = os.path.join(self.audio_dir, mp3_file)
            audio_clip = AudioFileClip(file_path)
            total_duration += audio_clip.duration
            audio_clip.close()

        total_duration += 0.2 * (len(mp3_files) - 1)
        logger.debug("Downloading & formatting background...")
        self.background_agent.generate(total_duration, background_url, background_music_url)
        logger.info("Background generated!")

    def render_video(self):
        logger.info("Rendering...")
        self.combiner.process_files_reddit()
        logger.info(f"Video rendered at {self.output}!")

    def generate_subtitles(self):
        logger.info("Generating subtitles...")
        self.subtitle_agent.generate_subtitles()
        logger.info("Subtitles generated!")

    def generate_from_reddit_comments(self, reddit_url, max_comment_number, background_url, background_music_url, create_images, create_subtitles):
        title, comments = self.parse_reddit_comments(reddit_url, max_comment_number)
        if (create_images):
            self.generate_illustrations(title, comments)
        self.generate_tts(title, comments)
        self.generate_background(background_url, background_music_url)
        self.render_video()
        if (create_subtitles):
            self.generate_subtitles()

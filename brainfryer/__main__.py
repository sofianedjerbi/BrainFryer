import argparse
import logging
import logging.config
import os
from dotenv import load_dotenv

from brainfryer.creator import *

LOGO = """
  ____               _         _____                         
 | __ )  _ __  __ _ (_) _ __  |  ___|_ __  _   _   ___  _ __ 
 |  _ \\ | '__|/ _` || || '_ \\ | |_  | '__|| | | | / _ \\| '__|
 | |_) || |  | (_| || || | | ||  _| | |   | |_| ||  __/| |   
 |____/ |_|   \\__,_||_||_| |_||_|   |_|    \\__, | \\___||_|   
                                           |___/             
"""

DEFAULT_SONG = "https://www.youtube.com/watch?v=bESTXIqCnac"
DEFAULT_BACKGROUND = "https://www.youtube.com/watch?v=R0b-VFV8SJ8"
DEFAULT_COMMENT_NUMBER = 10

load_dotenv()

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
log_level = log_levels.get(log_level_str, logging.INFO)

# Some modules INFO are too verbose
if log_level == logging.INFO:
    logging.getLogger("openai").setLevel(logging.WARNING) 
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("faster_whisper").setLevel(logging.WARNING)

logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

GPT_KEY = os.getenv('OPENAI_KEY')
GPT_MODEL_TEXT = os.getenv('OPENAI_MODEL_TEXT')
GPT_MODEL_IMAGE = os.getenv('OPENAI_MODEL_IMAGE')
GPT_MODEL_TTS = os.getenv('OPENAI_MODEL_TTS')
GPT_MODEL_SUBTITLES = os.getenv('OPENAI_MODEL_WHISPER')
STABLE_DIFFUSION_HOST = os.getenv('STABLE_DIFFUSION_HOST')
STABLE_DIFFUSION_PORT = os.getenv('STABLE_DIFFUSION_PORT')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate attention-grabbing videos!', prog='python -m brainfryer')
    parser.add_argument('url', nargs='?', default=None, help='Reddit URL')
    parser.add_argument('-c', '--comments', type=int, help='Maximumm number of comments to get (default: 10)')
    parser.add_argument('-b', '--background', help='Youtube background URL (optional)')
    parser.add_argument('-s', '--song', help='Youtube song URL (optional)')
    parser.add_argument('-i', '--gen-images', action='store_true', help='Generate images (default: False)')
    parser.add_argument('-t', '--gen-subtitles', action='store_true', help='Generate subtitles (default: False)')
    parser.add_argument('-d', '--dall-e', action='store_true', help='Use Dall-E instead of Stable Diffusion (default: False)')

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    print(args)

    # If CLI arguments are provided, use them; otherwise, prompt the user
    if args.url is not None:
        url = args.url
        comments = args.comments or DEFAULT_COMMENT_NUMBER
        background = args.background or DEFAULT_BACKGROUND
        song = args.song or DEFAULT_SONG
        gen_images = args.gen_images
        gen_subtitles = args.gen_subtitles
        dall_e = args.dall_e
    else:
        print(LOGO)
        # Query user
        url = input("Reddit url: ")
        comments = input("Maximum number of comments (empty = 10): ") or DEFAULT_COMMENT_NUMBER
        background = input("Youtube background url (empty = default): ") or DEFAULT_BACKGROUND
        song = input("Youtube song url (empty = default): ") or DEFAULT_SONG
        gen_images = True if input("Generate images (Y/N, default = N)? ").strip().lower() == 'y' else False
        gen_subtitles = True if input("Generate subtitles (Y/N, default = N)? ").strip().lower() == 'y' else False
        dall_e = True if input("Use Dall-E ? May cause extra cost. (Y/N, default = N) ").strip().lower() == 'y' else False

    creator = VideoCreator(
        GPT_KEY,
        GPT_MODEL_IMAGE,
        GPT_MODEL_TEXT,
        GPT_MODEL_TTS,
        GPT_MODEL_SUBTITLES,
        dall_e,
        STABLE_DIFFUSION_HOST,
        STABLE_DIFFUSION_PORT
    )

    # Generate
    creator.generate_from_reddit_comments(url, comments, background, song, gen_images, gen_subtitles)

if __name__ == "__main__":
    main()

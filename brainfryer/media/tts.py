import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class TTSAgent:
    def __init__(self, key, model):
        self.client = OpenAI(api_key=key)
        self.model = model
    
    def generate_and_save(self, voice, text, file):
        logger.debug(f"Generating for \"{text}\"")
        response = self.client.audio.speech.create(
            model=self.model,
            voice=voice,
            input=text,
            speed=1.15,
        )
        return response.stream_to_file(file)

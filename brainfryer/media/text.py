import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class TextAgent:
    def __init__(self, key, model):
        self.client = OpenAI(api_key=key)
        self.model = model
    
    def send_message(self, message):
        logger.debug(f"Generating for \"{message}\"")
        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": message
                }
            ],
            model=self.model
        )

        return completion.choices[0].message.content


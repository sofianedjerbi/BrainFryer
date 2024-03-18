import logging
from openai import OpenAI

MAX_ATTEMPT = 5
FALLBACK_TEXT = "Huge flying turtle in the beautiful sunset sky" # Surely you'll get comments about that !
logger = logging.getLogger(__name__)

class TextAgent:
    def __init__(self, key, model):
        self.client = OpenAI(api_key=key)
        self.model = model
    
    def send_message(self, message, attempt=1):
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
        answer = completion.choices[0].message.content
        logger.debug(f"Answer: \"{answer}\"")

        # ignore if new message is counter productive
        if "i'm sorry" in answer.lower() or "i can't" in answer.lower():
            if attempt > MAX_ATTEMPT:
                logger.debug(f"Max tentative reached! Using default text: \"{FALLBACK_TEXT}\"")
                return FALLBACK_TEXT
            logger.debug(f"Useless answer from model. Retrying... {MAX_ATTEMPT - attempt} attept left.")
            return self.send_message(message, attempt + 1)

        return answer


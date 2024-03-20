import logging
import time
import re
import requests
import webuiapi
from openai import OpenAI, BadRequestError, RateLimitError

MAX_ATTEMPT = 3
logger = logging.getLogger(__name__)

class ImageAgentDallE:
    def __init__(self, key, model, text_agent):
        self.client = OpenAI(api_key=key)
        self.model = model
        self.text_agent = text_agent
    
    def generate(self, message, path, attempt=1):
        pattern = re.compile(r'nacked|nude|naked', re.IGNORECASE)
        message = pattern.sub('skin-colored', message).replace("\"", "")
        logger.debug(f"Generating \"{message}\"...")

        try:
            completion = self.client.images.generate(prompt=message, n=1, size="1024x1024", model=self.model) # 1024*1792
        except BadRequestError as e:
            logger.debug(e)
            if (e.code == "content_policy_violation"):
                logger.debug(f"Message denied: \"{message}\"")
                if attempt > MAX_ATTEMPT:
                    logger.debug("Max tentative reached! Image won't be generated.")
                    raise e
                logger.debug(f"Retrying, {MAX_ATTEMPT - attempt} retry left...")
                new_message = self.text_agent.send_message(
                    f"This text does not pass DALL-E content policy. Rewrite it: {message}"
                )
                logger.debug(f"New message: \"{new_message}\"")
                return self.generate(new_message, path, attempt + 1)
            else:
                raise e
        except RateLimitError:
            time.sleep(20)
            logger.debug(f"Rate limit! Sleeping...")
            return self.generate(new_message, path, attempt)

        response = requests.get(completion.data[0].url)
        with open(path, 'wb') as file:
            file.write(response.content)

class ImageAgentStableDiffusion:
    def __init__(self, host, port):
        self.client = webuiapi.WebUIApi(host = host, port = port, sampler='Euler a', steps=35)
    
    def generate(self, message, path):
        pattern = re.compile(r'nacked|nude|naked', re.IGNORECASE)
        message = pattern.sub('skin-colored', message).replace("\"", "")
        logger.debug(f"Generating \"{message}\"...")
        result = self.client.txt2img(
            prompt=message + ", high resolution, realistic textures, best quality, high quality",
            negative_prompt="bad quality, worst quality, low res, lowres, low resolution, ugly, out of frame, unrealistic proportions, floating limbs, extra fingers, missing fingers, oversized hands, undersized hands, distorted, floating limbs",
            cfg_scale=4.5,
            width = 1024,
            height= 1024,
        )
        result.image.save(path)

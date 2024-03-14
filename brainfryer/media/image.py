import time
import re
from openai import OpenAI, BadRequestError

MAX_ATTEMPT = 3

class ImageAgent:
    def __init__(self, key, model, text_agent):
        self.client = OpenAI(api_key=key)
        self.model = model
        self.text_agent = text_agent
    
    def generate(self, message, attempt=1):
        print(f"Generating \"{message}\"...")
        pattern = re.compile(r'nacked|nude|naked', re.IGNORECASE)
        message = pattern.sub('skin-colored', message).replace("\"", "")

        start_time = time.time()
        try:
            completion = self.client.images.generate(prompt=message, n=1, size="1024x1024", model=self.model) # 1024*1792
        except BadRequestError as e:
            print(f"Message denied: \"{message}\"")
            if attempt > MAX_ATTEMPT:
                raise e
            print("Retrying...")
            new_message = self.text_agent.send_message(
                f"This text does not pass DALL-E content policy. Rewrite it: {message}"
            )
            print(f"New message: \"{new_message}\"")
            return self.generate(new_message, attempt + 1)

        execution_time = time.time() - start_time
        time.sleep(max(60 - execution_time, 0))

        return completion.data[0].url

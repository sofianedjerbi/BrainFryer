from openai import OpenAI

class TTSAgent:
    def __init__(self, key, model):
        self.client = OpenAI(api_key=key)
        self.model = model
    
    def generate_and_save(self, voice, text, file):
        response = self.client.audio.speech.create(
            model=self.model,
            voice=voice,
            input=text,
            speed=1.15,
        )
        return response.stream_to_file(file)

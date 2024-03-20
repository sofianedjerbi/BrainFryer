<div align="center">
  <img src="./.github/media/logo.png?" width="32%" height="32%"/>
  <h1>BrainFryer</h1>
  <h3>Generate attention-grabbing videos!</h3>

  [![License](https://img.shields.io/github/license/chaoxel/BrainFryer?style=for-the-badge&logo=github)](LICENSE)
  [![Discord](https://img.shields.io/discord/1195177036210253864?color=5865F2&label=discord&style=for-the-badge)](https://discord.gg/jwb26Xy5M7)
  [![Demo](https://img.shields.io/badge/Tiktok%20-%20Demo?logo=tiktok&label=Demo&style=for-the-badge)](https://www.tiktok.com/@redditeel)

</div>


## How to use
### Basic Usage
You can use the wizard by typing `python -m brainfryer`.  
A CLI is available: `python -m brainfryer <Reddit URL>`

### CLI Options

Brainfryer supports several options for customization:

- `-h`, `--help`: Display the help message and exit.
- `-c COMMENTS`, `--comments COMMENTS`: Specify the maximum number of comments to retrieve (default is 10).
- `-b BACKGROUND`, `--background BACKGROUND`: Provide a YouTube URL for the video background (optional).
- `-s SONG`, `--song SONG`: Provide a YouTube URL for the background song (optional).
- `-i`, `--gen-images`: Enable image generation for your video (disabled by default).
- `-t`, `--gen-subtitles`: Enable subtitle generation for your video (disabled by default).
- `-d`, `--dall-e`: Use Dall-E for image generation instead of Stable Diffusion (disabled by default).
- `-u`, `--upload`: Upload the generated video on TikTok using `cookies.txt` (disabled by default).

### Example

To generate a video with images, subtitles, and upload it to TikTok, using a specific Reddit URL, background, and song, your command might look like this:

```bash
python -m brainfryer https://www.reddit.com/r/exampleSubreddit/examplePost -c 20 -b https://youtu.be/exampleBackground -s https://youtu.be/exampleSong -i -t -u
```

This command uses a Reddit URL, sets the maximum comments to 20, specifies background and song YouTube URLs, enables image and subtitle generation, and uploads the final product to TikTok.

### Demo

A live demo is available [here](https://www.tiktok.com/@redditeel).

## Setup

BrainFryer uses OpenAI's **TTS API** and **ChatGPT** for illustrations.

- Clone the repository: `https://github.com/chaoxel/BrainFryer.git`
- Enter the directory: `cd BrainFryer`
- Install dependencies: `pip install -r requirements.txt`
- Install [playwright](https://playwright.dev/python/docs/intro): `playwright install`
- Copy `.env.example`: `cp .env.example .env`
- Configure `.env`: `nano .env`

If you need subtitles:

- Install [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- Install [cuDNN](https://developer.nvidia.com/cudnn)

If you need illustrations:

- With [Dall-E](https://openai.com/dall-e-3): No configuration needed.
- With [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui): Install the [webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) and run it with `--api`. Configure *host* and *port* in `.env`.

## Behind the Scenes

Brainfryer turns Reddit threads into videos through a multi-step process:

1. **Web Parsing**: Uses Playwright for navigating and taking screenshots of web pages.
2. **Image Generation**: ChatGPT creates prompts for Stable Diffusion or Dall-E to generate illustrations.
3. **Text-to-Speech**: Utilizes OpenAI's TTS API to convert text into speech.
4. **Background Handling**: Downloads and crops YouTube backgrounds with Pytube & Moviepy.
5. **Video Assembly**: Combines images, backgrounds, and audio using Moviepy to create the final video.
6. **Subtitles Creation**: Converts audio to text with Whisper, adding timestamps to generate subtitles.

This streamlined approach automates the creation of engaging videos from online content.

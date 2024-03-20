<div align="center">
  <table style="width:100%;">
    <tr>
      <td style="width:70%;">
        <h1>BrainFryer</h1>
        <h3>Turn online discussions into captivating videos!</h3>
        <a href="LICENSE">
          <img src="https://img.shields.io/github/license/chaoxel/BrainFryer?style=for-the-badge&logo=github" alt="License"/>
        </a>
        <a href="https://discord.gg/jwb26Xy5M7">
          <img src="https://img.shields.io/discord/1195177036210253864?color=5865F2&label=discord&style=for-the-badge" alt="Discord"/>
        </a>
        <a href="https://www.tiktok.com/@redditeel">
          <img src="https://img.shields.io/badge/Demo%20-%20Demo?logo=tiktok&label=TikTok&style=for-the-badge" alt="Demo"/>
        </a>
        <p>Join our creative community!</p>
      </td>
      <td>
        <img src="./.github/media/logo.png?" width="100%" height="100%"/>
      </td>
    </tr>
  </table>
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

1. **Webpage Parsing**: Utilizes Playwright to navigate and parse the target webpage for content extraction.
2. **Screenshot Capture**: Takes screenshots of the webpage, capturing key visual elements.
3. **Content Analysis**: Uses ChatGPT to analyze the extracted content and identify themes or key points.
4. **Illustration Prompt Generation**: Based on the analysis, generates creative prompts for illustrations.
5. **Image Generation**: Sends these prompts to Stable Diffusion or Dall-E, which then generate corresponding images.
6. **Text-to-Speech Synthesis**: Converts the extracted textual content into spoken words using OpenAI's TTS API.
7. **Background Video Processing**:
   - Downloads the specified YouTube background video using Pytube.
   - Edits and crops the background video to fit the final video's format using Moviepy.
8. **Video Assembly**: Combines the generated images, edited background video, and synthesized speech into a cohesive video using Moviepy.
9. **Audio Transcription**: Converts the final video's audio into text using Whisper for subtitle generation.
10. **Subtitle Timing**: Analyzes the transcription to add accurate timestamps for each word, creating synchronized subtitles.
11. **Final Editing**: Applies the subtitles to the video, adjusting for readability and style.


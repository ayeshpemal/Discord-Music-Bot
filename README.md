# Discord Music Bot

A feature-rich Discord music bot built with Python and `discord.py`, capable of playing music from YouTube with support for playlists, volume control, search, and queue shuffling. Audio is streamed at a reduced bitrate of 64kbps for efficiency.

## Features
- **Play Music**: Play songs or playlists from YouTube URLs or search terms.
- **Search**: Search YouTube and select from the top 5 results.
- **Queue Management**: Add songs to a queue, view the queue, and shuffle it.
- **Playback Controls**: Pause, resume, skip, and stop playback.
- **Volume Control**: Adjust volume from 0% to 100%.
- **Low Bitrate**: Streams audio at 64kbps to save bandwidth.

## Prerequisites
Before setting up the bot, ensure you have the following installed:
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **FFmpeg**: Required for audio playback.
  - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract, and add the `bin` folder to your PATH.
  - **Linux**: `sudo apt install ffmpeg`
  - **macOS**: `brew install ffmpeg`
- **Git**: [Install Git](https://git-scm.com/downloads) for cloning the repository.


## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/ayeshpemal/Discord-Music-Bot.git
cd [Discord-Music-Bot]
```

### 2. Install Python Dependencies
Install the required Python libraries using pip:
```bash
pip install discord.py yt-dlp pynacl
```

### 3. Obtain a Discord Bot Token
- Go to the Discord Developer Portal. [Discord Developer Portal](https://discord.com/developers)

- Click "New Application," name it (e.g., "MusicBot"), and click "Create."

- Go to the "Bot" tab, click "Add Bot," then "Yes, do it!"

- Under "Token," click "Copy" to save your bot token (keep it private).

- Make sure to set bot private (Turn off the tick on public bot)

- Enable "Privileged Gateway Intents" (Presence, Server Members, Message Content).

- Go to "OAuth2 > URL Generator," select bot scope, and permissions: Connect and Speak. Copy the URL, open it in a browser, and invite the bot to your server.

### 4. Configure the Bot
- Open musicbot.py in a text editor.

- Replace 'YOUR_BOT_TOKEN_HERE' with your bot token from step 3:
python

- bot.run('YOUR_ACTUAL_TOKEN')

### 5. Run the Bot
Run the bot from the command line:
```bash
python musicbot.py
```

If successful, you’ll see "Logged in as [BotName]" in the terminal.

## Usage
Join a voice channel in your Discord server and use these commands:
| Command           | Description                                | Example                     |
|-------------------|--------------------------------------------|-----------------------------|
| !play [URL/term]  | Plays a song or playlist from a URL or term| !play https://youtube.com/... |
| !play [number]    | Plays a song from the last search results  | !play 2                     |
| !search [keyword] | Searches YouTube and shows top 5 results   | !search Billie Eilish       |
| !pause            | Pauses the current song                    | !pause                      |
| !resume           | Resumes the paused song                    | !resume                     |
| !skip             | Skips the current song                     | !skip                       |
| !stop             | Stops playback and clears the queue        | !stop                       |
| !queue            | Shows the current queue                    | !queue                      |
| !volume [0-100]   | Sets the volume (0-100%)                   | !volume 75                  |
| !shuffle          | Shuffles the current queue                 | !shuffle                    |

## Example Workflow
### Search for a song:
```bash
!search Imagine Dragons
# Bot lists 5 results
```

### Play a result:
```bash
!play 3  # Plays the third result
```

### Add a playlist:
```bash
!play https://www.youtube.com/playlist?list=PL4o29bBf0I0
```

### Shuffle the queue:
```bash
!shuffle
```

## Troubleshooting
Bot Doesn’t Join Voice: Ensure pynacl and FFmpeg are installed, and the bot has Connect/Speak permissions.

Video Unavailable: The bot skips unavailable videos in playlists; check the URL or try another.

No Sound: Verify FFmpeg is in your PATH (ffmpeg -version).

## Contributing
Feel free to fork this repository, make improvements, and submit pull requests!

## License
This project is licensed under the MIT License - see the LICENSE file for details.
Built by [ayeshpemal]
With assistance from Grok, created by xAI.




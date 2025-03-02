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

2. Install Python Dependencies
Install the required Python libraries using pip:
bash

pip install discord.py yt-dlp pynacl

3. Obtain a Discord Bot Token
Go to the Discord Developer Portal.

Click "New Application," name it (e.g., "MusicBot"), and click "Create."

Go to the "Bot" tab, click "Add Bot," then "Yes, do it!"

Under "Token," click "Copy" to save your bot token (keep it private).

Enable "Privileged Gateway Intents" (Presence, Server Members, Message Content).

Go to "OAuth2 > URL Generator," select bot scope, and permissions: Connect and Speak. Copy the URL, open it in a browser, and invite the bot to your server.

4. Configure the Bot
Open musicbot.py in a text editor.

Replace 'YOUR_BOT_TOKEN_HERE' with your bot token from step 3:
python

bot.run('YOUR_ACTUAL_TOKEN')

5. Run the Bot
Run the bot from the command line:
bash

python musicbot.py

If successful, you’ll see "Logged in as [BotName]" in the terminal.


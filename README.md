# ER-Bot
Eagle RSS BOT is a Python script that uses the Discord.py library to post updates from an RSS feed to a Discord channel.

# Getting Started
## Prerequisites
To use this bot, you need to have the following software installed:

* Python 3.x
* Discord Bot using your own Discord Account


## Installation
* Clone the repository: git clone `https://github.com/yourusername/discord-rss-bot.git`
* Install dependencies: `pip install -r requirements.txt`
* Create a `config.json` file with your bot token, feed URL, update interval, and channel ID. Example:
  ```{
    "bot_token": "your-bot-token",
    "feed_url": "https://example.com/feed.xml",
    "update_interval": 3600,
    "channel_id": 123456789012345678
    }
    ```
* Run the bot: python `botfeed.py` or `run.cmd`

## Usage
The bot automatically posts new entries from the RSS feed to the specified channel at the specified interval. To manually post the latest entry, use the !latest command in the channel where the bot is located.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Running the Bot
To run the bot, run the `run.cmd` in the folder inside


## Authors
EagleEye / DCS World Indonesia

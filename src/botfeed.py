import discord
from discord.ext import commands
import asyncio
import feedparser
import json
import logging
import html
import time

# set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO)

# load config file
with open('config.json', 'r') as f:
    config = json.load(f)

# set up bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# get channel object
channel = None
for guild in bot.guilds:
    for c in guild.channels:
        if c.id == config['channel_id']:
            channel = c
            break

async def post_new_entries():
    # parse RSS feed
    feed = feedparser.parse(config['feed_url'])

    # get the latest entry
    latest_entry = feed.entries[0]

    # check if latest entry is newer than last published entry
    latest_published = time.mktime(latest_entry.published_parsed)
    if latest_published > config['last_published']:
        # format entry as HTML string
        title = html.escape(latest_entry.title)
        link = html.escape(latest_entry.link)
        description = latest_entry.description.replace('\n', '<br/>')
        image_url = latest_entry.enclosures[0].url if latest_entry.get('enclosures') else None
        image_html = f'<img src="{image_url}" alt="Image">' if image_url else ''
        html_str = f'<h2>{title}</h2><p><a href="{link}">{link}</a></p><p>{description}</p>{image_html}'

        # post new entry in Discord channel
        embed = discord.Embed(description=html_str, color=0x00ff00)
        await channel.send(embed=embed)

        # update last published time in config
        config['last_published'] = latest_published
        with open('config.json', 'w') as f:
            json.dump(config, f)

        # log new entry
        logging.info(f'New entry posted: {latest_entry.title}')

    # wait for specified interval before checking for new entries again
    await asyncio.sleep(config['update_interval'])
    bot.loop.create_task(post_new_entries())

# event listener for when bot is ready
@bot.event
async def on_ready():
    logging.info('Bot is online!')

    # start checking for new entries
    bot.loop.create_task(post_new_entries())

# command to post latest entry
@bot.command(name='latest')
async def post_latest_entry(ctx):
    # get channel object
    global channel
    if channel is None:
        channel = bot.get_channel(config['channel_id'])
        if channel is None:
            # handle case where channel is not found
            await ctx.send(f"Error: Could not find channel '{config['channel_id']}'")
            return
    
    # parse RSS feed
    feed = feedparser.parse(config['feed_url'])

    # get latest entry
    latest_entry = feed.entries[0]

    # create Embed object with HTML tags
    embed = discord.Embed(title=latest_entry.title, url=latest_entry.link)
    embed.add_field(name="Description", value=latest_entry.description.replace("<br>", "\n"), inline=False)
    embed.set_image(url=latest_entry.enclosures[0].url)

    # post latest entry in Discord channel
    await channel.send(embed=embed)

    # log latest entry
    logging.info(f'Latest entry posted manually: {latest_entry.title}')


# start the bot
bot.run(config['bot_token'])

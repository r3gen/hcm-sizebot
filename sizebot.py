# Work with Python 3.6

import random
from configparser import ConfigParser
from datetime import datetime
from os import path

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

config_filename = 'hcm_sizebot.ini'

size = [
        "1 mm",
        "1 cm",
        "1 inch",
        "3 inch",
        "6 inch",
        "1 foot",
        "3 foot",
        "6 foot",
        "12 foot",
        "50 foot",
        "100 foot",
        "200 foot",
        "400 foot",
        "500 foot",
        "600 foot",
        "800 foot",
        "1000 foot",
        "2000 foot",
        "3000 foot",
        "5000 foot"
    ]

def load_config():
    bot_config = ConfigParser()
    if path.exists(config_filename):
        bot_config.read(config_filename)
        reset_config(bot_config)
    else:
        bot_config['Default'] = {
            "reset_hour": '5',
            "last_reset": datetime.now().isoformat()
        }
        save_config(bot_config)

    return bot_config


def save_config(bot_config):
    with open(config_filename, 'w') as config_file:
        bot_config.write(config_file)


def reset_config(bot_config):
    last_date = datetime.fromisoformat(bot_config["Default"]["last_reset"])
    if last_date.date() < datetime.now().date():
        for section in bot_config.sections():
            if section != "Default":
                bot_config.remove_section(section)
                bot_config.add_section(section)
        bot_config["Default"]["last_reset"] = datetime.now().isoformat()
        save_config(bot_config)


def read_token():
    import os
    return os.environ["SIZEBOT_TOKEN"]
    '''with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()
    '''


TOKEN = read_token()

sizes = dict()

config = load_config()


@bot.command()
async def sizeme(ctx):
    reset_config(config)
    user_id = "{}".format(ctx.author.id)
    server = "{}".format(ctx.guild.id)
    if config.has_option(server, user_id):
        size = config[server][user_id]
    else:
        size = get_size()
    msg = '{0.author.mention} is '.format(ctx.message) + size + " tall."
    await ctx.send(msg)
    # sizes[user] = size
    if not config.has_section(server):
        config.add_section(server)
    config[server][user_id] = size
    save_config(config)


@bot.command()
async def showsizes(ctx):
    reset_config(config)
    server = ctx.guild.id
    size_list = sorted(config[server].items(), key=lambda x: x[1], reverse=True)
    msg = "All sizes:\n"
    for user in size_list:
        member = await ctx.guild.fetch_member(user[0])
        username = member.display_name
        msg += username + ": " + user[1] + "\n"
    await ctx.send(msg)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def get_size():
    return size[random.randint(1, len(size))]


bot.run(TOKEN)

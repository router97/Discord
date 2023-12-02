# IMPORTS
from discord import Intents
from discord.ext.commands import Bot
from config import config
from openai import OpenAI

# VARIABLES
intents = Intents.all()
bot = Bot(command_prefix = config['prefix'], intents = intents)
# ai_client = OpenAI(api_key=config['openai_token'])
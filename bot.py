# IMPORTS
from discord import Intents
from discord.ext.commands import Bot
from config import config

# VARIABLES
intents = Intents.all()
bot = Bot(command_prefix = config['prefix'], intents = intents)
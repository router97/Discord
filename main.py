# IMPORTS
import discord
from discord.ext import commands

from cogs.Fun import Fun
from cogs.Moderation import Moderation
from cogs.Info import Info

from views.rps_buttons import RPS_Buttons

from config import config

from bot import bot
# from bot import ai_client




# CONTEXT MENUS
@bot.tree.context_menu(name='Rock, Paper, Scissors')
async def rps_context_menu(interaction: discord.Interaction, user: discord.Member):
    """Rock, Paper, Scissors context menu."""
    
    # You can't play with yourself :(
    if interaction.user == user:
        return await interaction.response.send_message('typen', ephemeral=True)
    
    # Making an embed
    embed = discord.Embed(title='Rock, Paper, Scissors')
    
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar)
    
    embed.add_field(name=interaction.user.display_name, value='Not Ready')
    embed.add_field(name=user.display_name, value='Not Ready')
        
    # Setting up the buttons
    buttons = RPS_Buttons(user1=interaction.user, user2=user)
    
    # Sending the message
    await interaction.response.send_message(view=buttons, embed=embed)




# FUNCTIONS
async def set_bot_activity():
    bot_activity = discord.Activity(type=discord.ActivityType.playing, name="Team Fortress 2")
    await bot.change_presence(activity=bot_activity, status=discord.Status.do_not_disturb)


async def setup_cogs():
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(Info(bot))
    await bot.tree.sync()


class EngineerHelp(commands.MinimalHelpCommand):
    """Help command."""
    
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=discord.Colour.red())
            embed.set_image(url=bot.user.avatar.url)
            await destination.send(embed=embed)

bot.help_command = EngineerHelp()


# EVENTS
@bot.event
async def on_ready():
    await set_bot_activity()
    await setup_cogs()
    print(f"Logged in as {bot.user.name} ({bot.user.id})")


@bot.event
async def on_message(message: discord.Message):
    """Message handler."""
    
    # Checking if the message is a command
    await bot.process_commands(message)

# LAUNCH
bot.run(config['token'])                     
# IMPORTS
import discord

from cogs.Fun import Fun
from cogs.Moderation import Moderation
from cogs.Info import Info

from views.rps_buttons import RPS_Buttons
from views.ttt_buttons import TTT_Buttons
from views.rr_buttons import RR_Buttons

from config import config
from bot import bot


# CONTEXT MENUS
@bot.tree.context_menu(name='Rock, Paper, Scissors')
async def rps_context_menu(interaction: discord.Interaction, user: discord.Member):
    """Rock, Paper, Scissors context menu."""
    
    # You can't play with yourself
    if interaction.user == user:
        return await interaction.response.send_message('typen', ephemeral=True)
    
    # Making an embed
    embed = discord.Embed(title='Rock, Paper, Scissors')
    
    embed.add_field(name=interaction.user.display_name, value='Not Ready')
    embed.add_field(name=user.display_name, value='Not Ready')
        
    # Setting up the buttons
    buttons = RPS_Buttons(user1=interaction.user, user2=user)
    
    # Sending the message
    await interaction.response.send_message(view=buttons, embed=embed)

@bot.tree.context_menu(name='Tic, Tac, Toe')
async def ttt_context_menu(interaction: discord.Interaction, user: discord.Member):
    """Tic, Tac, Toe context menu."""
    
    # You can't play with yourself
    if interaction.user == user:
        return await interaction.response.send_message('typen', ephemeral=True)
    
    # Making an embed
    embed = discord.Embed(title='Tick, Tack, Toe', color=discord.Color.red())
    
    embed.add_field(name='Board', value=':white_large_square::white_large_square::white_large_square:\n'*3)
    embed.set_author(name=f"{interaction.user.display_name} vs {user.display_name}")
    
    # Setting up the buttons
    buttons = TTT_Buttons(user1=interaction.user, user2=user)
    
    # Sending the message
    await interaction.response.send_message(view=buttons, embed=embed)

@bot.tree.context_menu(name='Russian Roulette')
async def rr_context_menu(interaction: discord.Interaction, user: discord.Member):
    """Russian Roulette context menu."""
    
    # You can't play with yourself
    if interaction.user == user:
        return await interaction.response.send_message('typen застрелился не так работает', ephemeral=True)
    
    # Making an embed
    embed = discord.Embed(title='Russian Roulette')
    embed.add_field(name='Turn', value=interaction.user.display_name)
    embed.add_field(name='Barrel', value='⦿⦿⦿⦿⦿⦿')
    embed.set_author(name=f"{interaction.user.display_name} vs {user.display_name}")
    
    # Setting up the buttons
    buttons = RR_Buttons(user1=interaction.user, user2=user)
    
    # Sending the message
    await interaction.response.send_message(view=buttons, embed=embed)


# FUNCTIONS
async def setup_cogs():
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(Info(bot))
    await bot.tree.sync()


# EVENTS
@bot.event
async def on_ready():
    await setup_cogs()
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

 
# LAUNCH
if __name__ == '__main__':
    bot.run(config['token'])
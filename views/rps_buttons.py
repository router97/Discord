# IMPORTS
from random import choice

import discord

from bot import bot


# BUTTONS
class RPS_Buttons(discord.ui.View):
    """Rock, Paper, Scissors buttons"""
    
    def __init__(self, user1: discord.Member, user2: discord.Member):
        super().__init__() 
        self.user1 = user1
        self.user2 = user2
        self.pick = {}
        
        self.__winning_combinations = {
            ('rock', 'paper'): self.user2.display_name,
            ('rock', 'scissors'): self.user1.display_name,
            ('paper', 'rock'): self.user1.display_name,
            ('paper', 'scissors'): self.user2.display_name,
            ('scissors', 'rock'): self.user2.display_name,
            ('scissors', 'paper'): self.user1.display_name,
        }
    
    async def game_logic(self) -> str:
        """Game logic for Rock, Paper, Scissors"""
        
        # Fetch the picks
        pick1 = self.pick[self.user1]
        pick2 = self.pick[self.user2]
        
        # Check for draw
        if pick1 == pick2:
            return 'draw!'
        
        # Check who won
        if (pick1, pick2) in self.__winning_combinations:
            return f"{self.__winning_combinations[(pick1, pick2)]} won!"
    
    async def interaction_check_rps(self, interaction: discord.interactions.Interaction, pick: str) -> None:
        """Rock, Paper, Scissors pick handler"""
        
        # Check if the user is a player
        if interaction.user not in (self.user1, self.user2):
            return
            
        # Accept interaction
        await interaction.response.defer()
        
        # Generate a response, if the player is the bot
        if self.user2 == bot.user:
            self.pick.update({self.user2: choice(['rock', 'paper', 'scissors'])})
            
        # Save the pick
        self.pick.update({interaction.user: pick})
        
        # Update the embed
        embed = interaction.message.embeds[0]
        embed.set_field_at(0, name=self.user1.display_name, value='Ready' if self.user1 in self.pick else 'Not Ready')
        embed.set_field_at(1, name=self.user2.display_name, value='Ready' if self.user2 in self.pick else 'Not Ready')
        await interaction.message.edit(embed=embed)
        
        # Check if both users are ready
        if len(self.pick) != 2:
            return
        
        # Check for game outcome
        outcome = await self.game_logic()
        
        # Provide results
        await interaction.message.reply(f"{outcome}\n{self.user1.display_name} picked {self.pick[self.user1]}, {self.user2.display_name} picked {self.pick[self.user2]}")
        
        # Clear the buttons
        await interaction.message.edit(view=None)
    
    async def generate_embed(self) -> discord.Embed:
        """Generate the game embed"""
        
        embed = discord.Embed(title='Rock, Paper, Scissors')
        
        embed.add_field(name=self.user1.display_name, value='Ready' if self.user1 in self.pick else 'Not Ready')
        embed.add_field(name=self.user2.display_name, value='Ready' if self.user2 in self.pick else 'Not Ready')
        return embed
    
    
    @discord.ui.button(label='rock', emoji="🗿", row=0, style=discord.ButtonStyle.primary)
    async def rock_button_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.interaction_check_rps(interaction, 'rock')

    @discord.ui.button(label='paper', emoji="📄", row=0, style=discord.ButtonStyle.primary)
    async def paper_button_callback(self, interaction: discord.interactions.Interaction, button):
        await self.interaction_check_rps(interaction, 'paper')
    
    @discord.ui.button(label='scissors', emoji="✂️", row=0, style=discord.ButtonStyle.primary)
    async def scissors_button_callback(self, interaction: discord.interactions.Interaction, button):
        await self.interaction_check_rps(interaction, 'scissors')
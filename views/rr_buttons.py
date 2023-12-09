# IMPORTS
from random import shuffle

import discord


# BUTTONS
class RR_Buttons(discord.ui.View):
    """Russian Roulette"""
    
    BULLET_SYMBOL = '⁍'
    
    def __init__(self, user1: discord.Member, user2: discord.Member):
        super().__init__()
        self.user1 = user1
        self.user2 = user2
        self.player = user1
        self.barrel = [None, None, None, None, None, 'bullet']
        shuffle(self.barrel)
    
    async def pull(self):
        """Pull the trigger"""
        
        if self.barrel[0]:
            self.barrel.pop(0)
            return self.player.id
        self.barrel.pop(0)
    
    async def process_button_interaction(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        """Process button interaction"""
        
        # Check if it's the user's move
        if interaction.user != self.player:
            return
        
        # Pull the trigger
        outcome = await self.pull()
        await interaction.response.defer()
        
        # Change the player
        self.player = self.user2 if self.player == self.user1 else self.user1
        
        # Fetch and edit the embed
        embed_new = interaction.message.embeds[0]
        if not outcome:
            embed_new.set_field_at(0, name='Turn', value=self.player.display_name)
            embed_new.set_field_at(1, name='Barrel', value='⦿'*len(self.barrel))

        # If someone lost - send a message and remove the buttons
        else:
            await interaction.channel.send(f"<@{outcome}> застрелився тупен")
            self.button_pull_callback.disabled = True
        
        await interaction.message.edit(embed=embed_new, view=self)
    
    
    @discord.ui.button(label='Pull', row=0, style=discord.ButtonStyle.primary)
    async def button_pull_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)
# IMPORTS
import discord


# BUTTONS
class TTT_Buttons(discord.ui.View):
    """Tic, Tac, Toe view"""

    EMPTY_SYMBOL = '⬜'
    CROSS_SYMBOL = '❌'
    CIRCLE_SYMBOL = '⭕'
    
    def __init__(self, user1: discord.Member, user2: discord.Member):
        super().__init__()
        self.user1 = user1
        self.user2 = user2
        self.player = user1
        self.board_map = {str(i): None for i in range(1, 10)}
    
    async def retry(self, interaction: discord.Interaction, button: discord.Button):
        """Reload everything and begin the game again"""
        
        # Check if it's one of the players who pressed the button
        if interaction.user not in (self.user1, self.user2):
            return
        
        # Reset the board
        self.board_map = {str(i): None for i in range(1, 10)}
        
        # Set the player to the player who began the game in the first place
        self.player = self.user1
        
        # Fetch the old embed
        embed = interaction.message.embeds[0]
        
        # Make an empty board
        embed.set_field_at(0, name='Board', value=':white_large_square::white_large_square::white_large_square:\n'*3)
        
        # Enable all the buttons
        for callback in self.children:
            callback.disabled = False
        
        # Disable the retry button
        self.button_retry_callback.disabled = True
        
        # Update the message
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def game_logic(self, board_map: str):
        """Process a string map from embed"""
        
        # Split the string map by lines
        board_map_line_split = board_map.splitlines()
        
        # Get the horizontal combinations
        board_map_horizontal = [[i for i in el] for el in board_map_line_split]
        
        # Get the vertical combinations
        board_map_vertical = [[el[counter] for el in board_map_line_split] for counter in range(3)]
        
        # Get the cross combinations
        board_map_cross1 = [[el[counter] for el, counter in zip(board_map_line_split, range(3))]]
        board_map_cross2 = [[el[counter] for el, counter in zip(board_map_line_split, range(2, -1, -1))]]
        
        # Check every combination for a win
        for checking in (board_map_horizontal, board_map_vertical, board_map_cross1, board_map_cross2):
            for check in checking:
                if check == [TTT_Buttons.CROSS_SYMBOL, TTT_Buttons.CROSS_SYMBOL, TTT_Buttons.CROSS_SYMBOL]:
                    return self.user1.id
                elif check == [TTT_Buttons.CIRCLE_SYMBOL, TTT_Buttons.CIRCLE_SYMBOL, TTT_Buttons.CIRCLE_SYMBOL]:
                    return self.user2.id
    
    async def process_button_interaction(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        """Process button interaction"""
        
        # Check if it's the user's move
        if interaction.user != self.player:
            return
        
        # Update the game map
        self.board_map.update({button.label: interaction.user.id})
        
        # Fetch the old embed
        embed = interaction.message.embeds[0]
        
        # Generate a board for the embed
        board_map_updated = []
        for key, value in self.board_map.items():
            if not value:
                symbol=TTT_Buttons.EMPTY_SYMBOL
            elif value == self.user1.id:
                symbol = TTT_Buttons.CROSS_SYMBOL
            elif value == self.user2.id:
                symbol = TTT_Buttons.CIRCLE_SYMBOL
            board_map_updated.append(symbol)
        board_map_updated = ''.join(board_map_updated)
        
        # Split every 3 elements with a new line
        board_map_updated = '\n'.join([board_map_updated[counter:counter+3] for counter in range(0, len(board_map_updated), 3)])
        
        # Update the board field
        embed.set_field_at(0, name='Board', value=board_map_updated)
        
        # Disabling the button
        button.disabled = True
        
        # Updating the message with a new embed and buttons
        await interaction.response.edit_message(embed=embed, view=self)
        
        # Check for a draw
        if None not in list(self.board_map.values()):
            await interaction.message.channel.send(f"draw!")
            for callback in self.children:
                callback.disabled = True
            self.button_retry_callback.disabled = False
            return await interaction.message.edit(view=self)
        
        # Check for a win
        outcome = await self.game_logic(board_map_updated)
        
        # If someone won - send a message and remove the buttons
        if outcome:
            await interaction.message.channel.send(f"<@{outcome}> won!")
            for callback in self.children:
                callback.disabled = True
            self.button_retry_callback.disabled = False
            return await interaction.message.edit(view=self)

        # If the game hasn't ended, change the player
        if self.player == self.user1:
            self.player = self.user2
            return
        self.player = self.user1
    
    
    @discord.ui.button(label='1', row=0, style=discord.ButtonStyle.primary)
    async def button1_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)

    @discord.ui.button(label='2', row=0, style=discord.ButtonStyle.primary)
    async def button2_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)
    
    @discord.ui.button(label='3', row=0, style=discord.ButtonStyle.primary)
    async def button3_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)
    
    @discord.ui.button(label='4', row=1, style=discord.ButtonStyle.primary)
    async def button4_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)

    @discord.ui.button(label='5', row=1, style=discord.ButtonStyle.primary)
    async def button5_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)
    
    @discord.ui.button(label='6', row=1, style=discord.ButtonStyle.primary)
    async def button6_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)
    
    @discord.ui.button(label='7', row=2, style=discord.ButtonStyle.primary)
    async def button7_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)

    @discord.ui.button(label='8', row=2, style=discord.ButtonStyle.primary)
    async def button8_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)
    
    @discord.ui.button(label='9', row=2, style=discord.ButtonStyle.primary)
    async def button9_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.process_button_interaction(interaction, button)
    
    
    @discord.ui.button(label='Retry', row=3, style=discord.ButtonStyle.secondary, disabled=True)
    async def button_retry_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
        await self.retry(interaction, button)
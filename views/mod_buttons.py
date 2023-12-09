# IMPORTS
# import discord


# # BUTTONS
# class ModView(discord.ui.View):
#     """Mod role buttons"""
    
#     member = discord.Member
#     __access_roles = [
#         982058707460456528, 
#         987499302895108147, 
#         1101608867302998016, 
#         982055691013464146
#         ]
    
#     def __init__(self, member: discord.Member):
#         super().__init__()
#         self.member = member
    
    
#     async def button_work(self, interaction: discord.interactions.Interaction, id1: int):
        
#         # Fetch the server
#         server = interaction.guild
        
#         member_interaction = interaction.user
        
#         role = discord.utils.get(server.roles, id = id1)
#         roles_list = member_interaction.roles
#         roles_list_id = [element.id for element in roles_list]
        
#         for id in roles_list_id:
#             if id in self.__access_roles:
#                 await interaction.response.send_message(f"Updated <@{self.member.id}> with <@&{role.id}>")
#                 await self.member.add_roles(roles=role, reason=f'{member_interaction} used the command "mod", to give {self.member} the role {role.name}')
#                 return
#         await interaction.response.send_message('ERROR!', ephemeral=True)
    
    
#     @discord.ui.button(label="jort", row=0, style=discord.ButtonStyle.primary)
#     async def first_button_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
#         await self.button_work(interaction, 987465332157481022)
    
    
#     @discord.ui.button(label="Jun. Mod", row=0, style=discord.ButtonStyle.primary)
#     async def second_button_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
#         await self.button_work(interaction, 998177461051330580)
    
    
#     @discord.ui.button(label="Mod", row=1, style=discord.ButtonStyle.primary)
#     async def third_button_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
#         await self.button_work(interaction, 982055862287859742)

    
#     @discord.ui.button(label="Head. Mod", row=1, style=discord.ButtonStyle.primary)
#     async def fourth_button_callback(self, interaction: discord.interactions.Interaction, button: discord.ui.Button):
#         server = interaction.guild
        
#         member_interaction = interaction.user
        
#         role = discord.utils.get(server.roles, id = 982058707460456528)
#         roles_list = member_interaction.roles
#         roles_list_id = [element.id for element in roles_list]
        
#         for id in roles_list_id:
#             if id in (987499302895108147, 1101608867302998016, 982055691013464146):
#                 await interaction.response.send_message(f"Updated <@{self.member.id}> with <@&{role.id}>")
#                 await self.member.add_roles(role) 
#                 return
#         await interaction.response.send_message('ERROR!')
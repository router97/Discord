# IMPORTS
from sys import path as sys_path
sys_path.append('D:\\Programm\\Python\\Discord')
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from views.buttons_mod import ModView


# COG
class Moderation(commands.Cog):
    """Moderation commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    # @commands.hybrid_command(name="mod", description="Mod promotion")
    # async def mod(self, ctx: commands.Context, member: commands.MemberConverter):
    #     """Mod promotion"""
        
    #     # Fetching the guild
    #     server = ctx.guild
        
    #     # Setting up the buttons
    #     buttons = ModView(member=member)
        
    #     # Sending the message
    #     await ctx.reply(f"Choose role to give {member}", view = buttons)
    
    
    @commands.hybrid_command(name="mute", description="Mute a member")
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx: commands.Context, member: commands.MemberConverter, duration: str = 'perm', reason: str = 'No reason given'):
        """Timeout a member"""
        
        delta = timedelta(seconds=duration)
        
        await member.timeout(until=delta, reason=reason)
        await ctx.reply(f'{member} was timed out for {duration} due to "{reason}"', ephemeral=True)
    
    
    @commands.hybrid_command(name="ban", description="Ban a member (permanently)")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: commands.MemberConverter, reason: str = 'No reason given'):
        """Ban a member (permanently)"""
        
        await ctx.guild.ban(member, reason=reason)
    
    
    @commands.hybrid_command(name="kick", description="Kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: commands.MemberConverter, reason: str ='No reason given'):
        """Kick"""
        
        # Kick the member
        await member.kick(reason=reason)
        
        # Sending a message
        await ctx.reply(f'kicked {member.mention} for "{reason}"')
    
    
    @kick.error
    async def kick_error(self, ctx: commands.Context, error: commands.CommandError):
        """Kick errors handler"""
        
        # Missing permissions handler
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("you are missing kick permissions", ephemeral=True)


# SETUP
def setup(bot):
    bot.add_cog(Moderation(bot))
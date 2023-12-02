# IMPORTS
import asyncio
from random import randint, choice

import discord
from discord.ext import commands

from bot import bot
from views.rps_buttons import RPS_Buttons



# COG
class Fun(commands.Cog):
    """Miscellaneous commands"""
    
    
    emojis_num = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟')
    
    fakt_map = {
        'a': 'ф', 'b': 'и', 'c': 'с', 'd': 'в', 'e': 'у', 'f': 'а', 'g': 'п', 'h': 'р',
        'i': 'ш', 'j': 'о', 'k': 'л', 'l': 'д', 'm': 'ь', 'n': 'т', 'o': 'щ', 'p': 'з',
        'q': 'й', 'r': 'к', 's': 'ы', 't': 'е', 'u': 'г', 'v': 'м', 'w': 'ц', 'x': 'ч',
        'y': 'н', 'z': 'я', ',': 'б', '.': 'ю', '[': 'х', ']': 'ъ', "'": 'э', '`': 'ё',
        ' ': ' '
    }
    
    random_replies = [
        "I'm good", 
        "KYS = Keep Yourself Safe", 
        "Nah", 
        "I'll pass on that one", 
        "No, thanks", 
        "/me Лицом к стене! 1... 2... 3... Стреляю!"
    ]
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.hybrid_command(name="ip", description="Generate a random IP address")
    async def ip(self, ctx: commands.Context):
        """Generate a random IP address"""
        # Generate 4 random numbers
        ip_numbers = [str(randint(0,255)) for _ in range(4)]
        
        # Join them with a dot
        ip_address = '.'.join(ip_numbers)
        
        await ctx.reply(ip_address)
    
    @commands.hybrid_command(name="kys", description="Generate a random reply")
    async def kys(self, ctx: commands.Context):
        """Generate a random reply"""
        await ctx.reply(choice(self.random_replies))
    
    @commands.command()
    async def poll(self, ctx: commands.Context, name: str, *args: str):
        """Create a poll."""
        
        # Zipping the options to nums (only 10 nums, so only 10 options available)
        options = zip(self.emojis_num, args)
        
        # Converting it into a string
        options_str = "\n".join([f"{emoji}: {option}" for emoji, option in options])
        
        # Making the embed
        embed = discord.Embed(title=f"{name}", description=options_str)
        
        # Setting the author, if possible
        try:
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        except:
            pass
        
        # Sending the embed
        poll = await ctx.send(embed=embed)
        
        # Adding reactions
        for emoji, option in zip(self.emojis_num, args):
            await poll.add_reaction(emoji)
    
    @commands.hybrid_command(name="rand", description="Generate a random number")
    async def rand(self, ctx: commands.Context, start: str, finish: str):
        """Generate a random number."""
        
        # Check if given arguments are valid integers
        try:
            start, finish = int(start), int(finish)
        except ValueError:
            return await ctx.reply("invalid typen")
        
        # Check if start is bigger than the finish
        if start > finish:
            return await ctx.reply("Start should be less than or equal to finish.")
        
        # Check if start is equal to finish
        if start == finish:
            return await ctx.reply("guess the answer.")

        # Generate the random number
        random_number = randint(start, finish)
        
        # Send it
        await ctx.reply(f"{random_number}")
    
    @commands.hybrid_command(name="randmember", description="Ping a random member from the guild")
    async def randmember(self, ctx: commands.Context):
        """Ping a random member from the guild"""
        
        # Get a list of server members without bots
        real_members_ids = [member.id for member in ctx.guild.members if not member.bot]
        
        # Send a random member from the list
        await ctx.reply(f"<@{choice(real_members_ids)}>")
    
    @commands.hybrid_command(name="fakt", description="Faktorizaciya verh")
    async def fakt(self, ctx: commands.Context):
        """Faktorizaciya niz"""
        
        # Getting the fakt
        fakt = ctx.message.content.replace('.fakt ', '', 1).casefold()
        
        # Translating from fakt language to real
        result = ''.join([self.fakt_map.get(char, char) for char in fakt])
        
        # Sending the result
        await ctx.reply(result, ephemeral=True)
    
    @commands.hybrid_command(name="rps", description="Rock, Paper, Scissors")
    async def rps(self, ctx: commands.Context, member: commands.MemberConverter):
        """Rock, Paper, Scissors"""
        
        # You can't play with yourself :(
        if ctx.author == member:
            return await ctx.reply('typen')
        
        # Making an embed
        embed = discord.Embed(title='Rock, Paper, Scissors')
        
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar)
        
        embed.add_field(name=ctx.author.display_name, value='Not Ready')
        embed.add_field(name=member.display_name, value='Not Ready')
        
        # Setting up the buttons
        buttons = RPS_Buttons(user1=ctx.author, user2=member)
        
        # Sending the message
        await ctx.reply(view=buttons, embed=embed)
    
    @commands.command()
    async def do(self, ctx: commands.Context, *, activity: str):
        """Change the presence of the bot."""
        
        # Create Activity object
        new_presence = discord.Activity(type=discord.ActivityType.playing, name=activity)
        
        # Change the presence
        await self.bot.change_presence(activity=new_presence, status=discord.Status.do_not_disturb)
        
        # Acknowledge the action
        await ctx.reply('changed the presence!', ephemeral=True)


# SETUP
def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))



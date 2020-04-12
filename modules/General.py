# Import required libraries:
import time
from glob import glob
from run import em, back_slash
from discord.ext import commands


# Our Cog object.
class General(commands.Cog):
    # Initialize our bot
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, message: str = None):
        """A basic say command."""
        if message is None:  # If no message was provided lets tell them they need to provide one.
            return await ctx.send(**em("Please provide a message, example usage:\n`!say hello`"))
        await ctx.send(message)

    @commands.command()
    async def embed(self, ctx, message: str = None):
        """A basic embed command."""
        if message is None:  # If no message was provided lets tell them they need to provide one.
            return await ctx.send(**em("Please provide a message, example usage:\n`!say hello`"))
        await ctx.send(**em(message))

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx):
        """Reload the bot."""
        msg = await ctx.send(**em("Started reloading the bot..."))
        first = time.perf_counter()
        for module in sorted(glob("modules/*.py")):
            self.bot.reload_extension(module.replace(back_slash, '.')[:-3])
        last = time.perf_counter()
        await msg.edit(**em(f"Successfully reloaded the bot!\nIt took `{round((last-first)*1000, 2)}ms`"))


# Always add this COG!
def setup(bot):
    bot.add_cog(General(bot))

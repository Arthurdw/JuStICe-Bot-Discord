# Import required libraries:
from run import em, field
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


# Always add this COG!
def setup(bot):
    bot.add_cog(General(bot))

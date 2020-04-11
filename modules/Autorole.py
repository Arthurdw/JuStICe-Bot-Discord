# Import required libraries:
from run import em, back_slash
from discord.ext import commands
from configparser import ConfigParser

# Setup and read config:
config = ConfigParser()
config.read(f"settings{back_slash}config.cfg")


# Create our 'Verification' class instance.
class Autorole(commands.Cog):
    # Initialize our static variables.
    main = config["GENERAL"]["main"]

    # Initialize our bot object & our channel.
    def __init__(self, bot):
        self.bot = bot
        self.roles = config["AUTOROLE"]["roles"]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Send a message to the channel when a member joins.
        if member.guild.id == int(config["GENERAL"]["main"]):
            await member.add_roles(*self.roles, reason="Automatic role!")

    @commands.Cog.listener()
    async def on_ready(self):
        # Only apply the value here to prevent that it returns None because no instance has been created yet.
        self.main = self.bot.get_guild(int(self.main))
        self.roles = [self.main.get_role(int(role)) for role in [item.strip() for item in str(self.roles).split(",")]]


# Add our COG if its enabled.
def setup(bot):
    if config["AUTOROLE"]["enabled"] == "true":
        bot.add_cog(Autorole(bot))

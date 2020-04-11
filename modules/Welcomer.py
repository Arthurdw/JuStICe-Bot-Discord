# Import required libraries:
from run import em, back_slash
from discord.ext import commands
from configparser import ConfigParser
from utils.parser import member_replacements as mr

# Setup and read config:
config = ConfigParser()
config.read(f"settings{back_slash}config.cfg")


# Create our 'Welcomer' class instance.
class Welcomer(commands.Cog):
    # Initialize our static messages.
    message = config["WELCOME"]["message"]
    leave = config["WELCOME"]["leave"]
    leave_enabled = True if config["WELCOME"]["send"] == 'true' else False

    # Initialize our bot object & our channel.
    def __init__(self, bot):
        self.bot = bot
        self.channel = config["WELCOME"]["channel"]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Send a message to the channel when a member joins.
        await self.channel.send(**em(mr(self.message, member).replace("{membercount}", str(len(member.guild.members)))))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Check if we need to send a message!
        if self.leave_enabled:
            await self.channel.send(**em(mr(self.leave, member).replace("{membercount}",
                                                                        str(len(member.guild.members)))))

    @commands.Cog.listener()
    async def on_ready(self):
        # Only apply the value here to prevent that it returns None because no instance has been created yet.
        self.channel = self.bot.get_channel(int(self.channel))


# Add our COG if its enabled.
def setup(bot):
    if True if config["WELCOME"]["enabled"] == "true" else False:
        bot.add_cog(Welcomer(bot))

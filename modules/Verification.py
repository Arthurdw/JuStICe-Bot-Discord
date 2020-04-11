# Import required libraries:
from run import em, back_slash
from discord.ext import commands
from configparser import ConfigParser
from utils.parser import member_replacements as mr

# Setup and read config:
config = ConfigParser()
config.read(f"settings{back_slash}config.cfg")


# Create our 'Verification' class instance.
class Verification(commands.Cog):
    # Initialize our static variables.
    main = config["GENERAL"]["main"]
    message = config["VERIFY"]["message"]
    messageID = config["VERIFY"]["messageID"]

    # Initialize our bot object & our channel.
    def __init__(self, bot):
        self.bot = bot
        self.role = config["VERIFY"]["role"]
        self.main = config["GENERAL"]["main"]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Send a message to the channel when a member joins.
        if member.guild.id == int(config["GENERAL"]["main"]):
            await member.add_roles(self.role, reason="Verification role!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Successful verification!
        if payload.message_id == int(self.messageID):
            await payload.member.remove_roles(self.role)
            try:
                await payload.member.send(**em(mr(self.message, payload.member)))
            except Exception:
                pass

    @commands.Cog.listener()
    async def on_ready(self):
        # Only apply the value here to prevent that it returns None because no instance has been created yet.
        self.main = self.bot.get_guild(int(self.main))
        self.role = self.main.get_role(int(self.role))


# Add our COG if its enabled.
def setup(bot):
    if config["VERIFY"]["enabled"] == "true":
        bot.add_cog(Verification(bot))

# Import required libraries:
from run import em, field, back_slash
from discord.ext import commands
from configparser import ConfigParser

config = ConfigParser()
config.read(f"settings{back_slash}config.cfg")


class ReactionRole(commands.Cog):
    # Define our static variables.
    message = config["REACTIONROLE"]["message"]

    # Initialize our bot and define our dynamic variables.
    def __init__(self, bot):
        self.bot = bot
        self.main = config["GENERAL"]["main"]
        self.dev = config["REACTIONROLE"]["dev"]
        self.gamer = config["REACTIONROLE"]["gamer"]
        self.devRole = config["REACTIONROLE"]["devRole"]
        self.gamerRole = config["REACTIONROLE"]["gamerRole"]

    async def reaction_event(self, payload):
        if payload.message_id == int(self.message):
            role = None
            if payload.emoji.id == self.dev.id:
                role = self.devRole
            elif payload.emoji.id == self.gamer.id:
                role = self.gamerRole
            if role is not None:
                reaction_type = "added" if payload.event_type == "REACTION_ADD" else "removed"
                member = payload.user_id
                if payload.event_type == "REACTION_ADD":
                    member = payload.member
                    await member.add_roles(role)
                else:
                    member = self.main.get_member(member)
                    await member.remove_roles(role)
                try:
                    await member.send(**em(f"You have successfully {reaction_type} the {role.name} in {self.main.name}"))
                except Exception:
                    pass

    # Create on reaction add:
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.reaction_event(payload)

    # Create on reaction remove:
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.reaction_event(payload)

    @commands.Cog.listener()
    async def on_ready(self):
        self.dev = self.bot.get_emoji(int(self.dev))
        self.main = self.bot.get_guild(int(self.main))
        self.gamer = self.bot.get_emoji(int(self.gamer))
        self.devRole = self.main.get_role(int(self.devRole))
        self.gamerRole = self.main.get_role(int(self.gamerRole))


# Add our COG if its enabled.
def setup(bot):
    if config["REACTIONROLE"]["enabled"] == "true":
        bot.add_cog(ReactionRole(bot))

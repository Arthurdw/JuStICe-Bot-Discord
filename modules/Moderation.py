# Import required libraries:
from discord import Member
from run import em, field, back_slash
from discord.ext import commands
from configparser import ConfigParser

config = ConfigParser()
config.read(f"settings{back_slash}config.cfg")

enabled = config["MODERATION"]["enabled"] == "true"


class Moderation(commands.Cog):
    # Define our static variables.
    reason = config["MODERATION"]["reason"]
    priority = config["MODERATION"]["priority"]
    logging = config["MODERATION"]["logging"] == "true"
    staff = [int(str(role).strip()) for role in str(config["MODERATION"]["staffRoles"]).split(",")]

    # Initialize our bot and define our dynamic variables.
    def __init__(self, bot):
        self.bot = bot
        self.logError = False
        self.main = config["GENERAL"]["main"]
        self.channel = config["MODERATION"]["channel"]
        self.mutedRole = config["MODERATION"]["mutedRole"]
        # Lets check if a valid log priority got chosen.
        if self.logging and str(self.priority).upper() not in ["LOW", "NORMAL", "HIGH"]:
            self.logError = True

    @commands.command()
    @commands.has_any_role(*staff)
    async def mute(self, ctx, member: Member, *, reason: str = None):
        """Silence a member.
        This gives the muted role. (PERMANENT)"""
        if member == ctx.author:
            return await ctx.send(**em("An invalid member was provided!"))
        if reason is None:
            reason = self.reason
        await member.add_roles(self.mutedRole)
        await ctx.send(**em(f"Successfully muted {member.mention} for `{reason}`"))
        msg = None
        if self.logging:
            msg = await self.channel.send(**em(title=f"Mute - {member}",
                                               content="Retrieving data..."))
            await msg.edit(**em(title=f"Mute - {member}",
                                fields=[field("Information:",
                                              f"Target: {member.mention} [{member.top_role.name}] (`{member.id}`)\n"
                                              f"Author: {ctx.author.mention} [{ctx.author.top_role.name}] (`{ctx.author.id}`)\n"
                                              f"Log ID: `{hex(int(msg.id))}`\n"),
                                        field("Reason:", f"```\n{reason}\n```", False)]))
        await member.send(**em(title=f"You have been muted in {ctx.guild.name}!",
                               fields=[field("Information:", f"Author: {ctx.author.mention} (`{ctx.author.id}`)\n"
                                                             f"Author group: {ctx.author.top_role.name}\n"
                                                             + (f"Log ID: `{hex(int(msg.id))}`" if self.logging else ""),
                                             False),
                                       field("Reason:", f"```\n{reason}\n```", False)]))

    @commands.Cog.listener()
    async def on_ready(self):
        self.main = self.bot.get_guild(int(self.main))
        self.mutedRole = self.main.get_role(int(self.mutedRole))
        if self.logError:  # An invalid log priority got chosen, lets notify that.
            print("\nAn invalid logging priority has been selected.\n"
                  "Please only use one of the following: LOW, NORMAL, HIGH\n"
                  "Because of this moderation logging has been disabled.")
        else:
            self.channel = self.bot.get_channel(int(self.channel))


# Add our COG if its enabled.
def setup(bot):
    if config["MODERATION"]["enabled"] == "true":
        bot.add_cog(Moderation(bot))

# Import base libraries.
from glob import glob
from os import system, name
from discord.ext import commands
from BeatPy.discord import formatter
from configparser import ConfigParser
from discord import NotFound, Forbidden, errors


# Setup BeatPy embeds.
embed_setup = formatter.Embed(footer=False, timestamp=False)
em = embed_setup.create
field = formatter.Field
author = formatter.Author

# System differences.
clear, back_slash = "clear", "/"
if name == "nt":
    clear, back_slash = "cls", "\\"

# Create config objects
token = ConfigParser()
config = ConfigParser()


# Our main bot object.
class Manager(commands.Bot):
    # Just a setup var that is temp.
    pre = []

    # Initialize the whole bot.
    def __init__(self):
        # Initialize the config files:
        token.read(f"settings{back_slash}secret.cfg")
        config.read(f"settings{back_slash}config.cfg")

        # Initialize our bot:
        super().__init__(command_prefix=config["GENERAL"]["prefix"],
                         description="A discord bot created for and by JuSt|Ce",
                         case_insensitive=True, help_attrs=dict(hidden=True))

        # Initialize our extensions (modules):
        print("Loading extensions:")
        for module in sorted(glob("modules/*.py")):
            self.load_module(module)

    # Add a module to the loaded extensions.
    def load_module(self, module: str):
        module_name = module.replace('modules' + back_slash, '')[:-3]
        print(f"Started loading: '{module_name}'")
        self.load_extension(module.replace(back_slash, '.')[:-3])
        load = f"\rLoaded: '{module_name}'{' '*50}"
        if module_name not in list(self.cogs):
            load = f"\rFailed to load: '{module_name}' - disabled in config? {' '*50}"
        self.pre.append(load)
        system(clear)
        print(f"Loaded extensions:\n{', '.join(list(self.cogs))}")
        for item in self.pre:
            print(item)

    # When the bot is ready we will print out information about the current client.
    async def on_ready(self):
        print(f"\n+{'='*40}+")
        print(f"Started bot on {self.user.name}!")
        print(f"Running on app with ID: {self.user.id}")
        print(f"+{'='*40}+")

    # Prevent the bot from reacting on other bots.
    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.get_context(message)
        if ctx.valid:
            if message.guild.id != int(config["GENERAL"]["main"]):
                try:
                    message.channel.send(**em("Hey, I'm a private bot.\n"
                                              "Want to have this bot in your server?\n"
                                              "Feel free to host the bot yourself.\n"
                                              "Download the LTS [here](https://github.com/Arthurdw/JuStICe-Bot-Discord)"))
                except Exception:
                    pass
        await self.process_commands(message)

    # Start the bot.
    def run(self):
        super().run(token["TOKEN"]["token"], reconnect=True)

    async def on_command_error(self, ctx, error):
        if isinstance(error, (NotFound, commands.errors.CommandNotFound)):
            return
        elif isinstance(error, (Forbidden, errors.Forbidden)):
            pass
        elif isinstance(error, (TypeError, commands.MissingRequiredArgument)):
            await ctx.send(**em(f"Missing argument(s) for the '{ctx.command.qualified_name}' command.\n"
                                f"Use the command like this:\n!{ctx.command.qualified_name} "
                                f"{' '.join(ctx.command.clean_params)}"))
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(**em("You are missing the required permissions/role!"))
        else:
            raise error


if __name__ == "__main__":
    Manager().run()

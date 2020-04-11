# Import base libraries.
from glob import glob
from sys import stdout
from os import system, name
from discord.ext import commands
from BeatPy.discord import formatter
from configparser import ConfigParser


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


# Read the config file using a function.
# This way we are able to create a reload command which will reload the config files without having to restart the bot.
def read_config(file):
    # Since our token (secret) file isn't going to change we only need to be able to reload the config file.
    # Its impossible to have your bot running with an invalid token.
    config.read(f"settings{back_slash}{file}.cfg")


# Our main bot object.
class Manager(commands.Bot):
    # Initialize the whole bot.
    def __init__(self):
        # Initialize the config files:
        token.read(f"settings{back_slash}secret.cfg")
        read_config("config")

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
        system(clear)
        module_name = module.replace('modules' + back_slash, '')[:-3]
        print(f"Loaded extensions:\n{', '.join(list(self.cogs))}")
        print(f"Started loading: '{module_name}'", end=" ")
        self.load_extension(module.replace(back_slash, '.')[:-3])
        if module_name in list(self.cogs):
            print("\r", f"\rLoaded: '{module_name}' {' '*50}")
        else:
            print("\r", f"\rFailed to load: '{module_name}' {' '*50}\nMaybe disabled in the config file?")
        stdout.flush()

    # When the bot is ready we will print out information about the current client.
    async def on_ready(self):
        system(clear)
        print(f"Loaded extensions:\n{', '.join(list(self.cogs))}\n")
        print(f"+{'='*40}+")
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


if __name__ == "__main__":
    Manager().run()

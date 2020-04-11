# Import base libraries.
from glob import glob
from sys import stdout
from os import system, name
from discord.ext import commands
from BeatPy.discord import formatter
from configparser import ConfigParser

# Create config objects
config = ConfigParser()
token = ConfigParser()

# Setup BeatPy embeds.
embed_setup = formatter.Embed(footer=False, timestamp=False)
em = embed_setup.create
field = formatter.Field
author = formatter.Author

# System differences.
clear, back_slash = "clear", "/"
if name == "nt":
    clear, back_slash = "cls", "\\"


# Read the config file using a function.
# This way we are able to create a reload command which will reload the config files without having to restart the bot.
def read_config(file):
    # Since our token (secret) file isn't going to change we only need to be able to reload the config file.
    # Its impossible to have your bot running with an invalid token.
    config.read(f"settings{back_slash}{file}.cfg")


# Our main bot object.
class Manager(commands.Bot):
    # Save data to our class var.
    loaded_modules = []

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
        print(f"Loaded extensions:\n{', '.join(self.loaded_modules)}")
        print(f"Started loading: '{module_name}'", end=" ")
        self.load_extension(module.replace(back_slash, '.')[:-3])
        print("\r", f"Loaded loading: '{module_name}' ")
        stdout.flush()
        self.loaded_modules += module_name

    # When the bot is ready we will print out information about the current client.
    async def on_ready(self):
        system(clear)
        print(f"Loaded extensions:\n{', '.join(self.loaded_modules)}")
        print(f"+{'='*20}+")
        print(f"Started bot on {self.user.name}!")
        print(f"Running on app with ID: {self.user.id}")
        print(f"+{'='*20}+")

    # Prevent the bot from reacting on other bots.
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    # Start the bot.
    def run(self):
        super().run(token["TOKEN"]["token"], reconnect=True)


if __name__ == "__main__":
    Manager().run()

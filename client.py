import os

from disnake.ext import commands
from database import Database


class Linguista(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=","
        )
        self.database = Database(self)

    def load_extensions(self) -> None:
        for filename in os.listdir("cogs"):
            try:
                if filename.endswith(".py"):
                    self.load_extension(f"cogs.{filename[:-3]}")
                    print("✅ " + filename)
            except Exception as error:
                print(f"⛔ {filename} | Exception: {error}")
        print("The cogs is finally loaded!")

from disnake.ext import commands
from database import Database


class Linguista(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=","
        )
        self.database = Database(self)

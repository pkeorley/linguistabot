import os

from config import datas
from client import Linguista


bot = Linguista()


for filename in os.listdir("cogs"):
    try:
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    except Exception as error:
        print(error)


bot.run(datas["TOKEN"])

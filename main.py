from config import datas
from client import Linguista


bot = Linguista()
bot.load_extensions()
bot.run(datas["TOKEN"])

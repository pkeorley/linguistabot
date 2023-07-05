from io import BytesIO

import disnake
import psutil
from disnake.ext import commands
import requests

from config import datas
from main import Linguista
from modules.buttons import Images


async def linguista_word_get_word_autocomplete(interaction: disnake.ApplicationCommandInteraction, string: str = None):
    bot: Linguista = interaction.bot
    user = await bot.database.get_user(interaction.author.id)

    emoji = lambda phrase: "✅" if phrase.get("learned") is True else "⛔"
    phrases = list(map(lambda phrase: f"{emoji(phrase)} {phrase['word']}", user["phrases"]))

    filtered_by_string = list(filter(lambda phrase: string in phrase, phrases))

    return sorted(filtered_by_string)


class Commands(commands.Cog):
    def __init__(self, bot: Linguista):
        self.bot = bot

    @commands.slash_command(
        name="linguista",
        description="."
    )
    async def linguista(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            word: str = commands.Param(
                description="."
            )
    ):
        pass

    @linguista.sub_command(
        name="word-add",
        description="Add a new word to your word list"
    )
    async def linguista_word_add(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            word: str = commands.Param(
                min_length=1,
                max_length=128,
                description="Enter the word or phrase you want to add to your word list"
            ),
            image: disnake.Attachment = commands.Param(
                description="Add an image to describe the selected word"
            )
    ):
        await interaction.response.defer()

        if not image.filename.endswith((".png", ".jpg", ".jpeg")):
            return await interaction.edit_original_response(content="It's not a image, try again with image")

        await self.bot.database.push_word(
            interaction.user.id,
            word=word,
            image_url=image.url
        )

        await interaction.edit_original_response(
            content=f"Successfully added a new word `{word}` to the words in your word list",
            file=await image.to_file()
        )

    @linguista.sub_command(
        name="word-get",
        description="Get a word from the word list, can be used to memorise a word"
    )
    async def linguista_word_get(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            word: str = commands.Param(
                description="Select the word you want to receive",
                autocomplete=linguista_word_get_word_autocomplete
            )
    ):
        await interaction.response.defer()

        word = word.lstrip(word.split()[0]).lstrip()
        print(word)
        phrase = await self.bot.database.get_phrase(interaction.author.id, word=word)

        response = requests.get(phrase['image_url'])
        file = disnake.File(fp=BytesIO(response.content), filename=word + ".png")

        word = word.replace("#", "$")
        await interaction.edit_original_response(
            content=f"## {word}",
            file=file
        )

    @linguista.sub_command(
        name="learn",
        description="Word learning mode, use this command if you want to start learning"
    )
    async def linguista_learn(
            self,
            interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer()

        await interaction.edit_original_response(
            content=(
                "You are provided with a pagination tool in which you can flip through the pages.\n"
                "- Click on the tick if you have memorised the word - "
                "it will be transferred to the list of memorised words\n"
                "- Click on the cross if you have not memorised the word yet - it will be repeated in the future"
            ),
            view=Images(self.bot)
        )

    @linguista.sub_command(
        name="word-delete",
        description="Remove a word from your word list"
    )
    async def linguista_word_delete(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            word: str = commands.Param(
                description="The word you want to delete",
                autocomplete=linguista_word_get_word_autocomplete
            )
    ):
        await interaction.response.defer()

        word = word.lstrip(word.split()[0]).lstrip()

        await self.bot.database.pull_word(
            interaction.author.id,
            word=word
        )

        await interaction.edit_original_response(
            content=f"✅ The word `{word}` has been successfully deleted from your word list, I hope you remember it..."
        )

    @commands.slash_command(
        name="bot",
        description="All information about the bot "
    )
    async def client_information(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        application = await self.bot.application_info()

        await interaction.edit_original_response(
            content=(
                "👾 Welcome to the bot help menu! Here you can get all "
                f"the information about the bot `(v{datas['BOT_VERSION']})`\n- "
                "[Official server](https://discord.gg/WDTtfSqSnN) with the "
                f"[bot developer](https://discord.com/users/{application.owner.id})\n"
                f"- [GitHub Repository](https://github.com/pkeorley/linguistabot) with the source code\n{'-' * 50}\n"
                f"- Bot websocket latency: **{round(self.bot.latency * 1000, 2)}ms**\n"
                f"- CPU Usage: **{psutil.cpu_percent()}%**\n"
            )
        )


def setup(bot):
    bot.add_cog(Commands(bot))

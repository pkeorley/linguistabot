from io import BytesIO

import disnake
from disnake.ext import commands
import requests

from main import Linguista


async def linguista_word_get_word_autocomplete(interaction: disnake.ApplicationCommandInteraction, string: str = None):
    bot: Linguista = interaction.bot
    user = await bot.database.get_user(interaction.author.id)
    phrases = list(map(lambda phrase: phrase["word"], user["phrases"]))
    filtered_by_string = list(filter(lambda phrase: string in phrase, phrases))
    return filtered_by_string


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
        name="word-add"
    )
    async def linguista_word_add(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            word: str = commands.Param(
                min_length=1,
                max_length=32,
                description="."
            ),
            image: disnake.Attachment = commands.Param(
                description="."
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
        description="."
    )
    async def linguista_word_get(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            word: str = commands.Param(
                autocomplete=linguista_word_get_word_autocomplete
            )
    ):
        await interaction.response.defer()

        phrase = await self.bot.database.get_phrase(interaction.author.id, word=word)

        response = requests.get(phrase['image_url'])
        file = disnake.File(fp=BytesIO(response.content), filename=word + ".png")

        word = word.replace("#", "$")
        await interaction.edit_original_response(content=f"## {word}", file=file)


def setup(bot):
    bot.add_cog(Commands(bot))

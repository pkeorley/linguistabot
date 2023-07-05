import random
from io import BytesIO

import disnake
import requests

from client import Linguista


class Images(disnake.ui.View):
    def __init__(
            self,
            bot: Linguista
    ):
        super().__init__()
        self.bot = bot
        self._index = -1

    async def update_content(self, interaction: disnake.ApplicationCommandInteraction, phrases: list):
        if not phrases:
            image = random.choice([
                "https://tenor.com/view/i-memorized-it-confused-sarcastic-face-mera-amber-heard-gif-12682550"
            ])
            return await interaction.edit_original_response(
                content=(
                    f"[🎉]({image}) I didn't find a single word that you didn't remember from your word list...\n"
                    "This means that you have memorised all the words on your vocabulary list, congratulations!"
                ),
                view=None
            )

        phrase = phrases[self._index]

        # response = requests.get(phrase['image_url'])
        # file = disnake.File(fp=BytesIO(response.content), filename=phrase["word"] + ".png")

        word = phrase["word"].replace("#", "$")

        await interaction.edit_original_response(
            content=f"## ({self._index + 1:,}/{len(phrases):,}) | [{word}]({phrase['image_url']})",
            # files=[file]
        )

    @disnake.ui.button(
        emoji="⬅️",
        style=disnake.ButtonStyle.blurple
    )
    async def to_left(self, button: disnake.Button, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        phrases = await self.bot.database.get_phrases(interaction.author.id, learned=False)

        if self._index > 0:
            self._index -= 1

        if self._index < 0:
            self._index = 0

        await self.update_content(interaction, phrases)

    @disnake.ui.button(
        emoji="➡️",
        style=disnake.ButtonStyle.blurple
    )
    async def to_right(self, button: disnake.Button, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        phrases = await self.bot.database.get_phrases(interaction.author.id, learned=False)

        if self._index <= len(phrases):
            self._index += 1

        if self._index > len(phrases) - 1:
            self._index = 0

        await self.update_content(interaction, phrases)

    @disnake.ui.button(
        emoji="✅",
        style=disnake.ButtonStyle.green,
        row=1
    )
    async def to_learned(self, button: disnake.Button, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        phrases = await self.bot.database.get_phrases(interaction.author.id, learned=False)
        phrase = phrases[self._index]

        await self.bot.database.set_phrase_status(
            interaction.author.id,
            word=phrase["word"],
            learned=True
        )

        await self.update_content(
            interaction,
            await self.bot.database.get_phrases(interaction.author.id, learned=False)
        )

    @disnake.ui.button(
        emoji="⛔",
        style=disnake.ButtonStyle.red,
        row=1,
        disabled=True
    )
    async def to_later(self, button: disnake.Button, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

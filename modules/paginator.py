from typing import List, Tuple

import disnake


class Paginator(disnake.ui.View):
    default_style = disnake.ButtonStyle.blurple

    def __init__(self, phrases: List[Tuple[str, str]]):
        super().__init__(timeout=60.0)
        self.phrases = phrases
        self.index = 0

    async def edit_page(self, interaction: disnake.ApplicationCommandInteraction, index: int = None):

        if not index:
            index = self.index

        phrase = self.phrases[index]
        await interaction.edit_original_response(content=(
            f"### 📖 {self.index + 1:,}/{len(self.phrases):,}\n"
            f"- {phrase[0]}\n"
            f"- {phrase[1]}"
        ))

    @disnake.ui.button(
        emoji="⏮️",
        style=default_style
    )
    async def switch_to_first_page(self, button: disnake.Button, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()
        await self.edit_page(interaction, index=0)

    @disnake.ui.button(
        emoji="⬅️",
        style=default_style
    )
    async def switch_to_left(self, button: disnake.Button, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        if self.index >= 0:
            self.index -= 1

        await self.edit_page(interaction, index=self.index)

    @disnake.ui.button(
        emoji="➡️",
        style=default_style
    )
    async def switch_to_right(self, button: disnake.Button, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        if self.index <= len(self.phrases) - 1:
            self.index += 1

        await self.edit_page(interaction, index=self.index)

    @disnake.ui.button(
        emoji="⏭️",
        style=default_style
    )
    async def switch_to_last_page(self, button: disnake.Button, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()
        await self.edit_page(interaction, index=len(self.phrases) - 1)

from motor.motor_asyncio import AsyncIOMotorClient

from config import datas


class Database:
    def __init__(self, bot):
        self.bot = bot
        self.cluster = AsyncIOMotorClient(datas["MONGO_URL"])
        self.db = self.cluster.website

    async def push_user(self, user_id: int):
        if not await self.db.word.find_one({"user_id": user_id}):
            await self.db.word.insert_one({
                "user_id": user_id,
                "phrases": []
            })

    async def push_word(self, user_id: int, word: str, image_url: str) -> None:
        await self.push_user(user_id)
        await self.db.word.update_one({
            "user_id": user_id,
        }, {
            "$push": {
                "phrases": {
                    "word": word,
                    "image_url": image_url
                }
            }
        })

    async def pull_word(self, user_id: int, word: str) -> None:
        user = await self.get_user(user_id)
        phrases: list = user["phrases"]

        for phrase in phrases:
            if phrase["word"] == word:
                index = phrases.index(phrase)
                del phrases[index]
                break

        await self.db.word.update_one({
            "user_id": user_id
        }, {
            "$set": {
                "phrases": phrases
            }
        })

    async def get_user(self, user_id: int):
        await self.push_user(user_id)
        return await self.db.word.find_one({"user_id": user_id})

    async def get_phrase(self, user_id: int, word: str):
        phrases = await self.get_phrases(user_id)

        for phrase in phrases:
            if phrase["word"] == word:
                return phrase

    async def get_phrases(self, user_id: int, learned: bool = False):
        user = await self.get_user(user_id)
        return list(filter(lambda phrase: user.get("learned", False) == learned, user["phrases"]))

    async def set_phrase_status(self, user_id: int, word: str, learned: bool):
        await self.push_user(user_id)

        user = await self.get_user(user_id)
        phrases: list = user["phrases"]

        for phrase in phrases:
            if phrase["word"] == word:
                index = phrases.index(phrase)
                phrases[index]["learned"] = learned

        await self.db.word.update_one({
            "user_id": user_id
        }, {
            "$set": {
                "phrases": phrases
            }
        })



from ast import literal_eval
from asyncio import sleep
from os import getenv

import disnake
from disnake.ext import commands


class MessageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.authors = literal_eval(getenv("FILTER_AUTHORS"))
        self.prefixes = literal_eval(getenv("FILTER_PREFIXES"))
        self.channels = literal_eval(getenv("FILTER_CHANNELS"))
        self.toggle = literal_eval(getenv("FILTER_TOGGLE"))
        self.seconds = literal_eval(getenv("FILTER_SECONDS"))
        self.whitelist = literal_eval(getenv("FILTER_WHITELIST_MESSAGES"))

        if self.toggle is False:
            self.bot.remove_listener(self.on_message)

    def parse_message_content(self, msg: disnake.Message) -> str:
        embed = msg.embeds

        if embed:
            embed = embed[0].to_dict()
            cont = msg.content, embed.get("title", ""), embed.get("description", "")
        else:
            cont = [msg.content]

        return "\n".join(map(str.lower, cont))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id in self.channels:
            if any(
                cont.lower() in self.parse_message_content(msg)
                for cont in self.whitelist
            ):
                return

            if msg.author.id in self.authors:
                await sleep(self.seconds)
                await msg.delete()
            if msg.content.startswith(self.prefixes):
                await msg.delete()

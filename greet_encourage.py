import discord
from discord.ext import commands
from replit import db


class greet_encourage(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def kappa(self, ctx, *, member: discord.Member = None):
        print(123)
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send(
                'Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member


def setup(client):
    client.add_cog(greet_encourage(client))

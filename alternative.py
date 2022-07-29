import discord
from discord.ext import commands

client = commands.Bot(command_prefix='?')


@client.command()
async def foo(ctx, arg):
    await ctx.send(arg)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


client.run(
    'MTAwMjM0MzAwMjUxOTM3OTk2OA.GuhAk1.HdPOG_6lMNxuM4iwjuC4sUqiWygAdulUSv5mTQ')

import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='?', intents=intents)
client.load_extension("greet_encourage")

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing", "hate",
    "dejected", "despair", "despairing", "not feeling good"
]
greetings = [
    "hello", "hi", "hola", "hey", "sup", "greetings", "good morning",
    "welcome", "howdy", "bonjour"
]

commanders = ["add", "delete", "quote", "customlist", "ban", "unban"]

starter_encouragements = [
    "Don't worry, I'm here UWU", "Hang in there Goshujin Sama",
    "Never fear, Elaina is here!"
]
starter_greetings = [
    "Hello, my name is Elaina", "Greetings traveller, tis I, Elaina", "Hi!"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


@client.command()
async def roll(ctx):
    await ctx.send("I will do so at once Master")


@client.command()
async def quote(ctx):
    print(ctx.guild.id)
    quote = get_quote()
    await ctx.send(quote)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send("BANNED")


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@unban.error
async def unban_error(ctx, error):
    proceed = False
    if isinstance(error, commands.CommandInvokeError): proceed = True
    if isinstance(error, commands.MissingRequiredArgument): proceed = True
    if (proceed):
        await ctx.send('Must specify a discord user')


@client.command()
async def responding(ctx, *boolean):
    if (len(boolean) == 0):
        await ctx.send("No argument")
        return
    if (len(boolean) > 1):
        await ctx.send("Argument invalid")
        return
    b = boolean[0].lower()
    if b == "true":
        db["responding"] = True
        await ctx.send("Message reponding is ON")
    elif b == "false":
        db["responding"] = False
        await ctx.send("Message responding is OFF")
    else:
        await ctx.send("Argument invalid")


@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user:
        return
    if db["responding"] and msg.startswith("?") and not any(
            word in msg for word in commanders):
        if any(word in msg for word in greetings):
            options = starter_greetings
            if "greetings" in db.keys():
                options = options + db["greetings"].value
            await message.channel.send(random.choice(options))
            return
        if any(word in msg for word in sad_words):
            options = starter_encouragements
            if "encouragements" in db.keys():
                options = options + db["encouragements"].value
            await message.channel.send(random.choice(options))
            return
    await client.process_commands(message)


keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)

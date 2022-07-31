import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands
import youtube_dl

client = commands.Bot(command_prefix='?')
client.load_extension("greet_encourage")

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing", "hate",
    "dejected", "despair", "despairing", "not feeling good"
]
greetings = [
    "hello", "hi", "hola", "hey", "sup", "greetings", "good morning",
    "welcome", "howdy", "bonjour"
]

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


def update_lists(message_type, message):
    if message_type.lower() in db.keys():
        tempList = db[message_type.lower()].value
        tempList.append(message)
        db[message_type] = tempList
    else:
        db[message_type] = [message]


def delete_list_elements(message_type, index):
    messages = db[message_type]
    if len(messages) > index:
        del messages[index]
    db[message_type] = messages


def check_message_add(message_type, msg):
    new_message = msg.split("?add " + message_type + " ", 1)[1]
    update_lists(message_type, new_message)


def check_message_delete(message_type, msg):
    if len(msg) < 8:
        return "Please specify delete type"
    messages = []
    index = int(msg.split("?delete " + message_type + " ", 1)[1])
    delete_list_elements(message_type, index)
    messages = db[message_type]
    return messages


def return_list(message_type):
    if message_type in db.keys():
        list = db[message_type]
        return list


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


@client.command()
async def add(ctx, args):
    proceed = False
    if args == "encouragements": proceed = True
    if args == "greetings": proceed = True
    if proceed:
        check_message_add(args, ctx.message.content)
        await ctx.send("New message added")


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('No argument added!')


@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    if msg.startswith("?delete encouragements"):
        await message.channel.send(
            list(check_message_delete(
                "encouragements",
                msg,
            )))
        return
    if msg.startswith("?delete greetings"):
        await message.channel.send(
            list(check_message_delete(
                "greetings",
                msg,
            )))
        return
    if msg.startswith("?customlist encouragements"):
        await message.channel.send(list(return_list("encouragements")))
        return
    if msg.startswith("?customlist greetings"):
        await message.channel.send(list(return_list("greetings")))
        return
    if msg.startswith("?responding "):
        value = msg.split("?responding ", 1)[1]
        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on")
            return
        elif value.lower() == "false":
            db["responding"] = False
            await message.channel.send("Responding is off")
            return
    if db["responding"] and msg.startswith("?"):
        msg = msg.lower()
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

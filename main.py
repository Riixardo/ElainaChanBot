import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

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
    if msg.startswith("?add " + message_type):
        new_message = msg.split("?add " + message_type + " ", 1)[1]
        update_lists(message_type, new_message)
        return True


def check_message_delete(message_type, msg):
    messages = []
    if msg.startswith("?delete " + message_type):
        index = int(msg.split("?delete " + message_type + " ", 1)[1])
        delete_list_elements(message_type, index)
        messages = db[message_type]
        return messages


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    if msg.startswith('?hello'):
        quote = get_quote()
        await message.channel.send(quote)
        return
    if (check_message_add("encouragements", msg)):
        await message.channel.send("New message added.")
        return
    if (check_message_add("greetings", msg)):
        await message.channel.send("New message added.")
        return
    if msg.startswith("?delete encouragements"):
        await message.channel.send(
            check_message_delete(
                "encouragements",
                msg,
            ))
        return
    if msg.startswith("?delete greetings"):
        await message.channel.send(check_message_delete(
            "greetings",
            msg,
        ))
        return

    if msg.startswith("?list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)
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
            if "greetings" in db.keys():
                options = starter_greetings
                options = options + db["greetings"].value
                await message.channel.send(random.choice(options))
                return
        if any(word in msg for word in sad_words):
            if "encouragements" in db.keys():
                options = starter_encouragements
                options = options + db["encouragements"].value
                await message.channel.send(random.choice(options))
                return


keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)

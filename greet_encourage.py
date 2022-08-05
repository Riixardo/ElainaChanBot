import discord
from discord.ext import commands
from replit import db


class greet_encourage(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self._last_member = None

    def check_message_add(self, message_type, msg):
        new_message = msg.split("?add " + message_type + " ", 1)[1]
        self.update_lists(message_type, new_message)

    def update_lists(self, message_type, message):
        if message_type.lower() in db.keys():
            tempList = db[message_type.lower()].value
            tempList.append(message)
            db[message_type] = tempList
        else:
            db[message_type] = [message]

    def delete_list_elements(self, message_type, index):
        index_in_range = False
        messages = db[message_type]
        if len(messages) > index:
            del messages[index]
            index_in_range = True
        db[message_type] = messages
        return index_in_range

    def check_message_delete(self, message_type, msg):
        messages = []
        index_in_range = False
        try:
            index = int(msg.split("?delete " + message_type + " ", 1)[1])
        except:
            return (messages, index_in_range)
        if (self.delete_list_elements(message_type, index)):
            index_in_range = True
        else:
            index_in_range = False
        messages = db[message_type]
        return (messages, index_in_range)

    def return_list(self, message_type):
        if message_type in db.keys():
            list = db[message_type]
            return list

    @commands.Cog.listener()
    async def on_member_join(ctx, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(
                'Greetings {0.mention}. I Elaina, the greatest witch ever, welcome you to this server! '
                .format(member))

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

    @commands.command()
    async def add(self, ctx, *args):
        proceed = False
        if len(args) == 0 or len(args) == 1:
            await ctx.send("No argument(s)!")
            return
        if args[0] == "encouragements": proceed = True
        if args[0] == "greetings": proceed = True
        if proceed:
            self.check_message_add(args[0], ctx.message.content)
            await ctx.send("New message added")
        else:
            await ctx.send("Invalid argument")

    @commands.command()
    async def delete(self, ctx, *args):
        if args == ():
            await ctx.send("No argument!")
            return
        proceed = False
        if args[0] == "encouragements": proceed = True
        if args[0] == "greetings": proceed = True
        if (not proceed):
            await ctx.send("Invalid argument")
            return
        if len(args) == 1:
            await ctx.send("No index provided")
            return
        if proceed:
            result = self.check_message_delete(args[0], ctx.message.content)
            if (result[1] is True):
                await ctx.send(list(result[0]))
            else:
                await ctx.send("Index not in range")
        else:
            ctx.send("Invalid argument")

    @commands.command()
    async def customlist(self, ctx, *args):
        if args == ():
            await ctx.send("No argument!")
            return
        if (len(args) > 1):
            await ctx.send("Invalid argument")
            return
        proceed = False
        if args[0] == "encouragements": proceed = True
        if args[0] == "greetings": proceed = True
        if proceed:
            await ctx.send(list(self.return_list(args[0])))
        else:
            await ctx.send("Invalid argument")


def setup(client):
    client.add_cog(greet_encourage(client))

import discord
from discord.ext import commands
import re
from discord.utils import get

from env import TOKEN

test_guild = 893145160207179866
member_role = 893551265043345429

# Create connection to discord

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# When someone enter the discord, send him a message
@bot.event
async def on_member_join(member):
    print('someone joined!')
    await member.send('Hello there!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    s = message.content.strip()
    r = r'[a-z]*.[a-z]*@epfl.ch'

    # TODO: check if already member
    response = ''
    if re.match(r, s):
        response = 'Perfect!\n'
        response += f'I\'m sending a verification code to this email: *{s}*\n\n'
        response += 'Send me that code to get the member role ;)'

        guild = bot.get_guild(test_guild)
        role = get(guild.roles, id=member_role)
        print(guild.members)
        member = guild.get_member(message.author.id)
        member.add_roles(role)
    else:
        response = "If you want to become a member of polygl0ts, send me you epfl email address."

    # TODO: generate code, send and verify it



    await message.channel.send(response)

bot.run(TOKEN)

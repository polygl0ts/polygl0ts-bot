import discord
from discord.ext import commands
import re
from discord.utils import get

import config


# Create bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Connect bot
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# When someone enters the discord, send him a message
@bot.event
async def on_member_join(member):
    print('someone joined!')
    await member.send('Hello there!')

# Helper to add member role
async def add_member_role(bot, user_id):
    guild = bot.get_guild(config.user_verification.guild_id)
    member = await(guild.fetch_member(user_id))
    await member.add_roles([r for r in guild.roles if r.name == config.user_verification.role][0])

# Verify command
@bot.command()
async def verify(ctx, checksum : str):
    # if captcha.validate_answer(ctx.author.id, checksum):
    await ctx.send("That looks correct.\nCome on in!")
    await add_member_role(ctx.bot, ctx.author.id)
    # else:
    #     await ctx.send("That doesn't look correct.\n" + captcha.get_instructions(ctx.author.id))

if __name__ == "__main__":
    # api.run_api(bot)
    bot.run(config.discord.token)



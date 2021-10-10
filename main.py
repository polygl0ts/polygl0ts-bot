import discord
import discord_slash
from discord.ext import commands
from discord.utils import get

import re

import config, captcha

# Create bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Connect bot
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

# When someone enters the discord, send him a message
@bot.event
async def on_member_join(member):
    print("someone joined!")
    await member.send("Hello there!")

# Helper to add member role
async def add_member_role(bot, user_id):
    guild = bot.get_guild(config.user_verification.guild_id)
    member = await (guild.fetch_member(user_id))
    await member.add_roles(
        [r for r in guild.roles if r.name == config.user_verification.role][0]
    )

@bot.command()
async def email(ctx, email : str):
    r = r'[a-z]*.[a-z]*@epfl.ch'
    if re.match(r, email):
        code = captcha.generate_captcha(ctx.author.id)
        await ctx.send(f'Here is your verification code: {code}')
    else:
        await ctx.send('This doesn\'t look like an EPFL email address to me...')

@bot.command()
async def verify(ctx, code: str):
    if captcha.validate_captcha(ctx.author.id, code):
        await ctx.send('Such member, much wow!')
        await add_member_role(ctx.bot, ctx.author.id)
    else:
        await ctx.send('Sorry, it looks like your code is invalid/expired.')


if __name__ == "__main__":
    bot.run(config.discord.token)


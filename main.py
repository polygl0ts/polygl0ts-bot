import discord
import discord_slash
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord.utils import get

import re
import typing

import config, captcha

# Create bot
intents = discord.Intents.default()
#intents.members = True
bot = discord.Client(intents=intents)
slash = discord_slash.SlashCommand(bot, sync_commands=True)

# Connect bot
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

# When someone enters the discord, send him a message
@bot.event
async def on_member_join(member):
    print("someone joined!")
    await member.send("Hello there!")

@slash.slash(name="ping", description="Just a test, sleeps for 5 seconds then replies with 'pong'", guild_ids=[config.user_verification.guild_id])
async def ping(ctx: discord_slash.SlashContext):
    await ctx.defer()
    await asyncio.sleep(5)
    await ctx.send("Pong!")

# Helper to add member role
async def add_member_role(bot, user_id):
    guild = bot.get_guild(config.user_verification.guild_id)
    member = await (guild.fetch_member(user_id))
    await member.add_roles(
        [r for r in guild.roles if r.name == config.user_verification.role][0]
    )

@slash.slash(name="send_code",
             description="Send a verification code by email",
             guild_ids=[config.user_verification.guild_id],
             options=[
                 create_option(name="email",
                    description="Your EPFL email address",
                    option_type=SlashCommandOptionType.STRING,
                    required=True)
                ]
             )
async def send_verification_code(ctx: discord_slash.SlashContext, email: typing.Optional[str] = None):
    r = r'[a-z]*.[a-z]*@epfl.ch'
    if re.match(r, email):
        code = captcha.generate_captcha(ctx.author.id)
        await ctx.send(f'Here is your verifcation code: {code}')
    else:
        await ctx.send('This doesn\'t look like an EPFL email address to me...')

@slash.slash(name="verify_code",
             description="Verify code and assign member role",
             guild_ids=[config.user_verification.guild_id],
             options=[
                 create_option(name="code",
                    description="Your verification code",
                    option_type=SlashCommandOptionType.STRING,
                    required=True)
                ]
             )
async def verify(ctx: discord_slash.SlashContext, code: typing.Optional[str] = None):
    if captcha.validate_captcha(ctx.author.id, code):
        await ctx.send("Such member, much wow!")
        await add_member_role(ctx.bot, ctx.author.id)
    else:
        await ctx.send('Sorry, it looks like your code is invalid/expired.')


if __name__ == "__main__":
    bot.run(config.discord.token)


import discord
import re
import requests
from discord.ext import commands

import config, captcha, constants, spam

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

# ==================
# Helpers
# ==================


async def add_member_role(bot, user_id):
    guild = bot.get_guild(config.user_verification.guild_id)
    member = await (guild.fetch_member(user_id))
    await member.add_roles(
        [r for r in guild.roles if r.name == config.user_verification.role][0]
    )

async def member_log(bot, text):
    channel = bot.get_channel(config.user_verification.log_channel_id)
    await channel.send(text)


# ==================
# Events handling
# ==================


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_member_join(member):
    await member.send(constants.help_message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(constants.help_message)
    else:
        welpwuat = requests.get("http://whatthecommit.com/index.txt").text.strip()
        await ctx.send(welpwuat)


# ==================
# Commands
# ==================


@bot.command()
async def help(ctx):
    await ctx.send(constants.help_message)


@bot.command()
async def email(ctx, email: str):
    r = r"[a-z]*.[a-z]*@epfl.ch"
    if re.match(r, email):
        code = captcha.generate_captcha(ctx.author.id)
        # Send the verification code via email
        if spam.send_mail(email, code):
            await ctx.send("Check your email inbox for the verification code!")
            await member_log(ctx.bot, f'{ctx.author.mention} required a verification code.')
        else:
            await ctx.send(
                "Sending the email failed. Are you sure your mail address is correct?"
            )
    else:
        await ctx.send("This doesn't look like an EPFL email address to me...")


@bot.command()
async def verify(ctx, code: str):
    if captcha.validate_captcha(ctx.author.id, code):
        await ctx.send("Such member, much wow!")
        await add_member_role(ctx.bot, ctx.author.id)
        await member_log(ctx.bot, f'{ctx.author.mention} validated is verification code.')
    else:
        await ctx.send("Sorry, it looks like your code is invalid/expired.")
        await member_log(ctx.bot, f'{ctx.author.mention} invalid code.')


if __name__ == "__main__":
    bot.run(config.discord.token)

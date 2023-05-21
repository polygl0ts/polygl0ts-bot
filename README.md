# polybot

This is the polybot - the Discord bot for the [polygl0ts Discord server](https://discord.gg/pjm7Mr6kUt)!

It is very powerful.
Never mess with our bot!
(And if you do, please follow responsible disclosure principles!)

## Running the bot

You can just call `python3 main.py` after you've installed the requirements via `pipenv install` and entered the virtual
environment via `pipenv shell`.

However, we suggest using the provided Dockerfile for a reproducible build and runtime environment.
Just call `docker compose build` and `docker compose up` and you're ready to go!
Don't forget to create a `config.json`, though.
The provided example file can act as a reference!

## Available commands

You're supposed to communicate with the bot via DMs for getting the member role on our server.
Whenever you're stuck, text `!help` to the bot and he'll let you know what to do :)

## Attributions and license

Thx to the guys from CryptoHack for the inspiration (inspiration meaning code snippet copy-pasting) from their
[cryptohacker bot](https://github.com/cryptohack/cryptohacker-discord-bot)!

Our own bot is licensed under the MIT license.
For more info, check the [license file](./LICENSE).

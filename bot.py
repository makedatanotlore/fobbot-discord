import discord
import random
import dice
import re
import os
from discord import Game, Message
from discord.ext.commands import Bot

TOKEN = os.environ['token']
BOT_PREFIX = os.environ['prefix']

client = Bot(command_prefix=BOT_PREFIX)
REGEX = {re.compile('(\d+)(ba|ge)'): dice.Base,
         re.compile('(\d+)(sk|fv)'): dice.Skill,
         re.compile('(\d+)(gr|rd)'): dice.Gear,
         re.compile('(\d+)(d8|t8)'): dice.D8,
         re.compile('(\d+)(d10|t10)'): dice.D10,
         re.compile('(\d+)(d12|t12)'): dice.D12}


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=Game(name='>hjälp / >help'))


@client.command(name='slå',
                aliases=['roll', 'fbl'],
                pass_context=True)
async def roll(context):
    if context.message.author.bot:
        return

    author_roles = [role.name.lower() for role in context.message.author.roles]
    pushes = 10 if 'dvärg' in author_roles or 'dwarf' in author_roles else 1

    dicepool = await parse_args(context)

    if not dicepool:
        embed = discord.Embed(title='<:ss_bane:546280456828485632>',
                              color=0xe60000)
        await context.message.channel.send(embed=embed)
        return

    for die in dicepool:
            await die.roll()

    embed = await embed_template(context, dicepool)
    message = await context.message.channel.send(embed=embed)

    while pushes > 0:
        if [die for die in dicepool if await die.pushable()]:
            await Message.add_reaction(message, '🔄')

            await client.wait_for('reaction_add',
                                  timeout=600.0,
                                  check=lambda reaction, user: str(reaction.emoji) == '🔄' and user == context.message.author)

            for die in dicepool:
                await die.roll()

            embed = await embed_template(context, dicepool)

            await Message.clear_reactions(message)
            await Message.edit(message, embed=embed)

            pushes -= 1
        else:
            return


@client.command(name='stop',
                pass_context=True)
async def stop(context):
    if context.message.author.bot:
        return
    await client.close()


async def embed_template(context, dicepool):
    embed = discord.Embed(title=' ',
                          color=context.message.author.color,
                          description=''.join([die.active.emoji for die in dicepool]))
    embed.set_author(name=context.message.author.display_name,
                     icon_url=context.message.author.avatar_url)

    return embed


async def parse_args(context):
    hand = []

    for regex, die in REGEX.items():
        result = regex.search(context.message.content.lower())
        if result is not None:
            hand += [die() for i in range(int(result.group(1)))]

    random.shuffle(hand)

    return hand

client.run(TOKEN)

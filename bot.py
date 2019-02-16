import asyncio

import discord
import random
import dice
import re
import os
from discord import Game, Message
from discord.ext.commands import Bot

TOKEN = os.environ.get('token')
BOT_PREFIX = os.environ.get('prefix')

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

REGEX = {re.compile('(\d+)(d6|t6)'): dice.D6,
         re.compile('(\d+)(ba|ge)'): dice.Base,
         re.compile('(\d+)(sk|fv)'): dice.Skill,
         re.compile('(\d+)(gr|rd|vp|wp)'): dice.Gear,
         re.compile('(\d+)(d8|t8)'): dice.D8,
         re.compile('(\d+)(d10|t10)'): dice.D10,
         re.compile('(\d+)(d12|t12)'): dice.D12,
         re.compile('(\d+)(resource ?d6|resurs ?t6)'): dice.ResourceD6,
         re.compile('(\d+)(resource ?d8|resurs ?t8)'): dice.ResourceD8,
         re.compile('(\d+)(resource ?d10|resurs ?t10)'): dice.ResourceD10,
         re.compile('(\d+)(resource ?d12|resurs ?t12)'): dice.ResourceD12}


@client.event
async def on_ready():
    await client.change_presence(activity=Game(name='>hjälp / >help'))


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

    embed = await embed_template(context)
    message = await context.message.channel.send(''.join([die.active.emoji for die in dicepool]), embed=embed)

    while pushes > 0:
        if [die for die in dicepool if await die.pushable()]:
            await Message.add_reaction(message, '🔄')

            try:
                await client.wait_for('reaction_add', timeout=60.0,
                                      check=lambda reaction, user: str(reaction.emoji) == '🔄' and user == context.message.author and reaction.message.id == message.id)
            except asyncio.TimeoutError:
                await Message.clear_reactions(message)
                return

            for die in dicepool:
                await die.roll()

            embed = await embed_template(context)

            await Message.clear_reactions(message)
            await Message.edit(message, content=''.join([die.active.emoji for die in dicepool]), embed=embed)

            pushes -= 1
        else:
            return


@client.command(name='hjälp',
                pass_context=True)
async def swedish_help(context):
    if context.message.author.bot:
        return

    embed = discord.Embed(title='Hjälp - Slå tärning',
                          color=0xa2e600,
                          description='För att slå tärning, ange antalet tärningar följt av tärningstypen.')
    embed.add_field(name='Exempel',
                    value='`>slå 5ge 2fv 2rd 1t8`',
                    inline=False)
    embed.add_field(name='Tärningstyper',
                    value=f'Vanlig T6 - `t6`\n'
                    f'Grundegenskapstärning - `ge`\n'
                    f'Färdighetstärning - `fv`\n'
                    f'Redskaps/vapentärning - `rd/vp`\n'
                    f'Artefakttärning T8 - `t8`\n'
                    f'Artefakttärning T10 - `t10`\n'
                    f'Artefakttärning T12 - `t12`',
                    inline=False)

    await context.message.channel.send(embed=embed)


@client.command(name='help',
                pass_context=True)
async def english_help(context):
    if context.message.author.bot:
        return

    embed = discord.Embed(title='Help - Rolling the dice',
                          color=0xa2e600,
                          description='To roll the dice, enter the number of dice followed by the type.')
    embed.add_field(name='Example usage',
                    value='`>roll 5ba 2sk 2gr 1d8`',
                    inline=False)
    embed.add_field(name='Types of dice',
                    value=f'Regular D6 - `d6`\n'
                    f'Base Attribute Die - `ba`\n'
                    f'Skill Die - `sk`\n'
                    f'Gear/Weapon Die - `gr/wp`\n'
                    f'Artifact D8 - `d8`\n'
                    f'Artifact D10 - `d10`\n'
                    f'Artifact D12 - `d12`',
                    inline=False)

    await context.message.channel.send(embed=embed)


async def embed_template(context):
    embed = discord.Embed(title=' ',
                          color=context.message.author.color)
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

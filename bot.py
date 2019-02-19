import asyncio

import discord
import random
import dice
import re
import os
import datetime
from discord import Game, Message
from discord.ext.commands import Bot

TOKEN = os.environ.get('token')
BOT_PREFIX = os.environ.get('prefix')

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

ROLL_NAME_REGEX = re.compile(' \"(.+)\"(?![a-zA-Z\d])')
REGEX = {re.compile(' (\d+)(d6|t6)(?![a-zA-Z\d])'): dice.D6,
         re.compile(' (\d+)(ba|ge)(?![a-zA-Z\d])'): dice.Base,
         re.compile(' (\d+)(sk|fv)(?![a-zA-Z\d])'): dice.Skill,
         re.compile(' (\d+)(gr|rd|vp|wp)(?![a-zA-Z\d])'): dice.Gear,
         re.compile(' (\d+)(d8|t8)(?![a-zA-Z\d])'): dice.D8,
         re.compile(' (\d+)(d10|t10)(?![a-zA-Z\d])'): dice.D10,
         re.compile(' (\d+)(d12|t12)(?![a-zA-Z\d])'): dice.D12,
         re.compile(' (\d+)res(d6|t6)(?![a-zA-Z\d])'): dice.ResourceD6,
         re.compile(' (\d+)res(d8|t8)(?![a-zA-Z\d])'): dice.ResourceD8,
         re.compile(' (\d+)res(d10|t10)(?![a-zA-Z\d])'): dice.ResourceD10,
         re.compile(' (\d+)res(d12|t12)(?![a-zA-Z\d])'): dice.ResourceD12}


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
        embed = discord.Embed(title='I am Error',
                              description='<No valid arguments found>',
                              color=0xe60000)
        await context.message.channel.send(embed=embed)
        return

    for die in dicepool:
            await die.roll()

    roll_name = ROLL_NAME_REGEX.search(context.message.content.lower())
    title = roll_name.group(1).capitalize() if roll_name is not None else ' ' \
                                                                          ''
    roll_count = 1
    embed = await embed_template(context, dicepool, roll_count, title=title)
    message = await context.message.channel.send('\n'.join(''.join([die.active.emoji for die in chunk]) for chunk in list(divide_chunks(dicepool, 6))), embed=embed)

    while pushes > 0:
        if [die for die in dicepool if await die.pushable()]:
            await Message.add_reaction(message, '🔄')

            try:
                await client.wait_for('reaction_add', timeout=600.0,
                                      check=lambda reaction, user: str(reaction.emoji) == '🔄' and user == context.message.author and reaction.message.id == message.id)
            except asyncio.TimeoutError:
                await Message.clear_reactions(message)
                return

            roll_count += 1
            for die in dicepool:
                await die.roll()

            embed = await embed_template(context, dicepool, roll_count, title=title)

            await Message.clear_reactions(message)
            await Message.edit(message, content='\n'.join(''.join([die.active.emoji for die in chunk]) for chunk in list(divide_chunks(dicepool, 6))), embed=embed)

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
                          description='För att slå tärning, ange antalet tärningar följt av tärningstypen. Tryck på 🔄 för att pressa slaget.')
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
    embed.add_field(name='Resurstärningar (<:ss_bane:546280456828485632> - 1/2)',
                    value=f'Resurstärning T6 - `rest6`\n'
                    f'Resurstärning T8 - `rest8`\n'
                    f'Resurstärning T10 - `rest10`\n'
                    f'Resurstärning T12 - `rest12`\n',
                    inline=True)

    await context.message.channel.send(embed=embed)


@client.command(name='help',
                pass_context=True)
async def english_help(context):
    if context.message.author.bot:
        return

    embed = discord.Embed(title='Help - Rolling the dice',
                          color=0xa2e600,
                          description='To roll dice, enter the number of dice followed by the type. Click 🔄 to push.')
    embed.add_field(name='Example usage',
                    value='`>roll 5ba 2sk 2gr 1d8`',
                    inline=False)
    embed.add_field(name='Dice',
                    value=f'Regular D6 - `d6`\n'
                    f'Base Attribute Die - `ba`\n'
                    f'Skill Die - `sk`\n'
                    f'Gear/Weapon Die - `gr/wp`\n'
                    f'Artifact Die D8 - `d8`\n'
                    f'Artifact Die D10 - `d10`\n'
                    f'Artifact Die D12 - `d12`',
                    inline=False)
    embed.add_field(name='Resource Dice (<:ss_bane:546280456828485632> - 1/2)',
                    value=f'Resource Die D6 - `resd6`\n'
                    f'Resource Die D8 - `resd8`\n'
                    f'Resource Die D10 - `resd10`\n'
                    f'Resource Die D12 - `resd12`\n',
                    inline=False)

    await context.message.channel.send(embed=embed)


async def embed_template(context, dicepool, roll_count, title=' '):
    countable = [die for die in dicepool if die.countable]

    if countable:
        swords = sum([die.active.swords for die in dicepool if die.countable])
        skulls = sum([die.active.skulls for die in dicepool if die.countable])
        embed = discord.Embed(
            title=title,
            description=f'**\#{roll_count}:** {swords} x<:grey_swords:547454438021791745>{skulls} x<:grey_skull:547454438873366528>',
            color=context.message.author.color,
            timestamp=context.message.edited_at if context.message.edited_at is datetime.datetime else context.message.created_at)
    else:
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


# divides list into chunks
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


client.run(TOKEN)

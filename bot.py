import asyncio

import discord
import random
import dice
import re
import os
from collections import namedtuple
from discord import Game, Message
from discord.ext.commands import Bot

TOKEN = os.environ.get('token')
TEST_TOKEN = os.environ.get('test_token')
BOT_PREFIX = os.environ.get('prefix')

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

GRITTERS = ['dvärg', 'dwarf', 'dvergar']
ACTUAL_NUMBERS_REGEX = re.compile(' -an(?![a-zA-Z\d])')
NO_SHUFFLE_REGEX = re.compile(' -ns(?![a-zA-Z\d])')
ROLL_NAME_REGEX = re.compile(' \"(.+)\"(?![a-zA-Z\d])')
REGEX = {re.compile(' (\d+|)(d6|t6)(?![a-zA-Z\d])'): dice.D6,
         re.compile(' (\d+|)(ba|ge)(?![a-zA-Z\d])'): dice.Base,
         re.compile(' (\d+|)(sk|fv)(?![a-zA-Z\d])'): dice.Skill,
         re.compile(' (\d+|)(gr|rd|vp|wp)(?![a-zA-Z\d])'): dice.Gear,
         re.compile(' (\d+|)(d8|t8)(?![a-zA-Z\d])'): dice.D8,
         re.compile(' (\d+|)(d10|t10)(?![a-zA-Z\d])'): dice.D10,
         re.compile(' (\d+|)(d12|t12)(?![a-zA-Z\d])'): dice.D12,
         re.compile(' (\d+|)res(d6|t6)(?![a-zA-Z\d])'): dice.ResourceD6,
         re.compile(' (\d+|)res(d8|t8)(?![a-zA-Z\d])'): dice.ResourceD8,
         re.compile(' (\d+|)res(d10|t10)(?![a-zA-Z\d])'): dice.ResourceD10,
         re.compile(' (\d+|)res(d12|t12)(?![a-zA-Z\d])'): dice.ResourceD12,
         re.compile(' (\d+|)(nv|nt|tv)(?![a-zA-Z\d])'): dice.Negative,
         re.compile(' (\d+|)(tl|vk)(?![a-zA-Z\d])'): dice.TalesFromTheLoopD6}

Roll = namedtuple('Roll', 'guild user dicepool')

roll_log = []


@client.event
async def on_ready():
    print('='*36)
    print(f'CONNECTED TO {len(client.guilds)} SERVERS WITH {len(client.users)} USERS')
    print('SERVERS:')
    for guild in client.guilds:
        print(f'{str.upper(guild.name)} WITH {len(guild.members)} MEMBERS')
    print('=' * 36)
    await client.change_presence(activity=Game(name=f'>help on {len(client.guilds)} servers'))


@client.event
async def on_disconnect():
    print('='*36)
    print(f'SESSION DISCONNECTED - AFTER {len(roll_log)} ROLLS')
    for roll in roll_log:
        print(f'{roll.guild} - {roll.user} - {[die.current.name for die in roll.dicepool]}')


@client.command(name='slå',
                aliases=['roll', 'fbl'],
                pass_context=True)
async def roll(context):
    if context.message.author.bot:
        return

    author_roles = [role.name.lower() for role in context.message.author.roles]
    grit = [role for role in author_roles if role in GRITTERS]
    pushes = 11 if grit else 1

    dicepool = await parse_args(context)

    if not dicepool:
        embed = discord.Embed(title='I am Error',
                              description='<No valid arguments found>',
                              color=0xe60000)
        await context.message.channel.send(embed=embed)
        return

    for die in dicepool:
            await die.roll()
    roll_log.append(Roll(context.message.guild.name, context.message.author.display_name, dicepool))

    roll_name = ROLL_NAME_REGEX.search(context.message.content)
    title = roll_name.group(1) if roll_name is not None else ' '

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
            roll_log.append(Roll(context.message.guild.name, context.message.author.display_name, dicepool))

            embed = await embed_template(context, dicepool, roll_count, title=title)

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
                    value='`>slå 5ge 2fv 2rd t8`',
                    inline=False)
    embed.add_field(name='Tärningstyper',
                    value=f'Grundegenskapstärning - `ge`\n'
                    f'Färdighetstärning - `fv`\n'
                    f'Redskaps/vapentärning - `rd/vp`\n'
                    f'Artefakttärning T8 - `t8`\n'
                    f'Artefakttärning T10 - `t10`\n'
                    f'Artefakttärning T12 - `t12`',
                    inline=False)
    embed.add_field(name='Resurstärningar',
                    value='När du behöver slå för en resurs.<:grey_skull:547454438873366528> betyder att resursen förbrukats.\n'
                    f'Resurstärning T6 - `rest6`\n'
                    f'Resurstärning T8 - `rest8`\n'
                    f'Resurstärning T10 - `rest10`\n'
                    f'Resurstärning T12 - `rest12`\n',
                    inline=False)
    embed.add_field(name='Negativa tärningar/tvärtomtärningar',
                    value='När du har en negativ modifikation på slaget.\n'
                    f'Negativ T6 - `nt/tv`\n',
                    inline=False)
    embed.add_field(name='Numrerade tärningar',
                    value='När du behöver en siffra på tärningen.\n'
                    '(Lägg till flaggan `-an` om du vill se de faktiska siffrorna som slogs fram.)\n'
                    f'Vanlig T6 - `t6`\n',
                    inline=False)
    embed.add_field(name='Anteckningar',
                    value='När du behöver en anteckning på slaget, använd "".\n'
                    f'`>slå 2rest8 "Mat/Vatten -ns"`\n'
                    f'(här används `-ns` för att förhindra att tärningarna byter plats)\n',
                    inline=False)
    embed.add_field(name='Hur kan en dvärg pressa fler gånger?',
                    value='Du behöver en Discord-roll som heter "dvärg", "dwarf" eller "dvergar".',
                    inline=False)
    embed.add_field(name='Kontakt',
                    value='Hoppa in på https://discord.gg/BSxpaQP för att ta kontakt. GitHub: https://github.com/makedatanotlore/fobbot-discord',
                    inline=False)
    embed.set_footer(text='For English, type >help')

    await context.message.channel.send(embed=embed)


@client.command(name='help',
                pass_context=True)
async def english_help(context):
    if context.message.author.bot:
        return

    embed = discord.Embed(title='Help - Rolling the dice',
                          color=0xa2e600,
                          description='To roll dice, enter the number of dice followed by the type. Click 🔄 to push.')
    embed.add_field(name='Example Usage',
                    value='`>roll 5ba 2sk 2gr d8`\n'
                          '*Remember to smash that space button.*',
                    inline=False)
    embed.add_field(name='Dice',
                    value=f'Base Attribute Die - `ba`\n'
                    f'Skill Die - `sk`\n'
                    f'Gear/Weapon Die - `gr/wp`\n'
                    f'Artifact Die D8 - `d8`\n'
                    f'Artifact Die D10 - `d10`\n'
                    f'Artifact Die D12 - `d12`',
                    inline=False)
    embed.add_field(name='Resource Dice',
                    value='When you\'re using a resource. A<:grey_skull:547454438873366528>means the resource is consumed.\n'
                    f'Resource Die D6 - `resd6`\n'
                    f'Resource Die D8 - `resd8`\n'
                    f'Resource Die D10 - `resd10`\n'
                    f'Resource Die D12 - `resd12`\n',
                    inline=False)
    embed.add_field(name='Negative Dice',
                    value='When you have a negative bonus modifier.\n'
                    f'Negative D6 - `nt/nv`\n',
                    inline=False)
    embed.add_field(name='Numbered Dice',
                    value='When you need an actual number on the die.\n'
                    f'Regular D6 - `d6`\n'
                    f'*Using `-an` to get **ALL** the numbers is the 9bee\'s knees.*',
                    inline=False)
    embed.add_field(name='Notes',
                    value='When you need to add a note to your roll, use "".\n'
                    f'`>roll 2resd8 "Food/Water" -ns`\n'
                    '(in this case we add `-ns` to prevent the dice from shuffling around)\n',
                    inline=False)
    embed.add_field(name='How do Dwarves get more pushes?',
                    value='You need to be assigned a Discord role called "dvärg", "dwarf", or "dvergar".',
                    inline=False)
    embed.add_field(name='Contact',
                    value='Visit https://discord.gg/BSxpaQP to get in touch. GitHub: https://github.com/makedatanotlore/fobbot-discord',
                    inline=False)
    embed.set_footer(text='För svenska, skriv >hjälp')

    await context.message.channel.send(embed=embed)


async def embed_template(context, dicepool, roll_count, title=' '):

    if [die for die in dicepool if die.success_icon]:
        success_icon = [die for die in dicepool if die.success_icon][0].success_icon
        successes = sum([die.active.swords for die in dicepool])
        fails = sum([die.active.skulls for die in dicepool])
        if [die for die in dicepool if die.fail_icon]:
            fail_icon = [die for die in dicepool if die.fail_icon][0].fail_icon
            embed = discord.Embed(
                title=title,
                description=f'**{roll_count})** {success_icon} = {successes}         {fail_icon} = {fails}',
                color=context.message.author.color)
        else:
            embed = discord.Embed(
                title=title,
                description=f'**{roll_count})** {success_icon} = {successes}',
                color=context.message.author.color)
    else:
        embed = discord.Embed(title=title,
                              description=f'**{roll_count})**',
                              color=context.message.author.color)

    if ACTUAL_NUMBERS_REGEX.search(context.message.content):
        embed.add_field(name='Actual Numbers',
                        value=f'{[die.active.pips for die in dicepool]}')

    embed.set_author(name=context.message.author.display_name,
                     icon_url=context.message.author.avatar_url)

    return embed


async def parse_args(context):
    hand = []

    for regex, die in REGEX.items():
        result = regex.search(context.message.content.lower())
        if result is not None:
            amount = int(result.group(1)) if result.group(1) is not '' else 1
            hand += [die() for i in range(amount)]

    no_shuffle = NO_SHUFFLE_REGEX.search(context.message.content)
    if no_shuffle:
        return hand

    random.shuffle(hand)
    return hand


# divides list into chunks
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


client.run(TOKEN)


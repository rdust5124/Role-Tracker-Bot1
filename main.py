import os
import ctx as ctx
import discord
import asyncio
import pandas
import pandas as pd
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import cooldown, BucketType, bot
from datetime import date, datetime

__all__ = [
    'discord', 'asyncio', 'pandas', 'commands', 'cooldown', 'BucketType', 'os',
    'bot', 'datetime', 'date', 'ctx', 'get'
]

client = commands.Bot(command_prefix='>', case_insensitive=True)


@client.event
async def on_ready():
    print('Bot is ready')


#    channel = client.get_channel(877880333276704810)
#    await channel.send('hello')

data = {
    'Character Name': [],
    'Main class': [],
    'Multi-Class': [],
    'Multi-Class Names': [],
    'User Name': [],
    'Current Rank': [],
    'Current Badges': [],
    'Time of logging': [],
    'Badge Increment': []
}

df = pd.DataFrame(data)
YesNo = dict({'Yes': 1, 'No': 2})

Server_Rank = dict({
    'Unranked': [0, 0.5],
    'Rookie': [1, 1.5, 2, 2.5],
    'Novice': [3, 3.5, 4, 4.5, 5, 5.5],
    'High Novice': [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5],
    'Apprentice': [10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5],
    'High Apprentice':
    [15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5],
    'Adventurer':
    [21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26, 26.5, 27, 27.5],
    'High Adventurer': [
        28, 28.5, 29, 29.5, 30, 30.5, 31, 31.5, 32, 32.5, 33, 33.5, 34, 34.5,
        35, 35.5
    ],
    'Journeyman': [
        36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5, 42, 42.5,
        43, 43.5
    ],
    'High Journeyman': [
        44, 44.5, 45, 45.5, 46, 46.5, 47, 47.5, 48, 48.5, 49, 49.5, 50, 50.5,
        51, 51.5
    ],
    'Veteran': [
        52, 52.5, 53, 53.5, 54, 54.5, 55, 55.5, 56, 56.5, 57, 57.5, 58, 58.5,
        59, 59.5, 60, 60.5, 61, 61.5
    ],
    'High Veteran': [
        62, 62.5, 63, 63.5, 64, 64.5, 65, 65.5, 67, 67.5, 68, 68.5, 69, 69.5,
        70, 70.5, 71, 71.5
    ],
    'Guardian': [
        72, 72.5, 73, 73.5, 74, 74.5, 75, 75.5, 76, 76.5, 77, 77.5, 78, 78.5,
        79, 79.5
    ],
    'High Guardian':
    [80, 80.5, 81, 81.5, 82, 82.5, 83, 83.5, 84, 84.5, 85, 85.5, 86, 86.5],
    'Champion': [87, 87.5, 88, 88.5, 89, 89.5, 90, 90.5, 91, 91.5, 92, 92.5],
    'High Champion': [93, 93.5, 94, 94.5, 95, 95.5, 96, 96.5, 97, 97.5],
    'Master': [98, 98.5, 99, 99.5, 100, 100.5, 101, 101.5],
    'High Master': [102, 102.5, 103, 103.5, 104, 104, 104.5, 105, 105.5],
    'Grand Master': [106, 106.5, 107, 107.5, 108, 108.5, 109, 109.5]
})

Server_Class = dict({
    1: 'Artificer',
    2: 'Barbarian',
    3: 'Bard',
    4: 'Cleric',
    5: 'Druid',
    6: 'Fighter',
    7: 'Monk',
    8: 'Paladin',
    9: 'Ranger',
    10: 'Rogue',
    11: 'Sorcerer',
    12: 'Warlock',
    13: 'Wizard',
    14: 'Homebrew'
})


class DataFrameManip:
    async def dfdmupdate(self, msg, charname, class_name, multiclass,
                         multiname, currentrank, badges, time, increment):
        global df
        i = df[df['Character Name'] == charname].index
        df.loc[i, 'Main Class'] = class_name
        df.loc[i, 'Multi_Class'] = multiclass
        df.loc[i, 'Multi-Class Names'] = multiname
        df.loc[i, 'Current Rank'] = currentrank
        df.loc[i, 'Current Badges'] = float(badges) + float(increment)
        df.loc[i, 'Time of logging'] = time
        df.loc[i, 'Badge Increment'] = float(increment)
        await DataFrameManip.dmsheet_show(0, msg, charname)
        return

    async def dfplayerupdate(self, msg, charname, username, time, increment):
        global df
        global Server_Rank
        i = df[df['Character Name'] == charname].index
        badges = df.loc[i, 'Current Badges']
        float(badges)
        float(increment)
        df.loc[i, 'User Name'] = username
        new_badge_count = badges + increment
        float(new_badge_count)
        df.loc[i, 'Current Badges'] = new_badge_count
        df.loc[i, 'Time of logging'] = time
        df.loc[i, 'Badge Increment'] = increment
        for key, value in Server_Rank.items():
            if float(new_badge_count) in value:
                currentrank = key
                break
            else:
                currentrank = df.loc[i, 'Current Rank']

        dummy_string = df.loc[i, 'Current Rank']

        if dummy_string[0] is not currentrank:
            df.loc[i, 'Current Rank'] = currentrank
            await DataFrameManip.grant_role(0, msg, currentrank)

        await DataFrameManip.sheet_show(0, msg, charname)
        return

    async def addcharacter(self,
                           msg,
                           charname,
                           class_name,
                           multiclass,
                           multiname,
                           username,
                           currentrank,
                           badges,
                           time,
                           increment=0.0):
        global df
        series = pd.DataFrame({
            'Character Name': [charname],
            'Main class': [class_name],
            'Multi-Class': [multiclass],
            'Multi-Class Names': [multiname],
            'User Name': [username],
            'Current Rank': [currentrank],
            'Current Badges': [badges],
            'Time of logging': [time],
            'Badge Increment': [increment]
        })
        df = pd.concat([series, df])
        await DataFrameManip.grant_role(0, msg, currentrank)
        return

    async def removecharacter(self, charname):
        global df
        i = df[df['Character Name'] == charname].index
        df = df.drop(i, inplace=True)
        return

    async def dmsheet_show(self, msg, charname):
        global df
        i = df[df['Character Name'] == charname].index
        em = discord.Embed(title=f"Character Sheet:",
                           description=f"",
                           color=0xFFFFFF)
        dummy_series = df.loc[i, 'Character Name']
        em.add_field(name="Character Name:",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'Main class']
        em.add_field(name="Character Class:",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'Multi-Class Names']
        em.add_field(name="Multi class(es):",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'Current Rank']
        em.add_field(name="Current Rank:", value=dummy_series[0], inline=False)
        dummy_series = df.loc[i, 'Current Badges']
        em.add_field(name="Total Badges:", value=dummy_series[0], inline=False)
        dummy_series = df.loc[i, 'Time of logging']
        em.add_field(name="Last modified:",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'Badge Increment']
        em.add_field(name="Last increase of badges:",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'User Name']
        em.add_field(name="Character belongs to:",
                     value=dummy_series[0],
                     inline=False)
        await msg.channel.send(embed=em)

    async def check_user_priviledge(self, msg, charname):
        global df
        i = df[df['Character Name'] == charname].index
        # await msg.channel.send(df.loc[i, 'User Name'])
        dummy_series = df.loc[i, 'User Name']
        if msg.author == dummy_series[0]:
            check = 1
        else:
            check = 0
        return check

    async def sheet_show(self, msg, charname):
        global df
        i = df[df['Character Name'] == charname].index
        em = discord.Embed(title=f"Character Sheet:",
                           description=f"",
                           color=0xFFFFFF)
        dummy_series = df.loc[i, 'Character Name']
        em.add_field(name="Character Name:",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'Main class']
        em.add_field(name="Character Class:",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'Multi-Class Names']
        em.add_field(name="Multi class(es):",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'Current Rank']
        em.add_field(name="Current Rank:", value=dummy_series[0], inline=False)
        dummy_series = df.loc[i, 'Current Badges']
        em.add_field(name="Current Badges:",
                     value=dummy_series[0],
                     inline=False)
        dummy_series = df.loc[i, 'Badge Increment']
        em.add_field(name="Last increase of badges:",
                     value=dummy_series[0],
                     inline=False)

        await msg.channel.send(embed=em)

    # async def check_role_priviledge(self, msg):

    #@commands.Bot(pass_context=True)
    async def grant_role(self, msg, rankname):
        role = discord.utils.get(msg.guild.roles, name=str(rankname))
        await msg.author.add_roles(role)
        return


@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def register(ctx):
    if ctx.message.author == client.user:
        return
    await ctx.send('Enter name of character', delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    charname = msg.content
    # await ctx.send(charname)
    username = msg.author
    # await ctx.send(username)
    time = msg.created_at
    # await ctx.send(time)

    em = discord.Embed(
        title=f'Enter corresponding number:',
        description=
        f'1: Artificer \n 2: Barbarian \n 3: Bard \n 4: Cleric \n 5: Druid \n 6: Fighter \n 7: Monk \n 8: Paladin \n 9: Ranger \n 10: Rogue \n 11: Sorcerer \n 12 : Warlock \n 13: Wizard \n 14: Homebrew',
        color=0xFFFFFF)
    await ctx.send(embed=em, delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    if int(msg.content) in Server_Class:
        class_name = Server_Class[int(msg.content)]
    else:
        await ctx.send('Bad Input')
        return
        # await ctx.send(class_name)

    em = discord.Embed(title=f"Multi Classed?",
                       description=f"1: Yes \n 2: No",
                       color=0xFFFFFF)
    await ctx.send(embed=em, delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    if msg.content == '1' or msg.content == 'Yes':
        multiclass = 'Yes'
    # await ctx.send(multiclass)
    elif msg.content == '2' or msg.content == 'No':
        multiclass = 'No'
    # await ctx.send(multiclass)
    else:
        await ctx.send('Bad Input', delete_after=20)
        return

    if multiclass == 'Yes':
        await ctx.send('Enter secondary classes', delete_after=20)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await client.wait_for('message', check=check)
        multiname = msg.content
        # await ctx.send(multiname)
    else:
        multiname = 'None'
        # await ctx.send(multiname)

    await ctx.send('Enter Badge Count', delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)

    badges = abs(float(msg.content))
    # await ctx.send(badges)

    counter = 0
    for keys in Server_Rank.keys():
        temp_list = Server_Rank[keys]
        if float(badges) in temp_list:
            rank = keys
            # await ctx.send(rank)
            counter = 1
    if counter != 1:
        rank = 'None'

    await DataFrameManip.addcharacter(0, msg, charname, class_name, multiclass,
                                      multiname, username, rank, badges, time)

    @register.error
    async def register_error(ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send('Wait for {error.retry_after:.2f}', delete_after=20)
        if isinstance(error, commands.BadArgument):
            await ctx.send('Bad input', delete_after=20)

    await ctx.send("Character Added!")


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def update(ctx):
    if ctx.message.author == client.user:
        return
    global df

    await ctx.send('Enter name of character')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    chk = await DataFrameManip.check_user_priviledge(0, msg, msg.content)
    # await ctx.send(chk)
    if chk == 1:

        charname = msg.content
        username = msg.author
        time = msg.created_at

        await ctx.send('Enter number of badges to be added:')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await client.wait_for('message', check=check)
        increment = abs(float(msg.content))

        await DataFrameManip.dfplayerupdate(0, msg, charname, username, time,
                                            increment)
        await ctx.send('Character updated')
    else:
        await ctx.send('This character does not belong to you',
                       delete_after=20)

    @update.error
    async def update_error(ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send('Wait for {error.retry_after:.2f}', delete_after=20)
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send('Bad input', delete_after=20)


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def dmupdate(ctx):
    # global df

    if ctx.message.author == client.user:
        return
    await ctx.send('Enter name of character')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    charname = msg.content
    time = msg.created_at

    await ctx.send('Enter main class of character', delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    class_name = msg.content

    await ctx.send('Is character multi-class?', delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    multiclass = msg.content

    await ctx.send('Enter secondary classes', delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    multiname = msg.content

    await ctx.send('Enter Current rank', delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    currentrank = msg.content

    await ctx.send('Enter Badge Count', delete_after=20)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    badges = msg.content
    increment = 0.0

    await DataFrameManip.dfdmupdate(0, msg, charname, class_name, multiclass,
                                    multiname, currentrank, badges, time,
                                    increment)

    @dmupdate.error
    async def dmupdate_error(ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send('Wait for {error.retry_after:.2f}', delete_after=20)
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send('Bad input', delete_after=20)


@client.command()
async def dmremove(ctx):
    #   global df

    if ctx.message.author == client.user:
        return

    await ctx.send('Enter name of character')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)

    await ctx.send(
        'Are you sure you want to delete this record? Type YES to proceed.')
    await DataFrameManip.dmsheet_show(0, msg, msg.content)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    confirm = await client.wait_for('message', check=check)
    if confirm.content == 'YES':
        await DataFrameManip.removecharacter(0, msg)
        await ctx.send('Record Deleted')
    else:
        await ctx.send('Incorrect syntax, deletion cancelled', delete_after=20)

    @dmremove.error
    async def dmremove_error(ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send('Wait for {error.retry_after:.2f}', delete_after=20)
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send('Bad input', delete_after=20)


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def show(ctx):
    # global df

    if ctx.message.author == client.user:
        return

    await ctx.send('Enter name of character')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    chk = await DataFrameManip.check_user_priviledge(0, msg, msg.content)
    # await ctx.send(chk)
    if chk == 1:
        await DataFrameManip.sheet_show(0, msg, msg.content)
    else:
        await ctx.send('This character does not belong to you',
                       delete_after=20)

    @show.error
    async def show_error(ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send('Wait for {error.retry_after:.2f}', delete_after=20)
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send('Bad input', delete_after=20)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def dmshow(ctx):
    # global df

    if ctx.message.author == client.user:
        return

    await ctx.send('Enter name of character')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for('message', check=check)
    await DataFrameManip.dmsheet_show(0, msg, msg.content)

    @dmshow.error
    async def dmshow_error(ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send('Wait for {error.retry_after:.2f}', delete_after=20)
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send('Bad input', delete_after=20)


my_secret = os.environ['TOKEN']
client.run(my_secret)

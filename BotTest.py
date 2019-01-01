import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import youtube_dl
import praw
import random

players = {}
queues = {}


r = praw.Reddit(client_id='CLIENT_ID',client_secret= None, password='PASSWORD',user_agent='USERAGENT', username='USERNAME')

Client = discord.Client()
client = commands.Bot(command_prefix = "h!")

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author,content))   
    if message.content == "cookie":
        await client.send_message(message.channel, ":cookie:")
    if message.content == "cat":
        await client.send_message(message.channel,"https://media1.tenor.com/images/3fe0f068821a9baec3b1991b4c3cee35/tenor.gif?itemid=4576355")
    await client.process_commands(message)
    
    

# @client.event
# async def on_message_delete(message):
#     author = message.author
#     content = message.content
#     channel = message.channel
#     await client.send_message(channel, '{}: {}'.format(author,content))


@client.command()
async def ping():
    start_time = time.time()
    await client.say('Pong!')
    end_time = time.time() - start_time
    await client.say('it took {} seconds'.format(end_time))
    if end_time < .2:
        await client.say('wow, that was fast!')
    else:
        await client.say('eh, not as fast :/')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)   

@client.command(pass_context = True)
async def join(ctx):
        channel = ctx.message.author.voice.voice_channel
        await client.join_voice_channel(channel)

@client.command(pass_context = True)
async def leave(ctx):
    try:
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()
    except AttributeError:
        await client.say('im not in a vc')

@client.command(pass_context = True)
async def play(ctx,url):
    try:
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        players[server.id] = player
        player.start()
    except AttributeError:
        await client.say('im already playing something')

@client.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context = True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_contextx = True)
async def queue(ctx,url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda a: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video queued.')


@client.command(pass_context=True)       
async def clear(ctx, number):
    '''Clears The Chat 2-100'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await client.say("You do not have the role: Admin")
    pass
    mgs = []
    number = int(number)
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)


@client.command(pass_context = True)
async def serverinfo(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles)
    channelz = len(server.channels)
    time = str(server.created_at); time = time.split(' '); time= time[0]

    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', colour = 0xFFFF)
    join.set_thumbnail(url = server.icon_url)
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id)
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count))
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz))
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles)
    join.set_footer(text ='Created: %s'%time)

    return await client.say(embed = join)







client.run("NTA0NDA5MzU4MjU2MzA4MjI0.DrFcyQ.oRMEY1bIV0_UZhBZlndedGbzWBM")
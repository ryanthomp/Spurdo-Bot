#!/usr/bin/env python3
import random
import discord
import re
import requests
import urllib.request
import json
import cleverbot
import pickle
import logging

HairColor = ("Brunette", "Blond", "Red", "Pink Dyed", "Blue Dyed",  "No")
Ethnic = ("Mexican", "Black", "Nigerian", "Arab", "Aryan", "Northern Italian", "Ugandan")
Ideology = ("Authoritarian", "Nazbol", "Duginist", "Alt-Right", "Alt-Lite", "Fascist", "NatSoc", "AnCom", "Neo-Nazi", "AnCap", "Anarchist", "Communist", "Socialist")
Gender = ("Trap", "Trans-Girl", "Girl")
Strength = ("Orthodox", "Moderate", "Traditional")
Religon = ("Mormon", "Jewish", "Christian", "Catholic", "Scientologist", "Prot", "Lutheran")
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
logging.basicConfig(level=logging.INFO)
client = discord.Client()
print('Client')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='BenisXD'))
    servers = list(client.servers)
    print("Connected on "+str(len(client.servers))+" servers:")
    for x in range(len(servers)):
        print(' '+servers[x-1].name)
    print('------')


@client.event
async def on_member_join(member):
        print("JOIN")
        server = member.server
        print(member)
        print(server)
        print(member)
        await client.send_message(discord.Object(id='265623454521229312'), 'Welcome <@%s> to %s! Say `Ready` to be immigrated.' % (member, server))


@client.event
async def on_message(message):
    cw = cleverbot.Cleverbot('')
    if message.content == '!me':
        print('ME')
        user = message.author.ids
        political = random.choice(Ideology)
        religon1 = random.choice(Religon)
        hair = random.choice(HairColor)
        race = random.choice(Ethnic)
        sexuality = random.choice(Gender)
        hardcore = random.choice(Strength)
        await client.send_message(message.channel, 'Hi! <@%s> I am a %s %s %s %s %s with %s hair.' % (user, political, race, hardcore, religon1, sexuality, hair))

    elif message.content.startswith('-'):
        print('TALK')
        inp = message.content
        inpn = inp.replace("-", "")
        print(message.author)
        print(inpn)
        await client.send_typing(message.channel)
        cw.say(inpn)
        await client.send_typing(message.channel)
        out = cw.output
        if out is None:
            await client.send_message(message.channel, "**Error** all calls to the API have been used")
        else:
            print(out)
            await client.send_typing(message.channel)
            await client.send_message(message.channel, out)

    elif message.content.startswith('!reset'):
        print('RESET')
        cw.reset()
        await client.send_message(message.channel, "RESET")

    elif message.content.startswith('!promote '):
        print("PROMOTE")
        user_mess = message.content
        print(user_mess)
        userid = message.author.id
        member = message.author
        print(userid)
        user_mess2 = user_mess.replace('!promote', '')
        message1 = re.sub("[^\w]", " ",  user_mess2).split()
        print(message1)
        name1 = message1[1]
        print("ROLE %s" % name1)
        user3 = message1[0]
        user = message.mentions
        user2 = user[0]
        print("USER %s" % user2)
        reason = message1[2]
        permissions = member.server_permissions
        if permissions.manage_roles:
            role = discord.utils.get(message.server.roles, name=name1)
            await client.add_roles(user2, role)
            await client.send_message(discord.Object(id='283037229759070209'), "<@%s> given %s by <@%s> because %s" % (user3, role, member, reason))
        else:
            await client.send_message(message.channel, "Nig u don't hav the perms. smh ")

    elif message.content.startswith('=='):
        pkl_file = open('img.pkl', 'rb')
        lis = pickle.load(pkl_file)
        pkl_file.close()
        print(lis)
        org = await client.send_message (message.channel, "Loading...")
        print("IMAGE")
        attach = message.attachments[0]
        print(attach)
        name = attach['filename']
        attach2 = attach['url']
        m = requests.get(attach2, stream=True, headers={'User-Agent': USER_AGENT})
        with open(name, 'wb') as f:
            for chunk1 in m.iter_content():
                f.write(chunk1)
        lis.append(name)
        print(lis)
        print("OPEN")
        output = open('img.pkl', 'wb')
        print("DUMP")
        pickle.dump(lis, output)
        output.close()
        await client.edit_message(org, "Added!")
        print("COMPLETED")

    elif message.content == '!meme':
        pkl_file = open('img.pkl', 'rb')
        lis = pickle.load(pkl_file)
        pkl_file.close()
        file = random.choice(lis)
        await client.send_file(message.channel, file)

    elif message.content.startswith('!weather '):
        user_mess = message.content
        print(user_mess)
        user_mess2 = user_mess.replace('!weather ', '')
        print(user_mess2)
        message1 = re.sub("[^\w]", " ",  user_mess2).split()
        print(message1)
        state = message1[0]
        city = user_mess2[3:]
        city = city.replace(' ', '_')
        url = 'http://api.wunderground.com/api/699a8178c98f6d4b/geolookup/conditions/q/%s/%s.json' % (state, city)
        print(url)
        try:
            f = urllib.request.urlopen(url)
            json_string = f.read()
            parsed_json = json.loads(json_string)
            location = parsed_json['location']['city']
            temp_f = parsed_json['current_observation']['temp_f']
            wind_mph = parsed_json['current_observation']['wind_mph']
            weather = parsed_json['current_observation']['weather']
            windchill_f = parsed_json['current_observation']['windchill_f']
            await client.send_message(message.channel, 'Current Conditions for %s **Weather:** `%s`, **Temperature:** `%s °F`, **Wind:** `%s mph`, **Windchill:** `%s °F`' % (location, weather, temp_f, wind_mph, windchill_f))
            f.close()
        except KeyError:
            await client.send_message(message.channel, "**FORMAT**: `!weather {state code (GA)} {City}`")

    elif message.content.startswith('ready'):
        print("READY")
        member1 = message.author
        print(member1)
        if message.author == member1:
            await client.send_message(discord.Object(id='265623454521229312'), "What is your political ideology?")
            message = await client.wait_for_message(author=member1)
            ideo = message.content
            print(ideo)
#            #DELETE
            await client.purge_from(discord.Object(id='265623454521229312'), limit=2)
            await client.send_message(discord.Object(id='265623454521229312'), "What is your race?")
            message = await client.wait_for_message(author=member1)
            race = message.content
            print(race)
#            #DELETE
            await client.purge_from(discord.Object(id='265623454521229312'), limit=2)
            await client.send_message(discord.Object(id='265623454521229312'), "What is your nationality?")
            message = await client.wait_for_message(author=member1)
            nation = message.content
            print(nation)
#            #DELETE
            await client.purge_from(discord.Object(id='265623454521229312'), limit=2)
            await client.send_message(discord.Object(id='265623454521229312'), "Please post the image of your 8values test")
            if message.content.startswith("https"):
                name = "http 8V.png"
                linkn = message.content
                r = requests.get(linkn, stream=True, headers={'User-Agent': USER_AGENT})
                with open(name, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
            else:
                while True:
                            try:
                                message = await client.wait_for_message(author=member1)
                                attach = message.attachments[0]
                                print(attach)
                                name = attach['filename']
                                attach2 = attach['url']
                                m = requests.get(attach2, stream=True, headers={'User-Agent': USER_AGENT})
                                with open(name, 'wb') as f:
                                    for chunk1 in m.iter_content():
                                        f.write(chunk1)
                            except IndexError:
                                continue
                            break
            await client.purge_from(discord.Object(id='265623454521229312'), limit=2)
            await client.send_message(discord.Object(id='265623454521229312'), "Please post the image of your Political Compass")
            if message.content.startswith("https"):
                name2 = "http PC.png"
                linkn = message.content
                r = requests.get(linkn, stream=True, headers={'User-Agent': USER_AGENT})
                with open(name2, 'wb') as f:
                    for chunk3 in r.iter_content():
                        f.write(chunk3)
            else:
                while True:
                            try:
                                message = await client.wait_for_message(author=member1)
                                attach3 = message.attachments[0]
                                print(attach3)
                                name2 = attach3['filename']
                                attach4 = attach3['url']
                                o = requests.get(attach4, stream=True, headers={'User-Agent': USER_AGENT})
                                with open(name2, 'wb') as f:
                                    for chunk2 in o.iter_content():
                                        f.write(chunk2)
                            except IndexError:
                                continue
                            break
            fm = '{0.mention}'
            await client.purge_from(discord.Object(id='265623454521229312'), limit=2)
            await client.send_message(discord.Object(id='265623454521229312'), "Thank you an Immigration officer will review your answers shortly.")
            embed = discord.Embed(title='Immigration Application', color=0x206694)
            embed.add_field(name="User", value=fm.format(member1), inline=False)
            embed.add_field(name="What is your political ideology?", value=ideo, inline=False)
            embed.add_field(name="What is your race?", value=race, inline=False)
            embed.add_field(name="What is your nationality?", value=nation, inline=False)
            await client.send_message(discord.Object(id='359030804359413760'), embed=embed)
            await client.send_file(discord.Object(id='359030804359413760'), name, content="8Values")
            await client.send_file(discord.Object(id='359030804359413760'), name2, content="Political Compass")


client.run('')

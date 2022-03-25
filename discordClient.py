# Wizardkoala/2021
# https://github.com/Wizardkoala/Auto-Time-Convert
# Python 3.9.6
# 

import sys
if sys.version_info[1] <= 8:
    
    from backports.zoneinfo import ZoneInfo, ZoneInfoNotFoundError
else:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from datetime import datetime as time
import os
from time import sleep
from os import name as osname
from os import path
from settings import *
import json
import discord

Version = "Titanium-1.7.1"


def Authorize(userid, requireAdmin=False) -> bool:
    userid = str(userid)

    if requireAdmin:
        if userid in json.load(open("Secret.json", 'r'))["Admins"]:
            return True
        else:
            return False
    else:
        return True
    

# Gets the users timezone from the database
def GetTimezone(userID: str) -> str:
    try:
        timz = json.load(open("timezones.json", 'rb'))
        return timz[str(userID)]["tz"]
    except:
        return "not-regi"

# Converts a string time into a datetime object
def Format(string: str, userID: str) -> any:
    formats = ["%I:%M %p", "%I:%M%p",  "%H:%M", "%I:%p"]
    t = None
    for fmt in formats:
        try:
            # Sets all needed values from the datetime object 't'
            t = time.strptime(string, fmt)
            t = t.replace(day=time.today().date().day)
            t = t.replace(month=time.today().date().month)
            t = t.replace(year=time.today().date().year)
            t = t.replace(tzinfo=ZoneInfo(GetTimezone(userID)))
        except ZoneInfoNotFoundError:
            return "not-regi"
        except ValueError:
            pass
        finally:
            pass
    return t

# Main Bot Class
class TimeBot(discord.Client):
    def __init__(self, *, loop=None, **options):
        self.Secretdb = json.load(open("Secret.json", 'r'))
        super().__init__(loop=loop, **options)

    class Commands():
        async def registerOther(self, message: discord.Message) -> None:
            """Register a user to a timezone
            Syntax: TRegisterOther! DiscordUserID Timezone\n
            Eg. TRegisterOther! 267494392238047233 America/New_York"""


            if not Authorize(message.author.id, requireAdmin=IsAdminRegOther):
                await message.channel.send("You do not have the permission to do this.")
                return

            db = json.load(open("timezones.json", 'rb'))
            message.content = message.content.split(' ')

            # Checks if the entered timezone is valid
            try:
                ZoneInfo(message.content[2])
            except ZoneInfoNotFoundError:
                await message.channel.send('"' + message.content[2] + '" is not a valid timezone.')
                return

            if message.content[2] not in db['All']:
                db['All'].append(message.content[2])

            targetName = await self.fetch_user(message.content[1])
            targetName = str(targetName)
            db[message.content[1]] = {}
            db[message.content[1]]["name"] = targetName
            db[message.content[1]]["tz"] = message.content[2]

            print()

            if message.content[1] not in db['RegisteredUsers']:
                db['RegisteredUsers'].append(str(message.content[1]))

            json.dump(db, open("timezones.json", 'w'), indent=4)
            await message.channel.send(f"Registered user: {targetName}!")

        async def registerSelf(self, message) -> None:
            """Alows users to register their own timezone
            eg. TRegister! America/New_York"""

            if not Authorize(message.author.id, requireAdmin=IsAdminRegSelf):
                await message.channel.send("You do not have the permission to do this.")
                return

            db = json.load(open("timezones.json", 'rb'))
            message.content = message.content.split(' ')

            AuthorId = str(message.author.id)
            AuthorName = message.author.name
            Timezone = message.content[1]

            # Checks if the entered timezone is valid
            try:
                ZoneInfo(Timezone)
            except ZoneInfoNotFoundError:
                await message.channel.send('"' + Timezone + '" is not a valid timezone.')
                return

            if Timezone not in db['All']:
                db['All'].append(Timezone)

            db[AuthorId] = {
                "name": AuthorName,
                "tz": Timezone
            }

            if AuthorId not in db['RegisteredUsers']:
                db['RegisteredUsers'].append(str(AuthorId))

            json.dump(db, open("timezones.json", 'w'), indent=4)
            await message.channel.send("Registered user!")

        async def shutdown(self, message) -> None:
            """Shuts down the bot."""
            if not Authorize(message.author.id, requireAdmin=IsAdminShutdown):
                await message.channel.send("You do not have the permission to do this.")
                return

            await message.channel.send("Shutting Down!")
            await self.change_presence(activity=discord.Game(name="Shutting Down"))
            await self.close()

        async def status(self, message) -> None:
            """Changes the status message of the bot
            eg. TPlay! [Message]"""
            if not Authorize(message.author.id, requireAdmin=IsAdminStatus):
                await message.channel.send("You do not have the permission to do this.")
                return

            status = ' '.join(message.content.split(' ')[1:])
            db = json.load(open("Secret.json", 'r'))
            db['Status'] = status
            json.dump(db, open("Secret.json", 'w'), indent=4)

            await self.change_presence(activity=discord.Game(name=status))
            await message.channel.send("Changed Status!")

        async def report(self, message) -> None:
            """Sends a debug report."""
            if not Authorize(message.author.id, requireAdmin=IsAdminReport):
                await message.channel.send("You do not have the permission to do this.")
                return


            report = [
                "Version %s" % Version,
                "Running on: Windows" if osname == "nt" else "Running on: Unix-Based",
                "Latency: %ims" % int(self.latency * 1000),

                "Users num %i" % len(json.load(open("timezones.json", 'rb'))[
                    "RegisteredUsers"]),

                "Timezone num: %i" % len(
                    json.load(open("timezones.json", 'rb'))["All"]),
            ]
            await message.channel.send('\n'.join(report))

    async def IsCommand(self, message: discord.Message, Keyword: str, admin=False):
        MSGC = message.content.split(' ')

        if Keyword in MSGC:
            if admin and not( Authorize(MSGC[1]) ):
                await message.channel.send("Authorization Failed.")
                return False
            elif admin:
                print("Admin Command Used:", MSGC)
            
            return True

        else: return False

    async def on_connect(self):
        print('[INFO] Connecting to discord!')

    async def on_ready(self):
        print('[INFO] Bot is ready!')
        await self.change_presence(activity=discord.Game(name=OnReadyStatus))


    async def on_message(self, message: discord.Message):
        # Everytime the bot is used check to see if there are unneeded timezones saved.
        # If so remove them.
        if message.author == self.user:
            db = json.load(open("timezones.json", 'rb'))

            for tmz in db["All"]:
                used = False
                for user in db["RegisteredUsers"]:
                    if db[user]["tz"] == tmz:
                        used = True
                        continue

                if not used:
                    print("[INFO] Removing Unused Timezone:", tmz)
                    db['All'].remove(tmz)
                    json.dump(db, open("timezones.json", 'w'), indent=4)
            return

        commandLookupTable = [
            [CMDRegOther, self.Commands.registerOther],
            [CMDRegister, self.Commands.registerSelf],
            [CMDShutdown, self.Commands.shutdown],
            [CMDStatus, self.Commands.status],
            [CMDReport, self.Commands.report]
        ]

        for command in commandLookupTable:
            if await self.IsCommand(message, command[0]):
                await command[1](self, message=message)
                return

        else:
            ## ---
            ## Checks if there is a time in the message, if so extracts it

            # Checks if 'am' or 'pm' are in the message
            checks = ["pm", "am"] 
            for c in checks:
                if c in message.content:
                    message.content = message.content[:message.content.index(c)] + ":00" + \
                        message.content[message.content.index(c):]

            # Checks if there is a colon that is preceded and followed by an int
            targetTime = None
            for i, l in enumerate(message.content):
                if (l == ":"):
                    try:
                        int(message.content[i+1] + message.content[i+2] + message.content[i-1])
                        targetTime = ""
                        break
                    except Exception:
                        pass

            if targetTime != None:
                try:
                    assert i-2 >= 0
                    int(message.content[i-2])
                    targetTime = message.content[i-2:i+3]
                except Exception:
                    targetTime = message.content[i-1:i+3]

                if "pm" in message.content:
                    targetTime += "pm"
                elif "am" in message.content:
                    targetTime += "am"
                elif len(targetTime) == 4:
                    # If a pm or am is not specified then assume pm
                    targetTime += "pm"
                    await message.channel.send("Assuming time was PM")

            else:  # Return if we didn't find a time in the message
                return
            ## ---

            ## ---
            ## Converts the time into all other registed timezones
            t = Format(targetTime, message.author.id)
            if t == None:
                await message.channel.send("I couldn't convert the timezone on that.")

            elif t == "not-regi":
                await message.channel.send("You don't have a timezone registered.")

            else:
                emb = discord.Embed()
                emb.color = discord.Color.light_grey()

                ConvertTo = json.load(
                    open("timezones.json", 'rb'))["All"]
                ConvertTo.remove(
                    GetTimezone(message.author.id))

                for tmz in ConvertTo:
                    emb.add_field(
                        name=tmz,
                        value=str(t.astimezone(ZoneInfo(tmz)).strftime("%I:%M %p")),
                        inline=True
                    )

                await message.channel.send(embed=emb)
            ## ---

        


if __name__ == "__main__":
    if not path.exists("Secret.json"):
        db = {
            "Bot": input("Bot Token: "),
            "Status": "10-4 Soldier",
            "Admins": [input("What is your Discord client ID: ")],
        }

        json.dump(db, open("Secret.json", 'w'), indent=4)

    else:
        db = json.load(open("Secret.json", 'r'))

    Token = db["Bot"]
    OnReadyStatus = db['Status']
    
    if not path.exists("timezones.json"):
        open("timezones.json", 'w').write('{"All": [], "RegisteredUsers":[]}')

    client = TimeBot()
    client.run(Token)

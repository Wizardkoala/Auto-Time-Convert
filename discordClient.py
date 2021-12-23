# Wizardkoala/2021
# https://github.com/Wizardkoala/Auto-Time-Convert
# Python 3.9.6
# 
from datetime import datetime as time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from os import name as osname
from os import path
import json
import discord
import pyotp



OnReadyStatus = "10-4 Soldier"
Version       = "Bronze-1.6"

# Commands
CaseSensitive = False

CMDRegOther = "TRegisterOther!" # Register anouther user
CMDRegister = "TRegister!" # Self register timezone
CMDShutdown = "TEnd!" # Shutdown the bot (admin)
CMDStatus   = "TPlay!" # Change the game the bot is "playing"
CMDReport   = "TReport!" # Report debug info





def Authorize(code):
    TOTP = pyotp.TOTP(TOTPToken)
    return TOTP.verify(str(code))
    

# Gets the uses timezone from the database
def GetTimezone(userID):
    timz = json.load(open("timezones.json", 'rb'))
    return timz[str(userID)]["tz"]

# Converts a string time into a datetime object
def Format(string, userID):
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
    async def IsCommand(self, msg, Keyword, admin=True):
        MSGC = msg.content.split(' ')

        if Keyword in MSGC:
            if admin and not(Authorize(MSGC[1])):
                await msg.channel.send("Authorization Failed.")
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

    async def on_message(self, message):
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


        # Report for debugging purposes
        if await self.IsCommand(message, CMDReport):
            report = [
                "Version %s" % Version,
                "Running on: Windows" if osname == "nt" else "Running on: Unix-Based",
                "Latency: %ims" % int(self.latency * 1000),
                "Users num %i" % len(json.load(open("timezones.json", 'rb'))["RegisteredUsers"]),
                "Timezone num: %i" % len(json.load(open("timezones.json", 'rb'))["All"])
            ]
            await message.channel.send('\n'.join(report))

        # Cleanly shutdown (Not strictly needed disable if desired)
        if await self.IsCommand(message, CMDShutdown):
            message.content.split(' ')

            await message.channel.send("Shutting Down!")
            await self.change_presence(activity=discord.Game(name="Shutting Down"))
            await self.close()
            return

        # Change status message of the bot
        if await self.IsCommand(message, CMDStatus):
            message.content = message.content.split(' ')
            await self.change_presence(activity=discord.Game(name=' '.join(message.content[2:])))
            await message.channel.send("Changed Status!")

        # Syntax: TRegister! America/New_York
        if await self.IsCommand(message, CMDRegister, admin=False):
            db = json.load(open("timezones.json", 'rb'))
            message.content = message.content.split(' ')

            AuthorId = message.author.id
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
            return


        # Register a user to a timezone
        # Syntax: TRegisterOther! DiscordUserID FriendlyName Timezone
        # Eg: TRegisterOther! 267494392238047233 Install#0963 America/Denver
        if await self.IsCommand(message, CMDRegOther):
            db = json.load(open("timezones.json", 'rb'))
            message.content = message.content.split(' ')

            # Checks if the entered timezone is valid
            try:
                ZoneInfo(message.content[4])
            except ZoneInfoNotFoundError:
                await message.channel.send('"' + message.content[4] + '" is not a valid timezone.')
                return

            if message.content[4] not in db['All']:
                db['All'].append(message.content[3])

            db[message.content[2]] = {}
            db[message.content[2]]["name"] = message.content[3]
            db[message.content[2]]["tz"] = message.content[4]

            if message.content[2] not in db['RegisteredUsers']:
                db['RegisteredUsers'].append(str(message.content[2]))

            json.dump(db, open("timezones.json", 'w'), indent=4)
            await message.channel.send("Registered user!")
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

            # Checks if there is a comma that is preceded and followed by an int
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
                ConvertTo = json.load(
                    open("timezones.json", 'rb'))["All"]
                ConvertTo.remove(
                    GetTimezone(message.author.id))

                EndMessage = ""
                for tmz in ConvertTo:
                    EndMessage += (tmz + " " + str(t.astimezone(ZoneInfo(tmz)).strftime("%I:%M %p")) + " ")

                    if ConvertTo.index(tmz) != len(ConvertTo)-1:
                        EndMessage += "| "

                await message.channel.send(EndMessage)
            ## ---

        


if __name__ == "__main__":
    if not path.exists("Secret.json"):
        db = {
            "Bot": input("Bot Token: "),
            "TOTP": pyotp.random_base32()
        }
        print("TOTP Token: %s" % db['TOTP'])

        json.dump(db, open("Secret.json", 'w'), indent=4)
    
    if not path.exists("timezones.json"):
        open("timezones.json", 'w').write('{"All": [], "RegisteredUsers":[]}')

    db = json.load(open("Secret.json", 'r'))
    Token = db["Bot"]
    TOTPToken = db["TOTP"]

    client = TimeBot()
    client.run(Token)

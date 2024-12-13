# Wizardkoala/2024
# https://github.com/Wizardkoala/Auto-Time-Convert
# Python 3.11.0
#

import sys
from unicodedata import decomposition

if sys.version_info[1] <= 8:
    from backports.zoneinfo import ZoneInfo
else:
    from zoneinfo import ZoneInfo

from datetime import datetime as time
from os import path
from settings import *
import json

import discord
from discord import app_commands

from commands import *

Version = "Iridium-1.9.5"

# Main Bot Class
class TimeBot(discord.Client):
    def __init__(self, *, intents, loop=None, **options):
        self.Secretdb = json.load(open("secret.json", 'r'))
        super().__init__(intents=intents, loop=loop, **options)

    async def on_connect(self):
        print('[INFO] Connecting to discord!')

    # Sets the status to the previously saved value and sync slash commands
    # Keep in mind when changing slash commands globaly will take up to 2 hours to update.
    async def on_ready(self):
        await tree.sync()
        await self.change_presence(activity=discord.Game(name=OnReadyStatus))

        print('[INFO] Bot is ready!')

    # Check to see someone has sent a time in chat and responds accordingly
    async def on_message(self, message: discord.Message):
        if message.author.bot: #Ignores all bot input including itself.
            return

        zones = json.load(open("timezones.json", 'r'))
        time = GetTime(message.content)

        # Ignores all message that do not contain a time
        if not time: return

        # Ensures the user that sent the time has a registered timezone
        if str(message.author.id) not in zones['RegisteredUsers']:
            await message.reply("⚠️ You do not have a registered timezone. Use /register.")
            return

        # Get datetime object of the time
        t = Format(time, str(message.author.id))

        # Init a discord embed
        emb = discord.Embed()
        emb.color = discord.Color.light_grey()

        ConvertTo = json.load(
            open("timezones.json", 'rb'))["All"]
        ConvertTo.remove(
            GetTimezone(message.author.id))

        # Converts every timezone that has been registered.
        #    (not including the orgin user's timezone)
        for tmz in ConvertTo:
            emb.add_field(
                name=tmz,
                # Converts the timezone with the "astimezone" method
                value=str(t.astimezone(ZoneInfo(tmz)).strftime("%I:%M %p")),
                inline=True
            )

        await message.channel.send(embed=emb)
        # ---


def GetTime(message: str) -> any:
    # Needed for meridiem checks
    message = message.lower() 

    #Colon based detection
    try:
        while ":" in message:
            index = message.index(":")

            # Splits the time into a list [hour, minute]
            time = message[index-2:index+3].split(':')
            if time == ["0"] or time == ['']:
                time = message[index-1:index+3].split(':')

            time[0] = time[0].replace(" ", "0")

            if not time[0].isdigit() or not time[1].isdigit():
                message = message.replace(":", "", 1)
                continue

            # Corrects time to comply with datetime 0..23 range
            if time[0] == "12" and "pm" in message:
                time[0] = "00" 

            if "pm" in message:
                return [str(int(time[0]) + 12), time[1]]
            else:
                return [time[0].rjust(2, "0"), time[1]]
                

    except ValueError:
        return False

    # meridiem based detection (am, pm)
    meridiems = ["am", "pm", "a.m.", "p.m.", "a.m", "p.m"]
    for meridiem in meridiems:
        if meridiem not in message:
            continue

        # Check if meridiem is seperated from time
        if meridiem in message.split(' '):
            message = message.split(' ')
            index = message.index(meridiem)

            hour = message[index-1].zfill(2)
            if not hour.isdigit():
                return False

            

        # Combined with time
        else:
            index = message.index(meridiem)
            hour = message[index-2:index].replace(" ", "0")

            if hour == "":
                hour = message[index-1:index].zfill(2)

            if not hour.isdigit() or hour == "00":
                return False

        if hour == "12" and "pm" in message:
            hour = "00"

        elif meridiem == "pm":
            hour = int(hour)
            hour += 12
            
        return [str(hour), "00"]

    return False


if __name__ == "__main__":
    GetTime("5:00")
    # Checks for first time startup
    if not path.exists("secret.json"):
        db = {
            "Bot": input("Bot Token: "),
            "Status": "10-4 Soldier",
            "Admins": [input("What is your Discord client ID: ")]
        }

        json.dump(db, open("secret.json", 'w'), indent=4)

    else:
        db = json.load(open("secret.json", 'r'))

    Token = db["Bot"]
    OnReadyStatus = db['Status']

    if not path.exists("timezones.json"):
        open("timezones.json", 'w').write('{"All": [], "RegisteredUsers":[]}')

    intend = discord.Intents.all()
    client = TimeBot(intents=intend)

    tree = app_commands.CommandTree(client)

    # Slash command to convert current time
    @tree.command(
            name="now",
            description="Slash command to convert current time"
    )
    async def now(interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=Commands.now(interaction.user.id)
        )


    # Slash command to register another users timezone
    @tree.command(
        name="registeruser",
        description="Register anouther users timezone (Or your own if you like being over complicated)")
    async def registerOther(interaction: discord.Interaction, targetid: str, timezone: str):
        try:
            user = await client.fetch_user(int(targetid))
            await interaction.response.send_message(
                Commands.registerOther(interaction.user.id, user, timezone)
            )
        except discord.errors.NotFound:
            await interaction.response.send_message(
                "That user ID is not valid!"
            )

    # Slash command used to register your own timezone
    @tree.command(
        name="register",
        description="Register your own timezone eg. America/New_York")
    async def registerOther(interaction: discord.Interaction, timezone: str):
        await interaction.response.send_message(
            Commands.registerSelf(interaction.user, timezone)
        )

    # Slash command to shutdown the bot
    @tree.command(
        name="shutdown",
        description="Shutsdown the Bot")
    async def shutdown(interaction: discord.Interaction):
        """Shuts down the bot."""
        if not Authorized(interaction.user.id, requireAdmin=IsAdminShutdown):
            return "You do not have the permission to do this."

        await interaction.response.send_message("Shutting Down!")
        await client.close()

    # Slash command to change the playing status
    @tree.command(
        name="status",
        description="Changes the status message of the bot")
    async def status(interaction: discord.Interaction, message: str):
        """Changes the status message of the bot"""

        if not Authorized(interaction.user.id, requireAdmin=IsAdminStatus):
            await interaction.response.send_message("You do not have the permission to do this.")
            return

        db = json.load(open("secret.json", 'r'))
        db['Status'] = message
        json.dump(db, open("secret.json", 'w'), indent=4)

        await client.change_presence(activity=discord.Game(name=message))
        await interaction.response.send_message("Changed Status!")

    @tree.command(
        name="report",
        description="Sends a system report.")
    async def sysReport(interaction: discord.Interaction):
        await interaction.response.send_message(
            Commands.sendReport(interaction, Version, client.latency)
        )

    client.run(Token)

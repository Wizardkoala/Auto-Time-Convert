import discord
import json
import sys
import time
import os
import datetime

if sys.version_info[1] <= 8:
    from backports.zoneinfo import ZoneInfo, ZoneInfoNotFoundError
else:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from settings import *

# Clears all unused timezones
def clenseTimezones():
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

# Handles admin commands
def Authorized(userid, requireAdmin=False) -> bool:
    userid = str(userid)

    if requireAdmin:
        if userid in json.load(open("secret.json", 'r'))["Admins"]:
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
def Format(i, userID: str) -> any:
    n = datetime.datetime.now()

    userTimezone = ZoneInfo(GetTimezone(userID))
    dt = datetime.datetime(n.year, n.month, n.day, int(i[0]), int(i[1]), tzinfo=userTimezone)

    return dt

class Commands():
    def registerOther(author: int, target: discord.Member, timezone: str) -> str:
        """Register a user to a timezone\n
        Eg. /registerother 267494392238047233 America/New_York"""

        if not Authorized(author, requireAdmin=IsAdminRegOther):
            return "You do not have the permission to do this."

        db = json.load(open("timezones.json", 'rb'))

        # Checks if the entered timezone is valid
        try:
            ZoneInfo(timezone)
        except ZoneInfoNotFoundError:
            return f'"{timezone}" is not a valid timezone.'

        if timezone not in db['All']:
            db['All'].append(timezone)

        db[str(target.id)] = {
            "name": target.name,
            "tz": timezone
        }

        if str(target.id) not in db['RegisteredUsers']:
            db['RegisteredUsers'].append(str(target.id))

        json.dump(db, open("timezones.json", 'w'), indent=4)
        clenseTimezones()
        return f"Registered user: {target.name}!"

    def registerSelf(author: discord.Member, timezone: str) -> None:
        """Alows users to register their own timezone\n
        eg. /register America/New_York"""

        if not Authorized(author.id, requireAdmin=IsAdminRegSelf):
            return "You do not have the permission to do this."

        db = json.load(open("timezones.json", 'rb'))

        # Checks if the entered timezone is valid
        try:
            ZoneInfo(timezone)
        except ZoneInfoNotFoundError:
            return f'"{timezone}" is not a valid timezone.'

        if timezone not in db['All']:
            db['All'].append(timezone)

        db[str(author.id)] = {
            "name": author.name,
            "tz": timezone
        }

        if str(author.id) not in db['RegisteredUsers']:
            db['RegisteredUsers'].append(str(author.id))

        json.dump(db, open("timezones.json", 'w'), indent=4)

        clenseTimezones()
        return "Registered user!"

    def sendReport(interaction: discord.Interaction, Version: str, latency: float) -> str:
        """Sends a debug report."""
        if not Authorized(interaction.user.id, requireAdmin=IsAdminReport):
            return "You do not have the permission to do this."

        report = [
            "Version %s" % Version,
            "Running on: Windows" if os.name == "nt" else "Running on: Unix-Based",
            "Latency: %ims" % int(latency * 1000),

            "Users num %i" % len(json.load(open("timezones.json", 'rb'))[
                "RegisteredUsers"]),

            "Timezone num: %i" % len(
                json.load(open("timezones.json", 'rb'))["All"]),
        ]
        return '\n'.join(report)

    

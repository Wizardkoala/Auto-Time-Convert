# Auto-Time-Convert

This is a project created to make the process of planning dates with people overseas a little easier on discord.
The bot automatically converts times that are sent in chat to the timezones other people have registered for themselves.
It can support a bunch of different formats a few examples are listed:

- 6pm
- 9:00 am
- 4:20 a.m.
- 19:45

It also does not matter if there are words before or after the time that was sent. For instance, `let's go at 4pm.` would be understood by the bot.

## Setup

### Creating a Discord Bot

1. Go to [#setting-up-users-timezone](https://github.com/Wizardkoala/Auto-Time-Convert/edit/master/README.md#setting-up-users-timezone) and create a new application.
2. Under the 'Bot' tab click add bot.
3. Enable all Privileged Gateway Intents intents.
4. Copy the Bot token and save it in a safe place, NEVER share this token.
5. Invite the Discord bot to your server with the Administrator permission to ensure it can see all channels.

### Setting up the code

1. Download and extract the source code.
2. Execute `python -m pip3 install -r requirements.txt` in the project directory.
3. Run `discordClient.py`.
4. When prompted type in the Bot token you saved earlier.
5. Type in your own discord accounts user-id (Getting a user id is explained in #setting-up-users-timezone) this id will serve as the first admin
Anyone who is an admin will be able to shutdown the bot and gain information about the machine it is running on.
6. To add more admins open the `Secret.json` file and add the user's id in the list seperating them by a comma (,).

### Setting up users timezone

Keep in mind anyone can change there own timezone with `/register <Timezone>`. To setup someone elses timezone type: `/registeruser <UserId> <Timezone>`

- UserId: This is retreived by right-clicking on someone in Discord with developer mode enabled and selecting, "Copy ID"
- Timezone: This is the timezone the user is in. eg. America/Denver

## Commands

All commands are now slash commands. Simply type a slash and click on the bot to get a list and description of all commands.

## Common Timezones

### America

---

- Eastern Time: America/New_York
- Centeral Time: America/Chicago
- Mountain Time: America/Denver
- Pacific Time: America/Los_Angeles

### Europe

---

- United Kingdom: Europe/London
- Centeral Europe: Europe/Paris
- Eastern Europe: Europe/Moscow

### Asia

---

- China: Asia/Shanghai
- Singapore: Asia/Singapore
- Japan: Asia/Tokyo

## Future Plans

- Improve comments
- Build a .exe version for ease of use
- Host a public use version

## Update 1.9

- `5:00am` as the only content of a message is now recognized
- Fixed `5:00` time format
- Defaulted `5:00` format to 24 hour format instead of assuming PM
- Added `A.M` and `A.M.` time formats
- Updated discord.py package to 2.1.1
- Updated tzdata package to 2022.7

## Update 1.8

- Slash commands!
  - Added discord.py slash command tree.
  - Moved command logic to `commands.py` with the exception of `/shutdown`.
  - Minor rework to the logic of many commands.
- Complete rework of time extraction
- Updated to discord.py 2.0 (2.0.1)
- Replaced "no registered timezone" warning with an emoji reaction
- Removed command customization in `settings.py`

## Update 1.7

- Improved the look of time conversions using embeds.
- Moved all user configurable settings to `settings.py`.
- Allowed users to change wether a command should be admin-only or not.
- Cleaned up the code by moving commands to their own class.
- Removed one-time passwords for admin commands
- Added admin system
- Changed inital setup. This will require you to delete your existing `Secret.json` file and reset it up. `timezones.json` files should work just fine.
- Put a settings in `Secret.json` that saves the current status message and restores it next boot.

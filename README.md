# Auto-Time-Convert
This is a project created make the process of planing dates with people over-seas a little easier on discord. 
The bot automatically converts times that are sent in chat to those that other people of registed.
It can support a bunch of different formats a few examples are listed:
- 5pm
- 3:30 am
- 2:00 (In this case it would assume pm)

## Setup
### Creating a Discord Bot
1. Go to https://discord.com/developers/applications and create a new application.
2. Under the 'Bot' tab click add bot.
3. Copy the Bot token and save it in a safe place, NEVER share this token.
4. Invite the Discord bot to your server with the Administrator permission to ensure it 
can see all channels.
### Setting up the code
1. Download and extract the source code.
2. Run `pip3 install -r requirements.txt` in the codes directory.
3. Run the `discordClient.py` file.
4. When prompted type in the Bot token you saved earlier.
5. Type in your own discord accounts user-id (Getting a user id is explained in the "Setting up users timezone" section) this id will serve as the first admin
Anyone who is an admin will be able to shutdown the bot and gain information about the machine it is running on.
6. To add more admins open the Secret.json file and add the users id in the list seperating them by a comma. This will be imporved later.
### Setting up users timezone
Keep in mind anyone can change there own timezone with `TRegister! <Timezone>`. To setup someone elses timezone type: `TRegisterOther! <UserId> <Timezone>`
- UserId: This is retreived by right-clicking on someone in Discord with developer mode enabled and selecting, "Copy ID"
- Timezone: This is the timezone the user is in. eg. America/Denver

## Commands
All of these commands are the defaults and can be changed in `settings.py`
- `TReport!`
    - An admin-only command that reports details of the bot and the machine it is running on
- `TPlay! <Message>`
    - Admin-only command that changes the status of the bot
- `TEnd!`
    - Shuts down the bot
- `TRegister! <Timezone>`
    - Register the user who sent the message's timezone
- `TRegisterOther! <UserID> <Timezone>`
    - Sets anouther users timezone.  This is explained further in setting up timezones section

## Update 1.7
- Improved the look of time conversions using embeds.
- Moved all user configurable settings to `settings.py`.
- Allowed users to change wether a command should be admin-only or not.
- Cleaned up the code by moving commands to their own class.
- Removed one-time passwords for admin commands
- Added admin system
- Changed inital setup. This will require you to delete your existing `Secret.json` file and reset it up. `timezones.json` files should work just fine.
- Put a settings in `Secret.json` that saves the current status message and restores it next boot.
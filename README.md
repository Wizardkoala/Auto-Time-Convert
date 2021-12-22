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
3. Copy the Bot token and safe it in a safe place, NEVER share this token.
### Setting up the code
1. Download and extract the source code.
2. Run `pip3 install -r requirements.txt` in the codes directory.
3. Run the `discordClient.py` file.
4. When prompted type in the Bot token you saved earlier.
5. Copy the `TOTP:` token it provides and save it in a safe space. 
Anyone you share this with will be able to shutdown the bot and gain information about the machine it is running on
6. Setup the TOTP token in any authenticator app of your choosing.
### Setting up users timezone
Keep in mind anyone can change anyone elses timezone if they know the syntax. To setup anyones timezone type: `levRegister! <UserId> <Friendly Name> <Timezone>`
- UserId: This is retreived by right-clicking on someone with developer mode enabled and selecting, "Copy ID"
- Friendly Name: This is just a name so you can identify them in the timezones.json file if needed
- Timezone: This is the timezone the user is in. eg. America/Denver

## Commands
- levReport! 6-digit_OTP
- - An admin-only command that reports details of the bot and the machine it is running on
- levPlay! 6-digit_OTP Message
- - Admin-only command that changes the status of the bot
- levEnd! 6-digit_OTP
- - Shuts down the bot
- levRegister! User_ID Friendly_Name Timezone
- - This is explained in the "Setting up users timezone" section

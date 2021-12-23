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
5. Copy the `TOTP:` token it provides and save it in a safe space. 
Anyone you share this with will be able to shutdown the bot and gain information about the machine it is running on.
6. Setup the TOTP token in any authenticator app of your choosing.
### Setting up users timezone
Keep in mind anyone can change there own timezone with `TRegister! <Timezone>`. To setup someone elses timezone type: `TRegisterOther! <6-digit OTP> <UserId> <Friendly Name> <Timezone>`
- UserId: This is retreived by right-clicking on someone with developer mode enabled and selecting, "Copy ID"
- Friendly Name: This is just a name so you can identify them in the timezones.json file if needed
- Timezone: This is the timezone the user is in. eg. America/Denver

## Commands
All of these commands are the defaults and can be changed in `discordClient.py`
- `TReport! <6-digit OTP>`
    - An admin-only command that reports details of the bot and the machine it is running on
- `TPlay! <6-digit OTP> <Message>`
    - Admin-only command that changes the status of the bot
- `TEnd! <6-digit OTP>`
    - Shuts down the bot
- `TRegister! <Timezone>`
    - Register the user who sent the message's timezone
- `TRegisterOther! <6-digit OTP> <UserID> <Friendly Name> <Timezone>`
    - Sets anouther users timezone.  This is explained further in setting up timezones section

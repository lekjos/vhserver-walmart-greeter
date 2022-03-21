# Valheim Server Walmart Greeter
This script posts in Discord whenever someone joins or leaves your Valheim server. Users are identified by their SteamID and greeted using their realname or personaname attribute. If you recognize a steamID and would like to customize the user's name (e.g. your friend didn't enter their real name into steam), you can add them to the Known ID's using `greeter_config.ini` and customize their name.

Users who are in the Known ID's list are sometimes greeted in a more familiar way.

To customize the greetings, edit `discord_post.generate_greeting`.

## Background
I don't really game much anymore, but I was asked to host a Valheim Server on my Ubuntu Server. After building a really bad hut in the game and hunting a few deer, I got bored and decided to make Discord Bot that greeted my friends on the server when they joined or left the game. 

## Setup Instructions
1. Fork this repo and clone to your Server
2. Create a Discord Webhook, note the URL
3. Update the following variables in `log_update_watchdog.sh`:
    1. `LOG_PATH`: Should be the path to your instance of vhserver-console.log,
    2. `RECENT_PATH`: Is where the shell script will grep to, this is a new file created by the script
    3. `PROGRAM_PATH`: Points to `discord_post.py`, where you cloned the repo to
4. Update `greeter_config.ini`:
    1. `RECENT_LOG` should match `RECENT_PATH` above.
    2. `WEBHOOK_URL` should be added for whatever channel you want to post to in Discord.

## Adding Known Users
To add a known user, add a line under the `[Known Users]` heading, following the format shown in the comment in `greeter_config.ini`

## Disclaimer
This software is provided with no support or warranty, use at your own risk. I no longer host a Valheim server, so things may not work correctly.
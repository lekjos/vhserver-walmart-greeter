from discord_webhook import DiscordWebhook
from client_identifier import get_username
import random
import requests
from datetime import date, timedelta, datetime
import re

vhlog = '/home/***REMOVED***/log/console/recent.log'
lastupdated = '/home/***REMOVED***/source/vhserver_tools/last_updated.txt'

def get_username(steam_id):
    """
    Returns dict of persona name and name from Steam Player Summaries API
    """
    response = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=***REMOVED***&format=json&steamids=' + str(steam_id))
    #print(response.text)
    if 'realname' in response.json()['response']['players'][0]:
        name = response.json()['response']['players'][0]['realname']
    else:
        name = response.json()['response']['players'][0]['personaname']
    context = {
        'personaname': response.json()['response']['players'][0]['personaname'],
        'name': name
    }
    #print(context)
    return context

def check_name(steam_id):
    """
    Checks if user steam id is known, then returns user dict:
        {
            'status': <bool> (Is user recognized),
            'name': <str>
            'personaname': <str>
        }
    If username is unknown, looks up user via steam ID
    """
    # To add a known ID update this dict:
        # '<STEAM_ID:int>': ['<NAME>', '<PERSONA_NAME>'] 
        # Where persona name is their Steam ID
    known_id = {
        '***REMOVED***': ['***REMOVED***', '***REMOVED***'],
        '***REMOVED***': ['***REMOVED***', '***REMOVED***'],
        '***REMOVED***': ['***REMOVED***', '***REMOVED***'],
        '***REMOVED***': ['***REMOVED***', '***REMOVED***'],
        '***REMOVED***': ['***REMOVED***', '***REMOVED***']
    }
    if str(steam_id) in known_id:
        name = known_id[str(steam_id)][0]
        personaname = known_id[str(steam_id)][1]
        status = True
    else:
        response = get_username(steam_id)
        name = response['name']
        personaname = response['personaname']
        status = False
    user_dict = {
        'status': status,
        'name': name,
        'personaname': personaname,
    }
    return user_dict


def generate_greeting(steam_id, incoming):
    """
    Generates random greeting after looking up steam ID.

    args
        steam_id: <int>
        incoming: <bool> (true if user joining server, else false)
    
    returns:
        greeting: <str>
    """

    user = check_name(steam_id)
    status = user['status']
    name = user['name']
    personaname = user['personaname']
    #print(status)

    if incoming == True:
        greetings = [
            f'Hello {name}, or is it {personaname}? I don\'t know... I don\'t get paid enough.',
            f'Hello {name}, toilet paper is on isle 24.',
            f'Welcome to Walmart, {name}!',
            f'Enjoy shopping at Walmart, {name}!',
            f'Hi, {name} how can-- HEY, NO RIDING ON THE CARTS!',
            f'What do you want, {personaname}?',
            f'Yo, {personaname}, want to hear about the time i ran over a cat?',
            f'We don\'t sell them, but possums are super tasty, {name}',
            f'Hey {name}, Have you ever seen a grown Walmart Greeter Naked?',
        ]
        if status == True:
            greetings.append(f'Welcome back {name}!')
            greetings.append(f'Wonderful seeing you again, {name}!')
            greetings.append(f'Lookin\' fly today, {name}')
    else: 
        greetings = [
            f'Goodbye {name}',
            f'Thank you, come again {name}',
            f'Thank you for shopping at Walmart, see you next time, {name}',
            f'You better not have anything you didn\'t pay for {name}'
        ]
        if status == True:
            greetings.append(f'I hate to watch {name} go, but I love to watch {name} leave...')
            greetings.append(f'See ya {name}, wouldn\'t wanna be ya though.')


    result = greetings[random.randint(0, len(greetings)-1)]
    return result

# greeting = generate_greeting(steam_id, False)
#print(greeting)


def extract_date(line):
    """Return a datetime from a log line"""
    fmt = '%m/%d/%Y %H:%M:%S'
    return datetime.strptime(line[:19], fmt)

## get current time and last updated time
end_date = datetime.now()
date_file = open(lastupdated)
start_date = datetime.strptime(date_file.read(19), '%m/%d/%Y %H:%M:%S')
date_file.close()
changed = False

## Prevent posting status more than a minute old
## Useful if listener is started when there are a bunch of old logs
if end_date - start_date > timedelta(seconds=60):
    start_date = end_date - timedelta(seconds=60)

## check for updates and post to discord if any
with open(vhlog) as f:
    # from https://stackoverflow.com/questions/18562479/what-is-the-quickest-way-to-extract-entries-in-a-log-file-between-two-dates-in-p
    for line in f:
        if start_date < extract_date(line) < end_date:
            client_id = re.search(r'\d+$', line).group(0)
            if "Closing socket" in line:
                incoming = False
            elif "Got handshake from client" in line:
                incoming = True
            greeting = generate_greeting(client_id, incoming)
            webhook = DiscordWebhook(url='***REMOVED***', content=greeting)
            response = webhook.execute()
            changed = True


## set last_updated time to end_date
if changed == True:
    date_file = open(lastupdated, "w")
    date_file.write(end_date.strftime('%m/%d/%Y %H:%M:%S'))
    date_file.close()







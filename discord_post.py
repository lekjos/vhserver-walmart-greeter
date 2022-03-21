from configparser import ConfigParser
from datetime import timedelta, datetime
from discord_webhook import DiscordWebhook
import os, random, requests, re


def get_username(steam_id:int):
    """
    Returns dict of persona name and name from Steam Player Summaries API
    """
    response = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=***REMOVED***&format=json&steamids=' + str(steam_id))
    if 'realname' in response.json()['response']['players'][0]:
        name = response.json()['response']['players'][0]['realname']
    else:
        name = response.json()['response']['players'][0]['personaname']
    user_dict = {
        'personaname': response.json()['response']['players'][0]['personaname'],
        'name': name
    }
    return user_dict

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
    
    if str(steam_id) in known_ids:
        name = known_ids[str(steam_id)][0]
        personaname = known_ids[str(steam_id)][1]
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
            f'Yo, {personaname}, want to hear about the time I ran over a cat?',
            f'We don\'t sell them, but possums are super tasty, {name}',
            f'Hey {name}, Have you ever seen a grown Walmart Greeter Naked?',
        ]
        if status == True:
            greetings.append(f'Welcome back {name}!')
            greetings.append(f'Wonderful seeing you again, {name}!')
            greetings.append(f'Lookin\' fly today, {name}')
            greetings.append(f'Welcome back {name}... I\'m watching you...')
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

def extract_date(line):
    """Return a datetime from a log line"""
    fmt = '%m/%d/%Y %H:%M:%S'
    return datetime.strptime(line[:19], fmt)

# parse config file for paths and known ids
config = ConfigParser()
config.read('greeter_config.ini')
vhlog = config['Paths']['RECENT_LOG']
lastupdated = config['Paths']['LAST_UPDATED']
webhook_url = config['Discord'].get('WEBHOOK_URL',False)
suppress_old = True if config['Settings']['SUPPRESS_OLD'] == 'True' else False
known_ids = dict()
for key in config['Known Users']:
    known_ids[key] = [w.strip() for w in str(config['Known Users'][key]).split(',')]

## get current time and last updated time
end_date = datetime.now()

# create lastupdated file if none exists
if not os.path.exists(os.path.abspath(lastupdated)):
    print('Creating last_updated.txt')
    os.makedirs(os.path.dirname(lastupdated),exist_ok=True)
    new_file = open(lastupdated, 'a').close()


with open(lastupdated, 'r') as date_file:
    if os.stat(lastupdated).st_size > 0:
        data = date_file.read(19)
        start_date = datetime.strptime(data, '%m/%d/%Y %H:%M:%S')
    else:
        start_date = datetime(2019,1,1)
    changed = False

## Prevent posting status more than a minute old
## Useful if listener is started when there are a bunch of old logs
if suppress_old:
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
            
            if webhook_url:
                print('Sending webhook:',greeting)
                webhook = DiscordWebhook(url=webhook_url, content=greeting)
                response = webhook.execute()
            else:
                print('No Webhook_URL specified, didn\'t send greeting:', greeting)
            changed = True


## set last_updated time to end_date
if changed == True:
    date_file = open(lastupdated, "w")
    date_file.write(end_date.strftime('%m/%d/%Y %H:%M:%S'))
    date_file.close()
else:
    print(f'No changes found. Suppress old messages: {suppress_old}')







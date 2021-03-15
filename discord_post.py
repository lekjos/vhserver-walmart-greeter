from discord_webhook import DiscordWebhook
from client_identifier import get_username
import random
import requests



def get_username(steam_id):

    response = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=***REMOVED***&format=json&steamids=' + str(steam_id))
    print(response.text)
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
    context = {
        'status': status,
        'name': name,
        'personaname': personaname,
    }
    #print(context)
    return context






#webhook = DiscordWebhook(url='***REMOVED***', content='test message')
#response = webhook.execute()

def generate_greeting(steam_id):

    user = check_name(steam_id)
    status = user['status']
    name = user['name']
    personaname = user['personaname']
    #print(status)

    greetings = [
        f'Hello {name}, or is it {personaname}? I don\'t know... I don\'t get paid enough.',
        f'Hello {name}, toilet paper is on isle 24.',
        f'Welcome to Walmart, {name}!',
        f'Enjoy shopping at Walmart, {personaname}!',
        f'Hi, {name} how can-- HEY, NO RIDING ON THE FRONT OF THE CARTS!',
    ]
    if status == True:
        greetings.append(f'Welcome back {name}!')
        greetings.append(f'Lookin\' fly today, {personaname}')

    result = greetings[random.randint(0, len(greetings)-1)]
    return result

#steam_id = ***REMOVED*** #***REMOVED***
#steam_id = ***REMOVED*** #***REMOVED***
#steam_id = ***REMOVED*** #***REMOVED***
#steam_id = ***REMOVED*** #***REMOVED***
#steam_id = ***REMOVED*** #***REMOVED***


print(generate_greeting(steam_id))
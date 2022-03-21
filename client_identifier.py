import requests

def get_username(steam_id):
    response = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=***REMOVED***&format=json&steamids=' + str(steam_id))
    
    context = {
        'personaname': response.json()['response']['players'][0]['personaname'],
        'name': response.json()['response']['players'][0]['realname']
    }
    return context


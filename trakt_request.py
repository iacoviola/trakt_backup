import requests
import json
import os

def create_data_files(usr, root):
    global username
    username = usr
    
    global url
    url = f'{url}/{username}'

    global root_path
    root_path = root

    get_watched_movies()
    get_watched_episodes()
    get_watched_shows()
    get_movies_ratings()
    get_episodes_ratings()
    get_shows_ratings()
    get_seasons_ratings()
    get_movies_history()
    get_episodes_ratings()
    get_movies_watchlist()
    get_episodes_history()
    get_shows_watchlist()
    get_movies_collection()
    get_episodes_collection()
    get_shows_collection()
    get_user_stats()

# Get data from trakt api by specifying the action and type of media
def get(action, type):
    print(f'Obtaining: {url}/{action}/{type}')
    response = requests.get(f'{url}/{action}/{type}?limit=100000' , headers=headers)

    if response.status_code == 404:
        raise Exception(f'Error: user {username} not found')
    elif response.status_code != 200:
        print(f'An error as occured with code: {response.status_code} for operation {action}/{type}')
        return
    
    if response.json() == []:
        print(f'No {type} found in {action}')
        return

    file_watched = open(os.path.join(root_path, f'{action}_{type}.json'), 'w')
    file_watched.write(json.dumps(response.json(), separators=(',', ':'), indent=4))
    file_watched.close()
    print(f'Obtained: {url}/{action}/{type}')

def get_watched_movies():
    get('watched', 'movies')

def get_watched_episodes():
    get('watched', 'episodes')

def get_watched_shows():
    get('watched', 'shows')

def get_movies_ratings():
    get('ratings', 'movies')

def get_episodes_ratings():
    get('ratings', 'episodes')

def get_shows_ratings():
    get('ratings', 'shows')

def get_seasons_ratings():
    get('ratings', 'seasons')

def get_movies_history():
    get('history', 'movies')

def get_episodes_history():
    get('history', 'episodes')

def get_movies_watchlist():
    get('watchlist', 'movies')

def get_shows_watchlist():
    get('watchlist', 'shows')

def get_movies_collection():
    get('collection', 'movies')

def get_episodes_collection():
    get('collection', 'episodes')

def get_shows_collection():
    get('collection', 'shows')

def get_user_stats():
    get('stats', '')

# Trakt request base url
url = 'https://api.trakt.tv/users'
# Backup absolute path
root_path = ''
# Trakt username to get data from
username = ''

# Trakt request required headers
headers = {
    # Trakt return a json response
    'Content-Type': 'application/json',
    # Trakt api version
    'trakt-api-version': '2',
    # Trakt api key
    'trakt-api-key': '' # Your trakt api key
}
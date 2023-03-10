import requests
import json
import os


class TraktRequest:
    def __init__(self, api_key, username, url, root_path):
        self.username = username
        self.url = f"{url}/{self.username}"
        self.root_path = root_path
        # Trakt request required headers
        self.headers = {
            # Trakt return a json response
            "Content-Type": "application/json",
            # Trakt api version
            "trakt-api-version": "2",
            # Trakt api key
            "trakt-api-key": api_key,  # Your trakt api key
        }

    def create_data_files(self):
        self.get_watched_movies()
        self.get_watched_episodes()
        self.get_watched_shows()
        self.get_movies_ratings()
        self.get_episodes_ratings()
        self.get_shows_ratings()
        self.get_seasons_ratings()
        self.get_movies_history()
        self.get_episodes_ratings()
        self.get_movies_watchlist()
        self.get_episodes_history()
        self.get_shows_watchlist()
        self.get_movies_collection()
        self.get_episodes_collection()
        self.get_shows_collection()
        self.get_user_stats()

    # Get data from trakt api by specifying the action and type of media
    def get(self, action, endpoint_type):
        print(f"Obtaining: {self.url}/{action}/{endpoint_type}")
        response = requests.get(f"{self.url}/{action}/{endpoint_type}?limit=100000", headers=self.headers)

        if response.status_code == 404:
            raise Exception(f"Error: user {self.username} not found")
        elif response.status_code != 200:
            print(f"An error as occurred with code: {response.status_code} for operation {action}/{endpoint_type}")
            return

        if not response.json():
            print(f"No {endpoint_type} found in {action}")
            return

        file_watched = open(os.path.join(self.root_path, f"{action}_{endpoint_type}.json"), "w")
        file_watched.write(json.dumps(response.json(), separators=(",", ":"), indent=4))
        file_watched.close()
        print(f"Obtained: {self.url}/{action}/{endpoint_type}")

    def get_watched_movies(self):
        self.get("watched", "movies")

    def get_watched_episodes(self):
        self.get("watched", "episodes")

    def get_watched_shows(self):
        self.get("watched", "shows")

    def get_movies_ratings(self):
        self.get("ratings", "movies")

    def get_episodes_ratings(self):
        self.get("ratings", "episodes")

    def get_shows_ratings(self):
        self.get("ratings", "shows")

    def get_seasons_ratings(self):
        self.get("ratings", "seasons")

    def get_movies_history(self):
        self.get("history", "movies")

    def get_episodes_history(self):
        self.get("history", "episodes")

    def get_movies_watchlist(self):
        self.get("watchlist", "movies")

    def get_shows_watchlist(self):
        self.get("watchlist", "shows")

    def get_movies_collection(self):
        self.get("collection", "movies")

    def get_episodes_collection(self):
        self.get("collection", "episodes")

    def get_shows_collection(self):
        self.get("collection", "shows")

    def get_user_stats(self):
        self.get("stats", "")

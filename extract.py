import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta

def return_dataframe():
    scope = "user-read-recently-played"
    client_id = "Your client_id here" 
    client_secret = "Your client_secret"
    
    '''If you are developing your application locally, you can use a redirect URI with localhost.
    For example, you can set the redirect URI to http://localhost:8888/callback. This is a common choice during development and testing.'''
    
    redirect_uri = "http://localhost:8888/callback"  
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))
    
    today = datetime.now()
    three_days_ago = today - timedelta(days=3)

    recently_played = sp.current_user_recently_played(limit=50) #Get only 50 tracks from the last 3 days.

    if not recently_played["items"]:
        print("No songs played in the last 3 days.")
        return None

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for item in recently_played["items"]:
        track = item["track"]
        played_at = datetime.strptime(item["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ") #Converting spotify api response (string) into datetime format for comparison in the next block of code.
        
        if played_at >= three_days_ago:
            song_names.append(track["name"])
            artist_names.append(track["artists"][0]["name"])
            played_at_list.append(item["played_at"])
            timestamps.append(played_at)

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }
    
    song_df = pd.DataFrame(song_dict)

    return song_df

print(return_dataframe())

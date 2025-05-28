"""
spotify_rising_artists.py

Contains functions to search for specific "on the rise" Spotify created playlists,
extract artist data from those playlists, and deduplicate artists across playlists.

"""
import requests
import time
from src.utils.get_genre import get_artist_genres
from src.auth import get_auth_headers
from src.utils.dedup_artists import deduplicate_artists

def scrape_spotify_created_playlists(playlist_id, playlist_name, headers, max_retries=3):
    """
    Extracts artist metadata from a Spotify-curated playlist.

    Args:
        playlist_id (str): The Spotify playlist ID
        playlist_name (str): Playlist name for tagging
        headers (dict): Authorization headers for the Spotify API
        max_retries (int): Max number of retry attempts on 429 errors

    Returns:
        list of dict: Each dict includes artist name, ID, and playlist source
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    
    retries = 0

    while retries <= max_retries:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            break
        
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            print(f"ERROR: Status Code 429. Sleeping for {retry_after} seconds...")
            time.sleep(retry_after)
            retries += 1
        
        else:
            raise Exception(f"ERROR: Failed to fetch playlist {playlist_name}. Status: {response.status_code}. Response: {response.text}")
    
    else:
        raise Exception(f"ERROR: Exceeds max retries on playlist {playlist_name} due to repeated 429s.")
    
    items = response.json().get("items", [])

    seen = set()
    artists = []

    for item in items:
        try:
            artist = item['track']['artists'][0] #Pulls the first listed artist
            artist_id = artist["id"]
            if artist_id in seen:
                continue

            genres = get_artist_genres(artist["id"], headers)

            artists.append({
                "artist": artist["name"],
                "id": artist["id"],
                "genres": genres,
            })

        except (TypeError, KeyError): #Skip over any tracks that are missing artist info or are formatted oddly
            continue
    
    print(f"Tracks pulled from '{playlist_name}': {len(items)}")

    return artists

def artist_by_playlistIDs(playlist_dict):
    """
    Pulls artists directly from known Spotify playlist IDs.

    Args:
        playlist_dict (dict): Dict of {playlist_name: playlist_id}

    Returns:
        list of dict: Flattened list of all artists found, tagged with source playlist.
    """
    # This function calls the access token using Client Credentials Flow
    headers = get_auth_headers() 

    #This function calls the access token using Authorization Code Flow
    # headers = {"Authorization": "Bearer BQD47olRLZOIGRnmivqb6wntOug6_OqBAKtBc95rrt5xT-fhoZ4S7AoZSKJpvQaR7SYJDe57gWxlFnLiX59Vu3q570K6aFJ49TBrrP0QSkoGvP7Cm1kEZsZNmOeLsvfvnzr8khGM4sxUUB5_-WaGcVOeU4mK4ans4exdDLR9TJ8JwpJmVWA2fsGXNqxIUjh8TLKMQZb8tRHbgfZ8_E2vOmdsNue9EYOFnSjaHlhn"}
    all_artists = []

    for playlist_name, playlist_id in playlist_dict.items():
        print(f"INFO: Scraping '{playlist_name}' (ID: {playlist_id})")
        
        try:
            artists = scrape_spotify_created_playlists(playlist_id, playlist_name, headers)
            print(f"INFO: Found {len(artists)} artists in '{playlist_name}'")
            all_artists.extend(artists)
        
        except Exception as e:
            print(f"ERROR: Failed to scrape '{playlist_name}': {e}")
        
        time.sleep(1)

    print(f"INFO: Total collected before deduplication: {len(all_artists)}")

    deduped_artists = deduplicate_artists(all_artists)
    print(f"INFO: Total after deduplication: {len(deduped_artists)}")

    return deduped_artists
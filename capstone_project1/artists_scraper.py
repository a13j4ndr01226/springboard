"""
artists_scraper.py

Main script to collect rising artist data from selected Spotify playlists and
store them in a local JSON file.

This script:
- Loads a local cache to avoid redundant Spotify API calls
- Extracts artist metadata from playlists known for rising artists
- Saves the scraped data in JSON format
- Updates the cache after execution
"""

import json
import sys
from pathlib import Path

# Add src directory to Python path so modules can be imported
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from spotify_rising_artists import artist_by_playlistIDs
from utils.genre_cache import load_cache, save_cache 

#These are playlists that have "on the rise" artists
playlist_dict = {
                    # "Up-and-Coming Mix": "37i9dQZF1EIem8Lf3VpAdy", 
                    # "Up-and-Coming Country Mix": "37i9dQZF1EIgWAyzVf4UMk",
                    # "Up-and-Coming Pop Mix": "37i9dQZF1EIdVRWeLnQ9MD",
                    # "Dance Rising" : "37i9dQZF1DX8tZsk68tuDw", 
                    # "Electronic Rising": "37i9dQZF1DX8AliSIsGeKd",
                    # "Pop Rising": "37i9dQZF1DWUa8ZRTfalHk", 
                    # "R&B Rising": "37i9dQZF1DWUbo613Z2iWO",
                    # "Viral Hits": "37i9dQZF1DX2L0iB23Enbq", 
                    # "Viral 50 USA": "37i9dQZEVXbKuaTI1Z1Afx",
                    # "Fresh Finds": "37i9dQZF1DWWjGdmeTyeJ6",
                    # "Fresh Finds Dance": "37i9dQZF1DX6bBjHfdRnza", 
                    # "Fresh Finds:EDM": "5CweKpXcP6I3p95u8zgIyb",
                    # "Fresh Finds Country": "37i9dQZF1DWYUfsq4hxHWP",
                    # "New Music Friday": "37i9dQZF1DX4JAvHpjipBk", 
                    # "Best New Artist": "37i9dQZF1DX2SaVGyZ9hsv", 
                    # "All New Dance": "37i9dQZF1DXa41CMuUARjl", 
                    # "All New Indie": "37i9dQZF1DXdbXrPNafg9d",
                    # "All New Country": "37i9dQZF1DWVn8zvR5ROMB",
                    # "New Dance Pop": "37i9dQZF1DWWOGXILUAh53"
                    "Hesh Mix": "3jLfw7Z8VOpsBrCjDNuRzm"
}

# Output path
output_file = Path("data/spotify_rising_artists.json")

def main():
    print("Loading cache...")
    load_cache() 
    print("Collecting artists from rising playlists...")
    
    artists = artist_by_playlistIDs(playlist_dict)

    output_file.parent.mkdir(exist_ok=True)  # Create /data if missing
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(artists, f, indent=2)

    print(f"\n Saved {len(artists)} artists to {output_file.resolve()}")
    print("Saving cache...")
    save_cache()  

if __name__ == "__main__":
    main()

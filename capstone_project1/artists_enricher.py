"""
artists_enricher.py

Main script to enrich artist data with Google Trends daily trend scores across
multiple U.S. regions over the past two years.

The script:
- Loads a list of artists from a JSON file
- Retrieves daily trend scores for each artist per region using the Google Trends API
- Adds this trend data to each artist record
- Saves the enriched data to a new JSON file
"""

import json
import time
import random
from pathlib import Path
from src.google_trends import get_trend_score_2y_daily
from src.utils.trends_cache import load_cache, save_cache

INPUT_FILE = Path("data/spotify_rising_artists.json")
OUTPUT_FILE = Path("data/test_spotify_rising_with_trends.json")

#Add or change regions as needed. Current project focuses on the Atlantic City Area.
regions = {
    "nj": "US-NJ",
    "ny": "US-NY",
    "pa": "US-PA"
}

def add_google_trends_score(artists):
    """
    Enriches artist records with 2 years of daily Google Trends scores for specified regions.

    Parameters
    artists : list of dict

    Returns
    list of dict
    """
    for artist in artists:
        name = artist.get("artist", "")
        print(f"PROCESSING: {name}")
        
        for region_label, geo in regions.items():
            daily_scores = get_trend_score_2y_daily(name, geo) #For each region, daily scores get scraped
        
            if daily_scores:
                artist[f"daily_trends_{region_label}_2y"] = daily_scores
                print(f"TOTAL{region_label.upper()} 2Y Daily = {len(daily_scores)} entries")
            else:
                print(f"WARNING: No data returned for {name} in {region_label}")
        
        time.sleep(random.uniform(30, 60))  # Global throttle between artists

    
    return artists

def main():
    """
    Main function that loads rising artist, adds google trends, 
    and saves data as JSON file.

    - Loads raw artist data from the input JSON file
    - Loads cached Google Trends data to avoid redundant API calls
    - Enriches the artist data with Google Trends scores across selected regions
    - Saves the enriched data to the output JSON file
    """
    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f: #uses the deduped artist list 
        artists = json.load(f)

    print(f"Loaded {len(artists)} artists")
    
    load_cache()
    enriched = add_google_trends_score(artists)
    save_cache()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

    print(f"Saved enriched artist data to {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()

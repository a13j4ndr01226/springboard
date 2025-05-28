"""
trend_scraper.py

Fetches and caches 2 years of daily Google Trends interest scores
for musical artists across specified regions. Runs script in chunks to aovid getting blocked
by Google Trends API limitations

"""
import random
import time
from datetime import datetime, timedelta
from pytrends.request import TrendReq
from src.utils.trends_cache import get_cached_score, set_cached_score

pytrends = TrendReq(hl='en-US', tz=480)  # Pacific time, timestamps irrelevant for daily data

from datetime import datetime, timedelta

def get_trend_score_2y_daily(artist_name, geo):
    """
    Orchestrates chunked requests to Google Trends.
    Due to API limits, the 730-day range is split into ~260-day chunks, which are 
    queried sequentially and merged.

    Parameters
    artist_name : str
        The name of the artist to search for on Google Trends.
    geo : str
        The region code (e.g., 'US-NY') for location-specific interest scores.

    Returns
    dict
        Dictionary where keys are date strings (YYYY-MM-DD) and values are daily trend scores.
        Example: {'2023-05-26': 34, '2023-05-27': 40, ...}
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=730)
    chunk_size = 260  # Google allows up to ~270 days of daily granularity

    combined_scores = {}

    chunk_start = start_date
    chunk_index = 0

    while chunk_start < end_date:
        chunk_end = min(chunk_start + timedelta(days=chunk_size), end_date)
        tf_range = f"{chunk_start.strftime('%Y-%m-%d')} {chunk_end.strftime('%Y-%m-%d')}"
        label = f"daily2y_{chunk_index}"

        print(f"Chunk {chunk_index + 1}: {tf_range}")

        chunk_scores = get_trend_score(artist_name, geo, label, tf_range)
        if chunk_scores:
            combined_scores.update(chunk_scores)

        chunk_start = chunk_end + timedelta(days=1)
        chunk_index += 1
        time.sleep(random.uniform(5, 10))

    return combined_scores


def get_trend_score(artist_name, geo, timeframe_label, timeframe_range, max_retries=3):
    """
    Fetches interest-over-time data for a given artist from Google Trends for a specific
    time window and geographic region. Results are cached to minimize redundant requests.

    Parameters
    artist_name : str
        The artist name to query.
    geo : str
        The region code (e.g., 'US-PA').
    timeframe_label : str
        A custom label used as part of the cache key (e.g., 'daily2y_0').
    timeframe_range : str
        The timeframe string for the API (e.g., '2023-01-01 2023-09-30').
    max_retries : int, optional
        Number of retry attempts if request fails (default is 3).

    Returns
    dict or None
        Dictionary of daily scores {YYYY-MM-DD: interest_score} or None if request fails.
    """
    cache_key = f"{artist_name}|{geo}|{timeframe_label}" #unique identifier
    cached = get_cached_score(cache_key)                 #checks if it's already stored
    
    if cached is not None:
        return cached
    
    for attempt in range(1, max_retries + 1):
        try:
            pytrends.build_payload([artist_name], timeframe=timeframe_range, geo=geo)
            data = pytrends.interest_over_time()

            if not data.empty and artist_name in data.columns:
                trend_series = {
                    str(date): int(score)
                    for date, score in data[artist_name].dropna().items()
                }
                #Save to cache and sleep before returning
                set_cached_score(cache_key, trend_series)

                time.sleep(random.uniform(4, 6))
                return trend_series 

            else:
                trend_series = None

        except Exception as e:
                print(f"WARNING: Attempt {attempt}/{max_retries} failed for {artist_name} in {geo} ({timeframe_label}): {e}")

                if "429" in str(e) and attempt < max_retries:
                    wait_time = 60 * attempt  # Exponential backoff
                    print(f"Sleeping for {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    print(f"Error: Giving up on {artist_name} in {geo} ({timeframe_label}) after {attempt} attempts.")
                    return None

    return None
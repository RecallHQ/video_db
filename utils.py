from pytube import YouTube
import datetime

import streamlit as st

FIRESTORE_COLLECTION = "videoindex_db_1"
TEST_COLLECTION = "test_collection"

LLMCOURSE_VIDEO_ENTRIES = [
    
]


def time_to_seconds(time_str):
    """
    Convert a time string in the format HH:MM:SS, MM:SS, or SS into total seconds.

    Parameters:
        time_str (str): Time in the format 'HH:MM:SS', 'MM:SS', or 'SS'.

    Returns:
        int: Total seconds.
    """

    if time_str.isdigit():
        return int(time_str)

    try:
        parts = list(map(int, time_str.split(':')))
        if len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = parts
        elif len(parts) == 2:  # MM:SS
            hours, minutes, seconds = 0, *parts
        elif len(parts) == 1:  # SS
            hours, minutes, seconds = 0, 0, parts[0]
        else:
            return 0
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        return 0
        
def seconds_to_time(seconds):
    """
    Convert a number of seconds into a time string in the format HH:MM:SS, MM:SS, or SS.

    Parameters:
        seconds (int): Total seconds.

    Returns:
        str: Time string in the appropriate format.
    """
    if seconds < 0:
        raise ValueError("Seconds cannot be negative")

    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    elif minutes > 0:
        return f"{minutes:02}:{seconds:02}"
    else:
        return f"{seconds:02}"

def invalidate_cache():
    if 'cache_value' not in st.session_state:
        st.session_state.cache_value = 0
    st.session_state.cache_value = st.session_state.cache_value + 1

def fetch_youtube_metadata(url):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        
        # Extract metadata
        metadata = {
            "title": yt.title,
            "description": yt.description,
            "duration": yt.length,  # Duration in seconds
        }
        
        return metadata
    except Exception as e:
        return {"error": str(e)}
    
def get_ms_since_epoch():
    dt = datetime.datetime.now()
    return dt.microsecond / 1000


def get_collection_uuid():
    id = get_ms_since_epoch()
    return f"dataitem_{id}"

def sanitize_url(youtube_url):
    if "live" in youtube_url:
        youtube_url = youtube_url.replace("live", "embed")
    return youtube_url


# Example usage
url = "https://www.youtube.com/watch?v=your_video_id"
metadata = fetch_youtube_metadata(url)

if "error" in metadata:
    print("Error:", metadata["error"])
else:
    print("Title:", metadata["title"])
    print("Description:", metadata["description"])
    print("Duration (seconds):", metadata["duration"])

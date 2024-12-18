from pytube import YouTube
import datetime

import streamlit as st


LLMCOURSE_VIDEO_ENTRIES = [
    
]

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

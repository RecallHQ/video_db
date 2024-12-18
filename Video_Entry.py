import streamlit as st
from firestore_db import FirestoreHandler, service_account_json
import streamlit.components.v1 as components
from utils import fetch_youtube_metadata, sanitize_url, get_collection_uuid, invalidate_cache, TEST_COLLECTION, FIRESTORE_COLLECTION



def clear_form():
  # st.session_state["video_url"] = ""
    st.session_state["query"] = ""
    st.session_state["answer"] = ""
    st.session_state["timestamp_pairs"] =[]




st.set_page_config(
    page_title="VideoIndex Dataset Tool",
    page_icon="👋",
    layout="wide"
)

# Initialize firebase
if 'firestore' not in st.session_state:
    st.session_state.firestore = FirestoreHandler(FIRESTORE_COLLECTION, service_account_json)


st.title('VideoIndex Dataset Tool')
st.header('New datapoint entry')

video_url = st.text_input("Enter video URL:", "", key="video_url")
if video_url:
    print(" video url = ", video_url)
    video_url = sanitize_url(video_url)
    st.video(video_url)
    print("sanitized video url = ", video_url)
    metadata = fetch_youtube_metadata(video_url)

query = st.text_area("Query", "", key="query")

answer = st.text_area("Answer", "", key="answer")
# Add a text input for the video URL
modality = st.selectbox(
    "The answer requires information from:",
    ("Audio only", "Images", "Video segment"),
    index=None,
    placeholder="Modality of information needed to answer the question...",
    key="modality"
)
st.write("You selected:", modality)
# Container for timestamp pairs
timestamp_pairs = []

# Initialize session state for timestamp pairs if not exists
if 'timestamp_pairs' not in st.session_state:
    st.session_state.timestamp_pairs = []

# Add new timestamp pair button
if st.button("Add Timestamp Interval"):
    st.session_state.timestamp_pairs.append({"start": "0", "end": ""})

# Display all timestamp pairs
for i, pair in enumerate(st.session_state.timestamp_pairs):
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        pair["start"] = st.text_input(f"Start timestamp {i+1} (in seconds):", pair["start"], key=f"start_{i}")
    with col2:
        pair["end"] = st.text_input(f"End timestamp {i+1} (in seconds):", pair["end"], key=f"end_{i}")
    # Add play button for this timestamp interval
    if st.button(f"Play {pair['start']}-{pair['end']}s", key=f"play_{i}"):
        # Format video URL for specific timestamp
        if video_url:
            start_time = int(float(pair["start"]))
            # Modify URL to start at timestamp
            if "youtube.com" in video_url:
                # For YouTube videos, add start parameter
                if "?" in video_url:
                    timestamped_url = f"{video_url}&start={start_time}"
                else:
                    timestamped_url = f"{video_url}?start={start_time}"
            else:
                # For direct video files, use as is
                timestamped_url = video_url
            orig_url = "https://www.youtube.com/embed/OOdtmCMSOo4?si=N2pyYNjpWwMyymbM"
            print(f"timestamped url = {timestamped_url}")
            # Display video starting at timestamp
            st.markdown(f"""
                     <iframe width="560" height="315" 
                        src={timestamped_url} title="YouTube video player"
                         frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media;
                         gyroscope; picture-in-picture; web-share"
                         referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>   

                """,  unsafe_allow_html=True)
    with col3:
        if st.button("Remove", key=f"remove_{i}"):
            st.session_state.timestamp_pairs.pop(i)
    

    # Add save button
if st.button("Save to Database"):
    # Create data object with all fields
    data = {
        "query": query,
        "answer": answer,
        "video_url": video_url,
        "status": "valid",
        "modality": modality,
        "timestamps": [
            {
                "start": pair["start"],
                "end": pair["end"]
            } for pair in st.session_state.timestamp_pairs
        ]
    }
    print("Saving to db: ", data)
    collection_id = get_collection_uuid()
    fs_handler = st.session_state.firestore
    fs_handler.write_document(collection_id, data)
    # TODO: Write data
    invalidate_cache()


if st.button("Clear"):
    clear_form()
    
  
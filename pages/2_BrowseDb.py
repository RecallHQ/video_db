import streamlit as st
from firestore_db import FirestoreHandler, service_account_json
from utils import invalidate_cache, FIRESTORE_COLLECTION, TEST_COLLECTION
from streamlit_js_eval import streamlit_js_eval


st.title("Browse the Database")
# Initialize firebase
if 'firestore' not in st.session_state:
    # change to TEST_COLLECTION for TESTING
    st.session_state.firestore = FirestoreHandler(FIRESTORE_COLLECTION, service_account_json)

fs_handler = st.session_state.firestore

if 'cache_value' not in st.session_state:
    st.session_state.cache_value = 0


@st.cache_data
def fetch_all(cache_input):
    all_docs = fs_handler.read_all_documents()
    return all_docs


for d in fetch_all(cache_input=st.session_state.cache_value):
    for key, value in d.items():
        st.text(f" DataEntry ID: {key}")
        video_url = value["video_url"]
        query = value["query"]
        answer = value["answer"]
        ts = value["timestamps"]
        status = value.get("status",  "valid")
        modality = value.get("modality", "Video segment")

        st.text(f"Video Url: {video_url}")
        st.text(f"Query: {query}")
        st.text(f"Answer: {answer}")
        st.text(f" Timestamps: {ts}")
        st.text(f"Status: {status}")
       
        if st.button("Delete"):
            value["status"] = "deleted"
            fs_handler.update_document(key, value)
            invalidate_cache()
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
       
        st.divider()





# app.py
import streamlit as st
import requests
import pandas as pd

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="MelodyMine", page_icon="🎵", layout="wide")

st.title("🎵 MelodyMine")
st.markdown("Discover new music based on audio features and similarity!")

# Search functionality - THIS SHOULD BE AT THE TOP
st.header("🔍 Search for Songs")
search_query = st.text_input("Search by song name or artist:", key="search_input")
if search_query:
    try:
        response = requests.get(f"{BACKEND_URL}/search", params={"query": search_query, "limit": 10})
        if response.status_code == 200:
            results = response.json()
            if results:
                st.subheader("Search Results:")
                for track in results:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{track['name']}** by {track['artist']}")
                        st.code(f"Track ID: {track['track_id']}")
                    with col2:
                        if st.button("Use this track", key=f"use_{track['track_id']}"):
                            st.session_state.selected_track_id = track['track_id']
                    with col3:
                        if st.button("View details", key=f"details_{track['track_id']}"):
                            st.session_state.view_track = track
                    st.divider()
            else:
                st.info("No songs found matching your search.")
    except Exception as e:
        st.error(f"Search failed: {e}")

# Show selected track
if 'selected_track_id' in st.session_state:
    st.success(f"Selected Track ID: {st.session_state.selected_track_id}")
    
# Input for song recommendation
st.header("🎧 Recommend Similar Songs")
col1, col2 = st.columns([2, 1])

with col1:
    # Use selected track ID or manual input
    track_id = st.text_input("Enter Track ID:", 
                            value=st.session_state.get('selected_track_id', ''),
                            placeholder="e.g., TRIOREW128F424EAF0")
with col2:
    num_recommendations = st.slider("Number of recommendations", 1, 10, 5)

if st.button("Get Recommendations") and track_id:
    with st.spinner("Finding similar songs..."):
        try:
            response = requests.get(f"{BACKEND_URL}/recommend/song", 
                                  params={"track_id": track_id, "n": num_recommendations})
            
            if response.status_code == 200:
                recommendations = response.json()
                if "error" in recommendations:
                    st.error(recommendations["error"])
                else:
                    st.success(f"Found {len(recommendations)} recommendations!")
                    
                    for i, rec in enumerate(recommendations, 1):
                        with st.container():
                            st.markdown(f"### {i}. {rec['name']}")
                            st.write(f"**Artist:** {rec['artist']}")
                            st.write(f"**Track ID:** `{rec['track_id']}`")
                            
                            # Show audio features
                            feature_cols = st.columns(3)
                            features_to_show = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness']
                            
                            for j, feature in enumerate(features_to_show):
                                if feature in rec:
                                    with feature_cols[j % 3]:
                                        st.metric(feature.title(), f"{rec[feature]:.2f}")
                            
                            st.divider()
            else:
                st.error("Failed to fetch recommendations.")
                
        except Exception as e:
            st.error(f"Error: {e}")

# Input for playlist recommendation
st.header("📋 Recommend by Playlist")
playlist_ids = st.text_area("Enter Track IDs (comma-separated):", 
                           placeholder="TRIOREW128F424EAF0, TRABC123456..., TRDEF789...")

if st.button("Recommend from Playlist") and playlist_ids:
    with st.spinner("Analyzing playlist and finding recommendations..."):
        try:
            response = requests.get(f"{BACKEND_URL}/recommend/playlist", 
                                  params={"playlist_ids": playlist_ids, "n": num_recommendations})
            
            if response.status_code == 200:
                recommendations = response.json()
                if "error" in recommendations:
                    st.error(recommendations["error"])
                else:
                    st.success(f"Found {len(recommendations)} playlist-based recommendations!")
                    
                    for i, rec in enumerate(recommendations, 1):
                        with st.container():
                            st.markdown(f"### {i}. {rec['name']}")
                            st.write(f"**Artist:** {rec['artist']}")
                            st.write(f"**Track ID:** `{rec['track_id']}`")
                            st.divider()
            else:
                st.error("Failed to fetch playlist recommendations.")
                
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This music recommender uses:
    - **Audio features**: danceability, energy, valence, etc.
    - **Machine learning**: Cosine similarity on standardized features
    - **Dataset**: 50,000+ tracks with Spotify audio features
    
    **How to use:**
    1. Search for a song or artist
    2. Copy the Track ID from search results
    3. Use the Track ID to get recommendations
    4. Or create a playlist of multiple Track IDs
    """)
    
    # Show dataset stats
    try:
        response = requests.get(f"{BACKEND_URL}/")
        if response.status_code == 200:
            stats = response.json()
            st.metric("Total Tracks", stats["total_tracks"])
    except:
        pass

    # Sample Track IDs for testing
    st.header("🎯 Sample Track IDs")
    st.markdown("""
    Try these for testing:
    - `TRIOREW128F424EAF0` (Mr. Brightside)
    - Search for more above!
    """)
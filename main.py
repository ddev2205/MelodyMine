# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from recommender import build_model, recommend_by_song, recommend_by_playlist, search_songs, load_data

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data and model on startup
data, feature_columns = load_data()
model = build_model(data, feature_columns)

@app.get("/")
def read_root():
    return {"message": "Music Recommender API", "total_tracks": len(data)}

@app.get("/recommend/song")
def recommend_song(track_id: str, n: int = 5):
    try:
        recommendations = recommend_by_song(model, data, feature_columns, track_id, n)
        return recommendations.to_dict(orient="records")
    except ValueError as e:
        return {"error": str(e)}

@app.get("/recommend/playlist")
def recommend_playlist(playlist_ids: str, n: int = 5):
    try:
        playlist_track_ids = playlist_ids.split(",")
        recommendations = recommend_by_playlist(model, data, feature_columns, playlist_track_ids, n)
        return recommendations.to_dict(orient="records")
    except ValueError as e:
        return {"error": str(e)}

@app.get("/search")
def search_tracks(query: str, limit: int = 10):
    results = search_songs(data, query, limit)
    return results.to_dict(orient="records")

@app.get("/track/{track_id}")
def get_track_info(track_id: str):
    track = data[data["track_id"] == track_id]
    if track.empty:
        return {"error": "Track not found"}
    return track.iloc[0].to_dict()
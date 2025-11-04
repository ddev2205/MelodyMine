# recommender.py
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

# Load preprocessed data
data_path = "data/preprocessed_data.parquet"

def load_data():
    print("Loading preprocessed data...")
    data = pd.read_parquet(data_path)
    
    # Use track_id as the identifier from your dataset
    feature_columns = ["danceability", "energy", "acousticness", "instrumentalness", 
                      "liveness", "valence", "tempo", "loudness", "speechiness"]
    
    # Filter to only existing columns
    feature_columns = [col for col in feature_columns if col in data.columns]
    
    print(f"Using features: {feature_columns}")
    return data, feature_columns

# Build recommender model
def build_model(data, feature_columns):
    print("Building recommender model...")
    features = data[feature_columns]
    model = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=20)
    model.fit(features)
    return model

# Recommend songs by track_id
def recommend_by_song(model, data, feature_columns, track_id, n=5):
    print(f"Recommending songs similar to track_id {track_id}...")
    
    # Find song by track_id
    song_features = data.loc[data["track_id"] == track_id, feature_columns]
    
    if song_features.empty:
        raise ValueError(f"Track ID {track_id} not found in dataset.")
    
    distances, indices = model.kneighbors(song_features, n_neighbors=n+1)
    recommendations = data.iloc[indices[0][1:]]  # Exclude the input song itself
    return recommendations

# Recommend songs by playlist (average features)
def recommend_by_playlist(model, data, feature_columns, playlist_track_ids, n=5):
    print("Recommending songs based on playlist...")
    
    # Filter playlist songs
    playlist_features = data[data["track_id"].isin(playlist_track_ids)][feature_columns]
    
    if playlist_features.empty:
        raise ValueError("No valid track IDs found in playlist.")
    
    avg_features = np.mean(playlist_features, axis=0).values.reshape(1, -1)
    distances, indices = model.kneighbors(avg_features, n_neighbors=n)
    recommendations = data.iloc[indices[0]]
    return recommendations

# Search songs by name or artist
def search_songs(data, query, limit=10):
    mask = (
        data['name'].str.contains(query, case=False, na=False) |
        data['artist'].str.contains(query, case=False, na=False)
    )
    return data[mask].head(limit)

if __name__ == "__main__":
    data, feature_columns = load_data()
    model = build_model(data, feature_columns)
    print("Recommender ready!")
    print(f"Total tracks: {len(data)}")
    
    # Test with a sample track
    sample_track = data.iloc[0]
    print(f"Sample track: '{sample_track['name']}' by {sample_track['artist']}")
    print(f"Sample track_id: {sample_track['track_id']}")
# data_loader.py
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Define paths
data_path = "data/Music Info.csv"
output_path = "data/preprocessed_data.parquet"

print(f"Using dataset: {data_path}")

# Load dataset
def load_dataset():
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    print("Loading dataset...")
    return pd.read_csv(data_path)

# Preprocess dataset
def preprocess_data(df):
    print("Preprocessing data...")
    
    # Use the available features from your dataset
    available_features = ["danceability", "energy", "acousticness", "instrumentalness", 
                         "liveness", "valence", "tempo", "loudness", "speechiness"]
    
    # Check which features actually exist in the dataset
    available_features = [f for f in available_features if f in df.columns]
    
    print(f"Using features: {available_features}")
    
    if not available_features:
        raise ValueError("No audio features found in dataset")
    
    # Handle missing values
    df = df.dropna(subset=available_features)
    
    # Standardize features
    scaler = StandardScaler()
    df[available_features] = scaler.fit_transform(df[available_features])
    
    return df, available_features
    print(f"Features used: {features_used}")
    print(f"Dataset shape: {preprocessed_data.shape}")
    print(f"Sample track: {preprocessed_data.iloc[0]['name']} by {preprocessed_data.iloc[0]['artist']}")
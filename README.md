# Music Recommender Project

## Overview
This project is a music recommender system built using FastAPI, Streamlit, and machine learning. It recommends songs based on a given song or playlist.

## Features
- Content-based recommendations using Spotify audio features.
- Integration with Spotify API for playlist fetching.
- FastAPI backend with endpoints for recommendations.
- Streamlit frontend for user interaction.

## Setup
1. Install dependencies:
```cmd
pip install -r requirements.txt
```
2. Preprocess dataset:
```cmd
python data_loader.py
```
3. Run backend and frontend (see `DEPLOYMENT.md`).

## Dataset
- Kaggle: [Million Song Dataset - Spotify/LastFM](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)

## Explanation
Recommendations are based on cosine similarity of audio features (e.g., danceability, energy, tempo).
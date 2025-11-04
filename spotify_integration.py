import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Fetch tracks from a playlist
def fetch_playlist_tracks(playlist_url):
    print("Fetching playlist tracks...")
    playlist_id = playlist_url.split("playlist/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in results["items"]:
        track = item["track"]
        tracks.append({
            "id": track["id"],
            "name": track["name"],
            "artist": track["artists"][0]["name"]
        })
    return tracks

if __name__ == "__main__":
    # Example usage
    playlist_url = "your_playlist_url_here"
    tracks = fetch_playlist_tracks(playlist_url)
    print(tracks)
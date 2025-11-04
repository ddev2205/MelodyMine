import unittest
from recommender import recommend_by_song, recommend_by_playlist, build_model
import pandas as pd

class TestRecommender(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_parquet("data/preprocessed_data.parquet")
        cls.model = build_model(cls.data)

    def test_recommend_by_song(self):
        song_id = self.data.iloc[0]["id"]
        recommendations = recommend_by_song(self.model, self.data, song_id, n=3)
        self.assertEqual(len(recommendations), 3)

    def test_recommend_by_playlist(self):
        playlist_ids = self.data["id"].iloc[:3].tolist()
        recommendations = recommend_by_playlist(self.model, self.data, playlist_ids, n=3)
        self.assertEqual(len(recommendations), 3)

if __name__ == "__main__":
    unittest.main()
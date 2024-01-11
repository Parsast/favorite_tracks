import json
import numpy as np
from sklearn.neighbors import NearestNeighbors

with open("saved_tracks.json", "r") as f:
    data = json.load(f)

track_features = []
track_names = []
features_keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

for track in data:
    feature = []
    for key in features_keys:
        feature.append(track["audio_features"][key])
    track_features.append(feature)
    track_names.append(track["track"]["name"])

X = np.array(track_features)

k = 5

knn = NearestNeighbors(n_neighbors=k)

knn.fit(X)

distances, indices = knn.kneighbors(X)
# print(distances)
for i in range(len(indices)):
    # Get the current track name
    current_track = track_names[i]

    # Get neighbor indices for the current track
    neighbor_indices = indices[i]

    # Find the neighbor track names
    neighbor_tracks = [track_names[index] for index in neighbor_indices]

    print(f"Neighbors of {current_track}: {neighbor_tracks}")

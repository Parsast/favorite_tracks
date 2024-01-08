import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  

# Select your database
db = client['mini_tracks']

# Select your collection
collection = db['mini']

pipeline = [
    {"$unwind": "$recommendations.tracks"},
    {"$group": {"_id": "$recommendations.tracks.id", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}  
]
results = collection.aggregate(pipeline)

for result in results:
    documents = collection.find({"recommendations.tracks.id":result["_id"]})
    for document in documents:
        print ("The original track: " + document["track"]["name"])
        for recommended in document["recommendations"]["tracks"]:
            if recommended['id'] == result["_id"]:
                print ("The recommended song is: " + recommended["name"])

# mini_tracks = tracks[0:int(len(tracks)/20)]

# with open('saved_mini_tracks.json', 'w') as file:
#         json.dump(mini_tracks, file, indent=4)
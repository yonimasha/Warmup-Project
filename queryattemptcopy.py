import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from google.api_core.client_options import ClientOptions
from google.cloud.firestore_v1.base_query import FieldFilter


def make_query(listqueries, db):

    # connect to the database
    docs = db.collection("top100spotifysongscoll").stream()
    print(listqueries)
    if 'AND' in listqueries:
        listqueries.remove('AND')

    # check the length of the list to determine if it is a compound query 
    if len(listqueries) == 3: 
        # the query is not compound 
        # check the operator 
        #operator = ""
        if listqueries[1] == "==":
            result = query_equals(db, listqueries)
            return result
        elif listqueries[1] == "<":
            result = query_less(db, listqueries)
            return result
        elif listqueries[1] == ">":
            result = query_greater(db, listqueries)
            return result
    elif len(listqueries) == 6:
        # Create filters explicitly using FieldFilter for both conditions
        filter_1 = firestore.FieldFilter(listqueries[0], listqueries[1], listqueries[2])
        filter_2 = firestore.FieldFilter(listqueries[3], listqueries[4], listqueries[5])
        # print(listqueries[1])
        # print(listqueries[4])

        query_ref = db.collection("top100spotifysongscoll").where(filter=firestore.FieldFilter(listqueries[0], listqueries[1], listqueries[2])).where(filter=firestore.FieldFilter(listqueries[3], listqueries[4], listqueries[5]))

        # Fetch and display only track names
        results = query_ref.stream()
        #print(results)

        # List to hold all the songs by the artist
        artist_songs = []

        
        for doc in results:
            data = doc.to_dict()
            artist_songs.append(data['track'])
        return artist_songs

    
def connect_to_database():
    cred = credentials.Certificate('songskey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return cred, db

def query_equals(db, listqueries): 
     # Reference to the spotifytop100songs collection
    songs_ref = db.collection('spotifytop100songs')

    if listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name" or listqueries[0] == "dance_ability":
        # Use filter keyword for the query and chain where clauses
        query_ref =  db.collection("top100spotifysongscoll").where(filter=firestore.FieldFilter(listqueries[0], '==', listqueries[2]))

        # Fetch and display only track names
        results = query_ref.stream()

        # List to hold all the songs by the artist
        artist_songs = []

        for doc in results:
            data = doc.to_dict()
            artist_songs.append(data['track'])  # Add each song's data to the list
        
        
        return(artist_songs)  # This prints only the track name
    elif listqueries[0] == "track":
        # Use filter keyword for the query and chain where clauses
        query_ref = songs_ref.where(filter=firestore.FieldFilter(listqueries[0], '==', listqueries[2]))

        # Fetch and display only track names
        results = query_ref.stream()

        for doc in results:
            data = doc.to_dict()
            return([data['artist'] + ' ' + data['album_name'] + ' ' + data['genre'] + ' ' + data['release_date']])  
        
def query_less(db, listqueries):
     # Reference to the spotifytop100songs collection
    songs_ref = db.collection('spotifytop100songs')

    if listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name":
        print("You cannot use this operator for that key words")
    else:
        query_ref = db.collection("top100spotifysongscoll").where(filter=firestore.FieldFilter('dance_ability', '<', int(listqueries[2])))

        # Fetch and display only track names
        results = query_ref.stream()
        data = []

        for doc in results:
            print(doc)
            song_data = doc.to_dict()
            data.append(song_data['track'] + ' by ' + song_data['artist'])

        return data
        # return("track: " + data['track'] + "     artist: " + data['artist'] + "     genre: " + data['genre'])  
        



def query_greater(db, listqueries):
     # Reference to the spotifytop100songs collection
    songs_ref = db.collection('spotifytop100songs')

    if listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name":
        print("You cannot use this operator for that key words")
    else:
        query_ref = db.collection("top100spotifysongscoll").where(filter=firestore.FieldFilter('dance_ability', '>', int(listqueries[2])))
        # Fetch and display only track names
        results = query_ref.stream()
        
        data = []
        for doc in results:
            song_data = doc.to_dict()
            data.append(song_data['track'] + ' by ' + song_data['artist'])
            
        return data
        # return("track: " + data['track'] + "     artist: " + data['artist'] + "     genre: " + data['genre'])  

#make_query(listqueries)


        
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from google.api_core.client_options import ClientOptions
from google.cloud.firestore_v1.base_query import FieldFilter


def make_query(listqueries, db):
    """This function takes in a list of strings as well as the data base that is being queried.
    The length of the list is checked, and if it is empty then we return false to indicate that no query was made.
    If it is a single query, we make calls to one of three query types based on the operator. If the query is a compound
    query, we convert any items in a dancability query to floats and then check the collection. Returns a list of results
    from the database given the specified criteria of the query."""
    if len(listqueries) == 0:
        return False
    # connect to the database
    docs = db.collection("top100songsonspotify").stream()
    if 'AND' in listqueries:
        listqueries.remove('AND')

    # check the length of the list to determine if it is a compound query 
    if len(listqueries) == 3: 
        # the query is not compound 
        # check the operator to determine which query function to call
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
        # create filters explicitly using FieldFilter for both conditions
        filter_1 = firestore.FieldFilter(listqueries[0], listqueries[1], listqueries[2])
        filter_2 = firestore.FieldFilter(listqueries[3], listqueries[4], listqueries[5])
        
        # check listqueries[0] to see if it is dancability. if it is, make listqueries[2] a float 
        if listqueries[0] == 'dance_ability':
            query_ref = db.collection("top100songsonspotify").where(filter=firestore.FieldFilter(listqueries[0], listqueries[1], float(listqueries[2]))).where(filter=firestore.FieldFilter(listqueries[3], listqueries[4], listqueries[5]))
        
        # check listqueries[3] to see if it is dancability. if it is, make listqueries[5] a float 
        elif listqueries[3] == 'dance_ability':
            query_ref = db.collection("top100songsonspotify").where(filter=firestore.FieldFilter(listqueries[0], listqueries[1], listqueries[2])).where(filter=firestore.FieldFilter(listqueries[3], listqueries[4], float(listqueries[5])))

        # check listqueries[0] and listqueries[3] to see if they are dancability. if they both are, make listqueries[2] and listqueries[5] floats
        elif listqueries[0] == 'dance_ability' and listqueries[3] == 'dance_ability':
             query_ref = db.collection("top100songsonspotify").where(filter=firestore.FieldFilter(listqueries[0], listqueries[1], float(listqueries[2]))).where(filter=firestore.FieldFilter(listqueries[3], listqueries[4], float(listqueries[5])))

        # otherwise run the query without converting listqueries[2] or listqueries[5] to floats
        else:
            query_ref = db.collection("top100songsonspotify").where(filter=firestore.FieldFilter(listqueries[0], listqueries[1], listqueries[2])).where(filter=firestore.FieldFilter(listqueries[3], listqueries[4], listqueries[5]))
        
        # fetch the results from the query
        results = query_ref.stream()

        # initialize an empty list to hold all the tracks for that query 
        artist_songs = []

        
        for doc in results:
            data = doc.to_dict()
            # append the tracks to the artist_songs list
            artist_songs.append(data['track'])
        # return the list of tracks that meet the query criteria
        return artist_songs
    
def connect_to_database():
    # connects to the firestore firebase using the credentials in songskey.json
    cred = credentials.Certificate('songskey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return cred, db

def query_equals(db, listqueries): 
    """This is a function to query the database using the == operator. First we reference the collection, then we check
    to see if dance_ability is being queried to make sure that it is passed as a float when querying the database. Then we return a
    list of all of the tracks that meet the specified query criteria."""
     # create a reference to the top100songsonspotify collection
    songs_ref = db.collection('top100songsonspotify')

    if listqueries[0] == 'dance_ability':
         # pass the listqueries items in as filters 
        query_ref =  db.collection("top100songsonspotify").where(filter=firestore.FieldFilter(listqueries[0], '==', float(listqueries[2])))

        # fetch the results from the query
        results = query_ref.stream()

        # initialize an empty list to hold all the tracks for that query 
        artist_songs = []

        for doc in results:
            data = doc.to_dict()
            artist_songs.append(data['track'])  
        
        
        return(artist_songs)  # This prints only the track name
    
    elif listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name":
        # pass the listqueries items in as filters 
        query_ref =  db.collection("top100songsonspotify").where(filter=firestore.FieldFilter(listqueries[0], '==', listqueries[2]))

        # fetch the results from the query
        results = query_ref.stream()

        # initialize an empty list to hold all the tracks for that query 
        artist_songs = []

        for doc in results:
            data = doc.to_dict()
            # append the tracks to the artist_songs list
            artist_songs.append(data['track'])  
        
        return(artist_songs) 
        
    elif listqueries[0] == "track":
        # pass the listqueries items in as filters 
        query_ref = songs_ref.where(filter=firestore.FieldFilter(listqueries[0], '==', listqueries[2]))

        # fetch the results from the query
        results = query_ref.stream()

        for doc in results:
            data = doc.to_dict()
        return(['Artist: ' + data['artist'] +  ' Album: ' + data['album_name'] + ' Genre: ' + data['genre']])  
        
def query_less(db, listqueries):
    """This is a function to query the database using the < operator. First we reference the collection, then we check
    to verify dance_ability is being queried to make sure that it is passed as a float when querying the database. Then we return a
    list of all of the tracks that meet the specified query criteria."""
    # make reference to the top100songsonspotify collection
    songs_ref = db.collection('top100songsonspotify')

    # check to make sure that the query involves dance_ability
    if listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name":
        print("You cannot use this operator for that key words")
    else:
        query_ref = db.collection("top100songsonspotify").where(filter=firestore.FieldFilter('dance_ability', '<', float(listqueries[2])))

        # fetch the results from the query
        results = query_ref.stream()
        
        # initialize an empty list to hold all the tracks and artists for that query 
        data = []

        for doc in results:
            print(doc)
            song_data = doc.to_dict()
            # append the results of the query to the list
            data.append(song_data['track'] + ' by ' + song_data['artist'])

        return data

def query_greater(db, listqueries):
    """This is a function to query the database using the > operator. First we reference the collection, then we check
    to verify dance_ability is being queried to make sure that it is passed as a float when querying the database. Then we return a
    list of all of the tracks that meet the specified query criteria."""
    # make reference to the top100songsonspotify collection
    songs_ref = db.collection('top100songsonspotify')

    # check to make sure that the query involves dance_ability
    if listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name":
        print("You cannot use this operator for that key words")
    else:
        query_ref = db.collection("top100songsonspotify").where(filter=firestore.FieldFilter('dance_ability', '>', float(listqueries[2])))
        
        # fetch the results from the query
        results = query_ref.stream()

        # initialize an empty list to hold all the tracks and artists for that query 
        data = []
        for doc in results:
            song_data = doc.to_dict()
            # append the results of the query to the list
            data.append(song_data['track'] + ' by ' + song_data['artist'])
            
        return data


        

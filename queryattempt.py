import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from google.api_core.client_options import ClientOptions
from google.cloud.firestore_v1.base_query import FieldFilter


def make_query(listqueries):

    # connect to the database
    cred, db = connect_to_database()
    docs = db.collection("spotifytop100songs").stream()

    #for doc in docs:
        #print(f"{doc.id} => {doc.to_dict()}")

    #print(listqueries)
    # check the length of the list to determine if it is a compound query 
    if len(listqueries) == 3: 
        # the query is not compound 
        # check the operator 
        #operator = ""
        if listqueries[1] == "==":
            result = query_equals(db, listqueries)
            print(result)
        elif listqueries[1] == "<":
            result = query_less(db, listqueries)
            print(result)
        elif listqueries[1] == ">":
            result = query_greater(db, listqueries)
            print(result)
            
            # call func

            #print("<")
    #for item in listqueries:
        #print(item)
    
def connect_to_database():
    cred = credentials.Certificate('songskey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return cred, db

def query_equals(db, listqueries): 
     # Reference to the spotifytop100songs collection
    songs_ref = db.collection('spotifytop100songs')

    if listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name" or listqueries[0] == "release_date":
        # Use filter keyword for the query and chain where clauses
        query_ref = songs_ref.where(filter=firestore.FieldFilter(listqueries[0], '==', listqueries[2]))

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
            return(data['artist'] + data['albumn_name'] + data['genre'] + data['release_date'])  
        
def query_less(db, listqueries):
     # Reference to the spotifytop100songs collection
    songs_ref = db.collection('spotifytop100songs')

    if listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name":
        print("You cannot use this operator for that key words")
    else:
        #convert the dates to datetime
        convert_dates(db, listqueries[2])



def query_greater(db, listqueries):
     # Reference to the spotifytop100songs collection
    songs_ref = db.collection('spotifytop100songs')

    if listqueries[0] == "artist" or listqueries[0] == "genre" or listqueries[0] == "subgenre" or listqueries[0] == "album_name":
        print("You cannot use this operator for that key words")
    else:
        #convert the dates to datetime
        convert_dates(db, listqueries[2])

def convert_dates(db, listqueries):
    # Convert target date string to a datetime object
    target_date = datetime.strptime(listqueries[2], '%m/%d/%Y')
    
    # Reference to the spotifytop100songs collection
    songs_ref = db.collection('spotifytop100songs')
    
    # Query the entire collection (you can add more filters if needed)
    results = songs_ref.stream()

    # Iterate over the results
    for doc in results:
        data = doc.to_dict()
        
        # Convert the release_date field to a datetime object
        release_date_str = data.get('release_date', '')
        
        try:
            release_date = datetime.strptime(release_date_str, '%m/%d/%Y')
        except ValueError:
            # Skip this document if the release_date format is invalid
            print(f"Invalid date format for track: {data.get('track')}")
            continue
        
        # Check if release_date is before or after the target date
        if release_date < target_date:
            print(f"{data['track']} by {data['artist']} was released before {listqueries[2]}")
        else:
            print(f"{data['track']} by {data['artist']} was released on or after {listqueries[2]}")





    

#make_query(listqueries)


        # Use filter keyword for the query and chain where clauses
        #query_ref = songs_ref.where(filter=firestore.FieldFilter('artist', '==', listqueries[2])).where(filter=firestore.FieldFilter('genre', '==', 'pop'))
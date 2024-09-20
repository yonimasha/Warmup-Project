# for command line arguements.
import sys
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# make call to the SDK json file 
# included for security 
cred = credentials.Certificate('songskey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

class UploadJsonFileToFirestore:
    def __init__(self) -> None:
        # check the command line to ensure that 3 arguments are provided
        # the following are expected filepath, method (set or add), and the name of the collection 
        if len(sys.argv[1:]) != 3:
            print(f'ERROR: Check your command line arguments!,\n 3 arguements expected [file=filepath, method=[set or add], collectionname=[firestore collection name]')
            return None
        
        # Initialize instance variables
        self.json_data = sys.argv[1:][0]
        self.method = sys.argv[1:][1]
        self.collectionname = sys.argv[1:][2]
    
    # get method for the firestore upload method 
    @property
    def method(self):
        return self._method
    
    # set the firestore upload method indicated by the user on the command line
    @method.setter
    def method(self, val):
        if val == 'set' or val == 'add':
            self._method = val
        else:
            # verify that the method is either set or add
            # provide an error method if otherwise
            print(f'Wrong method {val}, use set or add')
    
    # get method for path to the json file with the data
    @property
    def json_data(self):
        return self._json_data
    
    # set the path to the json file with the data and process 
    @json_data.setter
    def json_data(self, val):
        if val:
            try:
                # Opening JSON file
                f = open(val,)
                
                # returns JSON object as a dictionary
                data = json.load(f)
                
                # make sure to close file
                f.close()
                self._json_data = data
            except Exception as e:
                print(f'FILE EXCEPTION: {str(e)}')
        else:
            print(f'Wrong file path {val}')

    # Main class method to populate firestore 
    # With the said data
    def upload(self):
        if  self.json_data and self.method:
           
            # Iterating through the json list
            for idx, item in enumerate(self.json_data):
                if self.method == 'set':
                    self.set(item)
                else:
                    self.add(item)
    
    # Collection Add method
    # Adds all data under a collection
    # With firebase firestore auto generated IDS
    def add(self, item):
        return db.collection(self.collectionname).add(item)
    
    # Collection document set method
    # Adds all data under a collection
    # With custom document IDS 
    def set(self, item):
        return db.collection(self.collectionname).document(str(item['id'])).set(item)

uploadjson = UploadJsonFileToFirestore()
uploadjson.upload()      



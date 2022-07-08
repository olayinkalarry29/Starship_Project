"""
Exercise:
The data in this database has been pulled from https://swapi.dev/,
As well as 'people', the API has data on starships,
In Python, pull data on all available starships from the API,
The "pilots" key contains URLs pointing to the characters who pilot the starship,
Use these to replace 'pilots' with a list of ObjectIDs from our characters collection,
then insert the starships into their own collection. Use functions at the very least!,
"""
import requests  # The Import requests allow HTTP requests and return the GET request's data.
import pymongo  # Import pymongo to connect and interacts with MongoDB databases Compass.

client = pymongo.MongoClient()  # Create Client to get the COLLECTIONS from database
db = client['starwars']
starships = db["Starships"]
characters = db['characters']

num_of_pages = 1  # Variable to add every number of page


def get_page(num_of_pages):  # To get details of a starship page using the API get requests
    return requests.get("https://swapi.dev/api/starships?page="+str(num_of_pages))


def get_name(pilot):  # To get only the pilot name from the API
    return requests.get(pilot).json()['name']


def get_obj_id(name):  # Get the ID from the characters' collection in the Database
    return characters.find_one({'name': name}, {"_id": 1})['_id']


def replace_with_id(starship):  # To replace api urls with character obj ids
    if starship['pilots']:
        for pilot in range(len(starship['pilots'])):
            name = get_name(starship['pilots'][pilot])
            id = get_obj_id(name)
            starship['pilots'][pilot] = id
    return starship


def insert_doc(starship_response):  # To insert the document into starships collection.
    for starship in starship_response.json()['results']:
        starships.insert_one(replace_with_id(starship))


while get_page(num_of_pages).status_code != 404:  # check if the number of page is not 404:
    starship_resp = get_page(num_of_pages)
    insert_doc(starship_resp)
    num_of_pages += 1

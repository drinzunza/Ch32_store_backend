import pymongo
import certifi

con_str = "mongodb+srv://FSDICh30:PassFSDICh30@cluster0.mzaem.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("OrganikaCh32")


me = {
    "first": "Sergio",
    "last": "Inzunza",
    "age": 36,
    "hobbies": [],
    "address": {
        "street": "Evergreen",
        "number": 742,
        "city": "Springfield"
    }
}
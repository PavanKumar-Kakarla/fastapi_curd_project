from pymongo import MongoClient

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017')

# Creating the Database
db = client['itemsDB']

# Creating the Collections
items_collection = db['Items']
clock_in_collection = db['ClockInRecords']



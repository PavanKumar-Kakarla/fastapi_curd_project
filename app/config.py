from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

# Read MongoDB URI and database name from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "itemsDB")

# MongoDB Connection
client = MongoClient(MONGO_URI)

# Creating the Database
db = client[DATABASE_NAME]

# Creating the Collections
items_collection = db['Items']
clock_in_collection = db['ClockInRecords']



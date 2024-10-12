from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)


# Read MongoDB URI and database name from environment variables
MONGO_URI = "mongodb+srv://pavankumar:12345@cluster0.smbft.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "itemsDB"

print(f"MONGO_URI: {MONGO_URI}")
print(f"DATABASE_NAME: {DATABASE_NAME}")

# MongoDB Connection
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Creating the Database
db = client[DATABASE_NAME]

# Creating the Collections
items_collection = db['Items']
clock_in_collection = db['ClockInRecords']



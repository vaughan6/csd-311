""" 
    Title: mongodb_test.py
    Author: James Vaughan
    Date: 01 July 2023
    Description: Test program for connecting to a 
                 MongoDB Atlas cluster
"""

""" import statements """
from pymongo import MongoClient

# MongoDB connection string 
url = "mongodb+srv://admin:admin@cluster0.ml7xex1.mongodb.net/pytech"

# connect to the MongoDB cluster 
client = MongoClient(url)

# connect pytech database
db = client.pytech

# show the connected collections 
print("\n -- Pytech COllection List --")
print(db.list_collection_names())

# show an exit message
input("\n\n  End of program, press any key to exit... ")

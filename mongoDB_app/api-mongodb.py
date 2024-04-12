# import packages and modules
# please note: if the app is running, then the API will automatically update
from pymongo import MongoClient
import requests as requests
import time

# connect to the MongoDB Atlas cluster with our own unique connection string
try:
    client = MongoClient(
        "mongodb+srv://BDAT_1004_Final_Project:folashade@cluster0.qvkirqz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.get_database('BDAT_FInal_Project')
    collection = db["BDAT_FInal_Project.LatestExchangeRate"]

except:
    print("error ocurred")

finally:
    client.close()
    print("Connection is closed")

# loop to load data from the API to the database
while True:
    r = requests.get("https://api.apilayer.com/exchangerates_data/latest?base=CAD")
    if r.status_code == 200:
        data = r.json()
        result = db.BDAT_FInal_Project.LatestExchangeRate.insert_one(data)
        print(data)
        time.sleep(60)

else:
    exit()

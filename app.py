from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from collections import UserDict
from pymongo.common import validate
import requests
import time
import json
import glob
import pandas as pd
import numpy as np

app = Flask(__name__)

# connecting to MongoDB Atlas
client = MongoClient(
    "mongodb+srv://BDAT_1004_Final_Project:folashade@cluster0.qvkirqz.mongodb.net/")
db = client.get_database('BDAT_FInal_Project')
records = db.LatestExchangeRate

# configurations
year, nMonths = "2023", 12
startdate = pd.date_range(year, periods=nMonths,
                          freq='MS').strftime("%Y-%m-%d")
enddate = pd.date_range(year, periods=nMonths, freq='M').strftime("%Y-%m-%d")
symbols = "USD,EUR,CAD,AUD,GBP,SGD"

l1, l2 = [], []
USD_lst, EUR_lst, CAD_lst, AUD_lst, GBP_lst, SGD_lst = [], [], [], [], [], []

for (start, end) in zip(startdate, enddate):

    url = "https://api.apilayer.com/exchangerates_data/fluctuation?start_date=" + \
        start + "&end_date=" + end + "&symbols=" + symbols + "&format=json"
    
    # set with API key
    payload = {}
    headers= {
    "apikey": "CJhxf2CyGgfimghZ2ywH5gGjAcUHLmqz"
    }

    r = requests.get(url, headers=headers, data = payload)

    if r.status_code == 200:
        data = r.json()

        # data input the line chart
        l1.append(data["rates"]["USD"]["change"])
        l2.append(data["rates"]["CAD"]["change"])

        # data input line chart
        USD_lst.append(data['rates']['USD']['start_rate'])
        EUR_lst.append(data['rates']['EUR']['start_rate'])
        CAD_lst.append(data['rates']['CAD']['start_rate'])
        AUD_lst.append(data['rates']['AUD']['start_rate'])
        GBP_lst.append(data['rates']['GBP']['start_rate'])
        SGD_lst.append(data['rates']['SGD']['start_rate'])

        # Storing data into MongoDB Atlas
        records.insert_one(data)

    else:
        print("Error while loading / prcessing the data.")

AVG_rate = [np.average(USD_lst),np.average(EUR_lst), np.average(CAD_lst), np.average(
    AUD_lst), np.average(GBP_lst), np.average(SGD_lst)]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about-us")
def about():
    return render_template("about-us.html")



@app.route("/line-chart")
def lineChart():
    # implementing the line Chart
    labels = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    values = l2
    return render_template('line-chart.html', labels=labels, values=values)


@app.route("/bar-chart")
def barChart():
    # implementing the bar Chart
    labels = ["USD","EUR", "CAD", "AUD", "GBP", "SGD"]
    values = AVG_rate
    return render_template('bar-chart.html', labels=labels, values=values)


if __name__ == "__main__":
    app.debug = True
    app.run()

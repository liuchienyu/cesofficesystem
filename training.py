from calendar import c
import datetime,time,pymongo
from pymongo import MongoClient
from flask import Flask, render_template, redirect, url_for, render_template, request, session, g
from datetime import timedelta,date

CONNECTION_STRING ="mongodb+srv://dandy40605:1234@cluster0.qqbqe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING,tls=True, tlsAllowInvalidCertificates=True,tz_aware=True )#tls=True, tlsAllowInvalidCertificates=True為解決無法連線問題
# 設定為 +8 時區
tz = datetime.timezone(datetime.timedelta(hours=+8))

db = client.systemdata
base_info = db.finance
results1 = base_info.find({'id_number':'A001'},{'_id':0,'tatal':1})
y = base_info.count_documents({'id_number':'A001'},)
x=0
while y != 0:
    z = base_info.find_one({'_id':y},{'_id':0,'tatal':1})
    y=y-1
    x=x+z['tatal']
    print(x)
else:
    print(y)
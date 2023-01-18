from calendar import c
import datetime,time,pymongo
from pymongo import MongoClient
from flask import Flask, render_template, redirect, url_for, render_template, request, session, g
from datetime import timedelta,date

CONNECTION_STRING ="mongodb+srv://dandy40605:1234@cluster0.qqbqe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING,tls=True, tlsAllowInvalidCertificates=True,tz_aware=True )#tls=True, tlsAllowInvalidCertificates=True為解決無法連線問題
# 設定為 +8 時區
tz = datetime.timezone(datetime.timedelta(hours=+8))

#本薪計算
def money_m(a):
    db = client.systemdata
    base_info = db.finance
    y = base_info.count_documents({'id_number':'A001'},)
    x=0
    while y != 0:
        z = base_info.find_one({'_id':y},{'_id':0,'tatal':1})
        y=y-1
        x=x+z['tatal']
        print(x)
    else:
        return x
#薪資登錄
def finance_imput(a,b,c,d,e,f,g,h):
    db = client.systemdata
    finance = db.finance
    finance_results = finance.find({'id_number':a},{'_id':1})
    finance_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    finance_results.limit(1)#限制數量
    print(finance_results[0])

    #計算文件數量並編號
    if finance_results != None:
        id = 0
        while finance_results != None:
            finance_results = finance.find_one({'_id':id})

            id=finance.count_documents({'id_number':a},)+1
        else:
            print(id)

    post = {"_id":id,
"make_time":datetime.datetime.now(), 
"code_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
"id_number": a, 
"Salary": b,
"food_allowance": c,
"PA_bonus": d,
"performance_bonus":e,
"job_added": f,
"labor_protection": g,
"health_insurance": h,
"tatal":int(b)+int(c)+int(d)+int(e)+int(f)-int(g)-int(h),
"search_date":time.strftime("%Y-%m-%d", time.localtime()),
}

    finance_result = finance.insert_one(post)
import datetime,time,pymongo
from flask import g
from pymongo import MongoClient
CONNECTION_STRING ="mongodb+srv://dandy40605:1234@cluster0.qqbqe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING,tls=True, tlsAllowInvalidCertificates=True,tz_aware=True )#tls=True, tlsAllowInvalidCertificates=True為解決無法連線問題
def document_code_data_in(a,b,c,d,e,f,g):


    db = client.systemdata
    document_code_data = db.document_code_data
    code_results = document_code_data.find({'category':'文號申請'},{'_id':1})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(1)#限制數量
    print(code_results[0])

    #計算文件數量並編號
    if code_results != None:
        id = 0
        while code_results != None:
            code_results = document_code_data.find_one({'_id':id})

            id=document_code_data.count_documents({'category':'文號申請'},)+1
        else:
            print(id)

    post = {"_id":id,
    "make_time":datetime.datetime.now(), 
    "code_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
    'code_name':a,
    'code_number':b + '22' + str(id).zfill(4)+'號',
    'code_speed':c,
    'class_level':d,
    'appendix':e,
    'category':'文號申請',
    'who_make':f,
    'for_who':g

    }

    doc_result = document_code_data.insert_one(post)

def document_code_data_find(a):
    db = client.systemdata
    document_code_data = a
    code_results = document_code_data.find({'category':'文號申請'},{'_id':1})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(1)#限制數量
    return code_results
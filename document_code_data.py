import datetime,time,pymongo
from pymongo import MongoClient

CONNECTION_STRING ="mongodb+srv://dandy40605:1234@cluster0.qqbqe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING,tls=True, tlsAllowInvalidCertificates=True,tz_aware=True )#tls=True, tlsAllowInvalidCertificates=True為解決無法連線問題
3
db = client.systemdata
document_code_data = db.law_system
#code_results = document_code_data.find({'category':'文號申請'},{'_id':1})
#code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
#code_results.limit(1)#限制數量
#print(code_results[0])
''''
if code_results != None:
    id = 0
    while code_results != None:
        code_results = document_code_data.find_one({'_id':id})

        id=document_code_data.count_documents({'category':'文號申請'},)+1
    else:
        print(id)
'''


post = {"_id":1,
"make_time":datetime.datetime.now(), 
"code_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
"unit": "總管理處",
"who": "劉建佑",
"subject": "公告基準測試",
"text_in": "一、公告基準測試",
"search_date":time.strftime("%Y-%m-%d", time.localtime()),
"category": "法務案件",
"law_system_category": "一般公告"

}



doc_result = document_code_data.insert_one(post)#insert_one()新增一筆資料、insert_many()新增多筆資料

#doc_result = document_code_data.update_one(filter={'_id':'0'},update={'$set':{'job_title':'6'}})#update_one()新增一筆資料、update_many()新增多筆資料

#doc_results =document_code_data.find_one({'id_number':'A001'})
print(doc_result)

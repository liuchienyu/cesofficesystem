from calendar import c
import datetime,time,pymongo
from pymongo import MongoClient

CONNECTION_STRING ="mongodb+srv://dandy40605:1234@cluster0.qqbqe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING,tls=True, tlsAllowInvalidCertificates=True,tz_aware=True )#tls=True, tlsAllowInvalidCertificates=True為解決無法連線問題
# 設定為 +8 時區
tz = datetime.timezone(datetime.timedelta(hours=+8))
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
    "code_date":datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"), 
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

def clockin(a,b):
    db = client.systemdata
    clockin = db.clockin
    clockin_results = clockin.find({'category':'打卡'},{'_id':1})
    clockin_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    clockin_results.limit(1)#限制數量
    print(clockin_results[0])

    #計算文件數量並編號
    if clockin_results != None:
        id = 0
        while clockin_results != None:
            clockin_results = clockin.find_one({'_id':id})

            id=clockin.count_documents({'category':'打卡'},)+1
        else:
            print(id)

    post = {"_id":id,
    "make_time":datetime.datetime.now(), 
    "code_date":datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"), 
    'state':a,
    'state2':'上班打卡',
    'code_number':b,
    'category':'打卡',
    "search_date":datetime.datetime.now(tz).strftime("%Y-%m-%d"),
    }

    clock_result = clockin.insert_one(post)

def clockout(a,b):
    db = client.systemdata
    clockin = db.clockin
    clockout_results = clockin.find({'category':'打卡'},{'_id':1})
    clockout_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    clockout_results.limit(1)#限制數量
    print(clockout_results[0])

    #計算文件數量並編號
    if clockout_results != None:
        id = 0
        while clockout_results != None:
            clockout_results = clockin.find_one({'_id':id})

            id=clockin.count_documents({'category':'打卡'},)+1
        else:
            print(id)

    post = {"_id":id,
    "make_time":datetime.datetime.now(), 
    "code_date":datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"), 
    'state':a,
    'state2':'下班打卡',
    'code_number':b,
    'category':'打卡',
    "search_date":datetime.datetime.now(tz).strftime("%Y-%m-%d"),
    }

    clock_result = clockin.insert_one(post)

def announcement_imput(a,b,c,d,e,f):
    db = client.systemdata
    announcement = db.announcement
    announcement_results = announcement.find({'category':'公告'},{'_id':1})
    announcement_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    announcement_results.limit(1)#限制數量
    print(announcement_results[0])

    #計算文件數量並編號
    if announcement_results != None:
        id = 0
        while announcement_results != None:
            announcement_results = announcement.find_one({'_id':id})

            id=announcement.count_documents({'category':'公告'},)+1
        else:
            print(id)

    post = {"_id":id,
    "make_time":datetime.datetime.now(), 
    "code_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
    'unit':a,
    'who':b,
    'subject':c,
    'text_in':d,
    "search_date":time.strftime("%Y-%m-%d", time.localtime()),
    'category':'公告',
    'announcement_category':e,
    'filename':f,
    'search_id':'F'+str(id)
    }

    announcement_result = announcement.insert_one(post)
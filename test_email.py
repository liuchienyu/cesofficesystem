import email.message
from pathlib import Path

def sendpaper(a,b,c,d,e):
#建立訊息物件
    msg=email.message.EmailMessage()
    #利用物件建立基本設定

    from_a="careeteam2021@gmail.com"
    to_b='chienyuliu40605@gmail.com'


    msg["From"]=from_a
    msg["To"]=to_b
    msg["Subject"]="你好"
    mss=Path("templates/paperbase.html").read_text()

    userss= a
    ytimes=b
    mtimes=c
    dtimes = d
    insends = e

    #寄送郵件主要內容
    #msg.set_content("測試郵件純文字內容") #純文字信件內容
    msg.add_alternative(mss.format(user=userss,ytime=ytimes,mtime=mtimes,dtime=dtimes,insend=insends),subtype="html") #HTML信件內容

    acc="careeteam2021@gmail.com"
    password="cgvfnfkyonalzixj"

    #連線到SMTP Sevver
    import smtplib
    #可以從網路上找到主機名稱和連線埠
    server=smtplib.SMTP_SSL("smtp.gmail.com",465) #建立gmail連驗
    server.login(acc,password)
    server.send_message(msg)
    server.close() #發送完成後關閉連線
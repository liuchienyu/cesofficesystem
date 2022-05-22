#encoding=utf-8
from datetime import datetime
import time
import schedule
from random import choice
import smtplib
from email.mime.text import MIMEText

def job1(*args):
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
    with open('tasks', 'a') as f:
        f.write('[{}]{}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(choice(l)))) 
    with open('tasks', 'r') as ff:
        lines = ff.readlines() #讀取所有行
        last_line = lines[-1] #取最後一行      
        print(last_line) 
    mime=MIMEText(last_line, "plain", "utf-8") #撰寫內文內容，以及指定格式為plain，語言為中文
    mime["Subject"]="test測試" #撰寫郵件標題
    mime["From"]= "careeteam2021@gmail.com" #撰寫你的暱稱或是信箱
    mime["To"]= "chienyuliu40605@gmail.com"#撰寫你要寄的人
    #mime["Cc"]="@gmail.com, @gmail.com" #副本收件人
    msg=mime.as_string() #將msg將text轉成str
    smtp=smtplib.SMTP("smtp.gmail.com", 587)  #googl的ping
    smtp.ehlo() #申請身分
    smtp.starttls() #加密文件，避免私密信息被截取
    smtp.login("careeteam2021@gmail.com", "cgvfnfkyonalzixj") 
    from_addr="careeteam2021@gmail.com"
    to_addr=["chienyuliu40605@gmail.com"]
    status=smtp.sendmail(from_addr, to_addr, msg)
    if status=={}:
        print("郵件傳送成功!5min")
    else:
        print("郵件傳送失敗!5min")
    smtp.quit()


# 每隔5秒執行一次job1
#schedule.every(5).seconds.do(job1)
# 每天9:30執行任務
schedule.every().day.at('20:35').do(job1)
schedule.every().day.at('20:40').do(job1)
schedule.every().day.at('20:45').do(job1)
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
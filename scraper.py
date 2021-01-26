import requests
import smtplib
import time
import mysql.connector
from mysql.connector import Error
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def check_price(_url, _price, _mail, _id):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    page = requests.get(_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        title_div = soup.find('div', attrs={'class': '_1h7wt _15mod'})
        title = title_div.find('h1', attrs={'class': '_9a071_1Ux3M _9a071_3nB-- _9a071_1R3g4 _9a071_1S3No'}).text
        price_str = soup.find('div', attrs={'class': '_1svub _lf05o _9a071_2MEB_'}).text
        price = price_str.split(',')
        price = float(f'{price[0]}.{price[1][:2]}')
        print(title)
        print(price)
        print(_price)
        if (_price < price):
            send_mail(_url, _price, _mail)
    except:
        try:
            db = mysql.connector.connect(host='', user="", password="", database="")
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM info WHERE id = '{_id}'")
            db.commit()
            
        except mysql.connector.Error as error:
            print(f"Failed to delete row in MySQL: {error}")
        
        finally:
            if (db.is_connected()):
                cursor.close()
                db.close()

def send_mail(_url, _price, _mail):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('', '')
    subject = 'Price Fell Down!'
    body = f'Check the allegro link {_url} the price now is {_price} zl'

    msg = f"Subject: {subject} \n\n{body}"

    server.sendmail('mypythonmailmm@gmail.com', _mail, msg)

    print('Email Has Been Sent')

    server.quit()
    

try:
    db = mysql.connector.connect(host='', user="", password="", database="")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM info")
    rows = cursor.fetchall()
    
except mysql.connector.Error as error:
    print(f"Failed to fetch data from MySQL: {error}")
    
finally:
        if (db.is_connected()):
            cursor.close()
            db.close()
            
for x in rows:
    _id        = x[0]
    _url       = x[1]
    _datetime  = x[2]
    _price     = x[3]
    _mail      = x[4]
    _life_span = x[5]
    if _life_span == 1:
        _life_span = 0
    if datetime.now() - _datetime > timedelta(_life_span):
        try:
            db = mysql.connector.connect(host='', user="", password="", database="")
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM info WHERE id = '{_id}'")
            db.commit()
            
        except mysql.connector.Error as error:
            print(f"Failed to delete row in MySQL: {error}")
        
        finally:
            if (db.is_connected()):
                cursor.close()
                db.close()
    else: 
        check_price(_url, _price, _mail, _id)
        time.sleep(15)
        

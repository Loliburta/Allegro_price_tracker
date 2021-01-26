from flask import Flask
from flask import render_template, redirect, request, url_for, flash
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = ''

@app.route('/', methods=["GET", "POST"])
def hello_world():
    user_input_URL = None
    user_input_price = None
    user_input_mail = None
    user_input_life_span = None

    if request.method == 'POST':
        try:
            db = mysql.connector.connect(host='', user="", password="", database="")
            cursor = db.cursor()
            
            user_input_URL = request.form.get('user_input_URL')
            print(f"url = {user_input_URL}")
            user_input_price = request.form.get('user_input_price')
            print(f"price = {user_input_price}")
            user_input_mail = request.form.get('user_input_mail')
            print(f"mail = {user_input_mail}")
            user_input_life_span = request.form.get('user_input_life_span')
            print(f"life_span = {user_input_life_span}")
            
            cursor.execute("INSERT INTO info (url, creation_date, price, mail, life_span) VALUES (%s, %s, %s, %s, %s)", (user_input_URL, datetime.now(), user_input_price, user_input_mail, user_input_life_span))
            db.commit()
            flash("We are now tracking this product. We will notify you via email as soon as the desired price is hit.")
            
        except mysql.connector.Error as error:
            print(f"Failed to create row in MySQL: {error}")
            
        finally:
            if (db.is_connected()):
                cursor.close()
                db.close()
                print("MySQL connection is closed")
    return render_template('index.html')

@app.route('/view')
def view():
    try:
        db = mysql.connector.connect(host='', user="", password="", database="")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM info")
        rows = cursor.fetchall()
        
    except mysql.connector.Error as error:
        print(f"Failed to fetch rows from MySQL: {error}")
        
    finally:
        cursor.close()
        db.close()
        print("MySQL connection is closed")
    return render_template("view.html", values=rows)


if __name__ == "__main__":
    app.run(debug=True,
            host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))
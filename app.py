from flask import Flask, request, render_template,redirect,url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Plai1412',
    database = 'user_info',
    port=3306
)

cursor = db.cursor(dictionary=True)

# Register Page
@app.route("/create-regis",methods=['POST','GET'])
def register():
    if request.method == "POST":
        user_email = request.form['email']
        username = request.form['user_name']
        password = request.form['password']
        password_hash = generate_password_hash(password)
    
        try:
            cursor.execute(" INSERT INTO users (username,email,password_hash) VALUES (%s,%s,%s) "
                           ,(username,user_email,password_hash))
            db.commit()
            return redirect(url_for('login-form'))
        except mysql.connector.IntegrityError:
            return "Username and Email already Exists!" 
    return render_template('register.html')

# Login Page

@app.route('/login-form',methods=['POST',"GET"])
def login_form():
    user_email = request.form['email']
    user_name = request.form['user_name']
    password = request.form['password']
    query_from_db = "SELECT * FROM users WHERE username = %s and email = %s and password_hash = %s"
    
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    
    for user in users:
        if user_name == user['username'] and user_email == user['email'] and check_password_hash(user['password_hash'],password):
            return redirect(url_for('main.html'))
        else:
            return "Fail Login"
        
    return render_template('login.html')
@app.route('/main')
def main():
    return render_template('main.html')
@app.route('/')
def first_page():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
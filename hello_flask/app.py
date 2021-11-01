from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)



#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )


#Assignment 3 
def decodeToken(authToken):
    decoded = jwt.decode(authToken, JWT_SECRET, algorithms=["HS256"])
    tokenString = decoded.get('username')
    print("this is token")
    print(tokenString) 
    return tokenString

def checkToken(authToken):
    print(authToken)
    tokenString = decodeToken(authToken)
    cur = global_db_con.cursor()

    dbUser = "select exists (select username from users where username = '"
    dbUser += tokenString
    dbUser += "' limit 1);"
    cur.execute(dbUser)
    r = cur.fetchone()
    print(r[0])
    if r[0] == True:
        return True
    return False
@app.route('/auth3', methods=['POST']) #endpoint 
def auth3():
        
    print(request.form)
    cur = global_db_con.cursor()
    userSelectP = "select password from users where username='"
    userSelectP += request.form['username']
    userSelectP += "';"
    cur.execute(userSelectP)
 
    #fetching next row from database books
    r = cur.fetchone()
    #store row inside variable to compare w/ user request form starting at index 0 
    existingUser = str(r[0]) 
    print(str(r[0]))
    #if statment to compare passwords with form
    if bcrypt.checkpw(bytes(request.form['password'], 'utf-8'), existingUser.encode('utf-8')):
        jwt_str = jwt.encode({"username": request.form['username'], "password" : request.form['password']}, JWT_SECRET, algorithm="HS256")
        return json_response(jwt=jwt_str)
    print("Error")
    return json_response(status='401', msg='Invalid Login')
   
@app.route('/signup', methods=['POST']) #endpoint
def signup():
    print(request.form)
    insertUser = request.form['newUser']
    insertPass = request.form['newPass']
    
    salted = bcrypt.hashpw(bytes(request.form['newPass'], 'utf-8'), bcrypt.gensalt(10))
    print(insertUser)

    submission = "insert into users(username, password) values ( '" 
    submission += str(insertUser)
    submission += "','" 
    submission += str(salted.decode('utf-8'))
    submission += "');"
    print(submission)
    
    cur = global_db_con.cursor()
    #will run the sql command submission
    cur.execute(submission)
    #saves user into databse 
    global_db_con.commit()

    return json_response(status="good")

@app.route('/getBooks', methods=['GET']) #endpoint
def getBooks():

    print("Verifying the JWT")
    authorizeJWT = request.headers.get('AuthorizeInfo')
    tokenVal = checkToken(authorizeJWT)

    if tokenVal == False:
        return json_response(status='404', msg='Invalid JWT Token')

    cur = global_db_con.cursor()
    bookName = "select book_name from books;"
    cur.execute(bookName)
    gotBookName = cur.fetchall()
    print(gotBookName)
    
    bookPrice = "select book_price from books;" 
    cur.execute(bookPrice)
    gotBookPrice = cur.fetchall()
    print(gotBookPrice)
    
    return json_response(jwt = authorizeJWT, book_name=gotBookName, book_price=gotBookPrice)

@app.route('/bookPurchase', methods = ['POST'])
def bookPurchase():
    cur = global_db_con.cursor()
    tokenString = request.headers.get('AuthorizeInfo') 
    bookForm = request.form['book']
    buyTime = datetime.datetime.now()
    decToken = decodeToken(tokenString)

    dbUserEntry = "insert into purchases(userID, bookID, buyTime) VALUES('" 
    dbUserEntry += str(decToken)
    dbUserEntry += "','"
    dbUserEntry += str(bookForm)
    dbUserEntry += "','"
    dbUserEntry += str(buyTime)
    dbUserEntry += "');"

    print(dbUserEntry)

    cur.execute(dbUserEntry)
    global_db_con.commit()

    return json_response(status = 'successful') 

#not part of assignment #3
@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    #cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    #global_db_con.commit()
    return json_response(status="good")

app.run(host='0.0.0.0', port=80)

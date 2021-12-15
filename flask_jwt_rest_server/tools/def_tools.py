import jwt
from flask import  request, g
from tools.logging import logger
from db_con import get_db_instance, get_db
import bcrypt

global_db_con = get_db()

def checkToken(username):

    print(username)
    cur = global_db_con.cursor()

    dbUser = "select exists (select username from users where username = '"
    dbUser += username
    dbUser += "' limit 1);"
    cur.execute(dbUser)
    r = cur.fetchone()
    #print(r[0])
    if r[0] == True:
        return True
    return False

def auth3(username, password):

    #print(request.form)
    cur = global_db_con.cursor()
        
    if checkToken(username) == False:
        return False
            
    userSelectP = "select password from users where username='"
    userSelectP += request.form['username']
    userSelectP += "';"
    cur.execute(userSelectP)
    #fetching next row from database books
    r = cur.fetchone()
    #store row inside variable to compare w/ user request form starting at index 0
    existingUser = str(r[0])
    #print(str(r[0]))
    #if statment to compare passwords with form                
    if bcrypt.checkpw(bytes(request.form['password'], 'utf-8'), existingUser.encode('utf-8')):
        return True
    return False

def signup(username, password):
            
        salted = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(10))

        submission = "insert into users(username, password) values ( '" 
        submission += str(username)
        submission += "','" 
        submission += str(salted.decode('utf-8'))
        submission += "');"
        print(submission)

        cur = global_db_con.cursor()
        #will run the sql command submission
        cur.execute(submission)
        #saves user into databse 
        global_db_con.commit()

def getBooks(colName):

    cur = global_db_con.cursor() 
    
    getString = "select " 
    getString += colName
    getString += " from books; "
    cur.execute(getString)
    reqJson = cur.fetchall()
    return reqJson

def db_purchases(userid, bookid, buytime):
    
    cur = global_db_con.cursor() 
    submission = "insert into purchases(userid, bookid, buytime) values( '"
    submission+= userid
    submission+= "','"
    submission+= bookid
    submission+= "','"
    submission+= buytime
    submission+= "');"
    print(submission)
    cur.execute(submission)
    global_db_con.commit()



from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.logging import logger
from tools.def_tools import auth3 

#testing random things 
import bcrypt
from db_con import get_db_instance, get_db

global_db_con = get_db()

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    password_from_user_form = request.form['password']
    print(password_from_user_form)
    existUser = request.form['username'] 
    print(existUser)

    if auth3(existUser, password_from_user_form) == True:
        user = {
        
                "sub" : existUser  #sub is used by pyJwt as the owner of the token
            
               }

    else:
        user = False; 

    if not user:
        print(password_from_user_form + " is incorrect")

        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )
    
    return json_response( token = create_token(user) , authenticated = True, username = existUser)


from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.def_tools import signup
from tools.logging import logger

def handle_request():
 
    logger.debug("Signup Handle Request")

    password_from_user_form = request.form['newPass']
    existUser = request.form['newUser']
             
    signup(existUser, password_from_user_form)
    
    user = {
            "sub" : existUser #sub is used by pyJwt as the owner of the token
           }

    return json_response( token = create_token(user) , authenticated = True, username = existUser)

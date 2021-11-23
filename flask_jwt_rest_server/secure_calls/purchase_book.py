from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.def_tools import db_purchases
from tools.logging import logger

def handle_request():
        logger.debug("Purchase Book Handle Request")
       
    
        print(request.form['userid'])
        print(request.form['bookid'])
        print(request.form['buytime'])
        
        db_purchases(request.form['userid'], request.form['bookid'], request.form['buytime'])
        return json_response( token = create_token(  g.jwt_data ) , books = {})

from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.def_tools import getBooks
from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")

    bookName = getBooks("book_name")
    bookPrice = getBooks("book_price")

    return json_response( token = create_token(  g.jwt_data ) , bookN = bookName, bookP = bookPrice)


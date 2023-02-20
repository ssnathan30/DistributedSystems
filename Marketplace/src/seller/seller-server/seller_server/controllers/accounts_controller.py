import json
import connexion
import six
import traceback
from seller_server.models.inline_response200 import InlineResponse200  # noqa: E501
from seller_server.models.inline_response400 import InlineResponse400  # noqa: E501
from seller_server.models.inline_response500 import InlineResponse500  # noqa: E501
from seller_server import util
from seller_server.controllers.db_utility import execute_query, QueryType, Database
from google.protobuf.json_format import MessageToJson
import logging
import pathlib
import time

def accounts_post(username, password, seller_id, name=None):  # noqa: E501
    """Create an account

     # noqa: E501

    :param username: 
    :type username: str
    :param password: 
    :type password: str
    :param name: 
    :type name: str
    :param seller_id: 
    :type seller_id: str

    :rtype: InlineResponse200
    """
    #Invalid/Missing input
    if not username or not password or not seller_id:
        return InlineResponse400(message="Username or password or seller_id not provided")
    
    #Insert data to Seller table
    query_ = '''
                INSERT INTO Seller 
                    (   
                        id,
                        seller_name
                    ) 
                VALUES 
                    ("{0}","{1}")
            '''.format(seller_id, name)
    try:
        response = execute_query(query_,Database.CUSTOMER,QueryType.INSERT)
        if response["error"].get("errorCode",-2) != 1:
            return InlineResponse400(message=response["error"]["errorMessage"])
    except Exception as e:
        return InlineResponse400(message=str(traceback.format_exc()))
    
    #Insert data to SellerLogin
    query_ = '''
                INSERT INTO Seller_Login 
                    (   
                        seller_id,
                        username,
                        password
                    ) 
                VALUES 
                    ({0},"{1}","{2}")
            '''.format(seller_id,username,password)
    try:
        response = execute_query(query_,Database.CUSTOMER,QueryType.INSERT)
    except Exception as e:
        return InlineResponse400(message=str(traceback.format_exc()))
    
    return InlineResponse200(message=json.dumps(response))

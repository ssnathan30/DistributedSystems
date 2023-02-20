import json
import connexion
import six

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.models.credentials import Credentials  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response401 import InlineResponse401  # noqa: E501
from swagger_server import util
from swagger_server.controllers.db_utility import execute_query, QueryType, Database
from google.protobuf.json_format import MessageToJson
import traceback
import logging
import pathlib
import time

src_dir = pathlib.Path(__file__).parent.parent.resolve()
logging.basicConfig(filename="{0}/logs/buyer_server_throughput.log".format(src_dir),
                    format='%(message)s',
                    )
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        logger.info(f'{func.__name__!r},{(t2-t1):.4f}')
        return result
    return wrap_func

def account_post(account):  # noqa: E501
    """Create a new buyer account

     # noqa: E501

    :param account: 
    :type account: dict | bytes

    :rtype: InlineResponse201
    """
    if connexion.request.is_json:
        account = Account.from_dict(connexion.request.get_json())  # noqa: E501
        #Insert data to Buyer table
        query_ = '''
                    INSERT INTO Buyer 
                        (   
                            id,
                            buyer_name
                        ) 
                    VALUES 
                        ("{0}","{1}")
                '''.format(account.buyer_id, account.name)
        try:
            response = execute_query(query_,Database.CUSTOMER,QueryType.INSERT)
            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))

        #Insert data to BuyerLogin
        query_ = '''
                    INSERT INTO Buyer_Login 
                        (   
                            buyer_id,
                            username,
                            password
                        ) 
                    VALUES 
                        ({0},"{1}","{2}")
                '''.format(account.buyer_id,account.username,account.password)
        try:
            response = execute_query(query_,Database.CUSTOMER,QueryType.INSERT)
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
        return InlineResponse201(message=json.dumps(response),buyer_id=account.buyer_id)

def login_post(credentials):  # noqa: E501
    """Log in to an existing account

     # noqa: E501

    :param credentials: 
    :type credentials: dict | bytes

    :rtype: InlineResponse2005
    """
    if connexion.request.is_json:
        credentials = Credentials.from_dict(connexion.request.get_json())  # noqa: E501
        #Check if user data exist
        if_exist =  '''
                        SELECT is_active
                        FROM Buyer_Login
                        WHERE username = "{0}"
                        AND password = "{1}"
                    '''.format(credentials.username, credentials.password)
        try:
            response = execute_query(if_exist,Database.CUSTOMER,QueryType.GET)
            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
            if response.get("rows",-4) == -4:
                return InlineResponse400(message="Username or password is incorrect")
            buyer_row = response.get("rows")[0].get("values")
            is_active = buyer_row[0].get("columnValue")
            if int(is_active):
                return InlineResponse400(message="Session Active")
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
        query = '''
                    UPDATE Buyer_Login
                    SET is_active = 1
                    WHERE username = "{0}"
                    AND password = "{1}"
                '''.format(credentials.username, credentials.password)
        try:
            response = execute_query(query,Database.CUSTOMER,QueryType.UPDATE)
            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))

        return InlineResponse2005(message="Login Successful")   

def logout_buyer_id_get(buyer_id):  # noqa: E501
    """Log out of an existing account

     # noqa: E501

    :param buyer_id: 
    :type buyer_id: int

    :rtype: InlineResponse2006
    """
    #Check if user data exist
    if_exist =  '''
                    SELECT is_active
                    FROM Buyer_Login
                    WHERE buyer_id = {0}
                '''.format(buyer_id)
    try:
        response = execute_query(if_exist,Database.CUSTOMER,QueryType.GET)
        if response["error"].get("errorCode") != 1:
            return InlineResponse400(message=response["error"]["errorMessage"])
        if response.get("rows",-4) == -4:
            return InlineResponse400(message="buyer_id is wrong")
        buyer_row = response.get("rows")[0].get("values")
        is_active = buyer_row[0].get("columnValue")
        if not int(is_active):
            return InlineResponse400(message="Invalid Operation. Please Login")
    except Exception as e:
        return InlineResponse400(message=str(traceback.format_exc()))
    # Set is_active to false
    query = '''
                UPDATE Buyer_Login
                SET is_active = 0
                WHERE buyer_id = {0}
            '''.format(buyer_id)
    try:
        response = execute_query(query,Database.CUSTOMER,QueryType.UPDATE)
        if response["error"].get("errorCode") != 1:
            return InlineResponse400(message=response["error"]["errorMessage"])
    except Exception as e:
        return InlineResponse400(message=str(traceback.format_exc()))
    
    return InlineResponse2006(message="logged out")

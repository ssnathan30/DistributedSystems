import json
import connexion
import six
import traceback
from seller_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from seller_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from seller_server.models.inline_response400 import InlineResponse400  # noqa: E501
from seller_server.models.inline_response401 import InlineResponse401  # noqa: E501
from seller_server.models.inline_response5001 import InlineResponse5001  # noqa: E501
from seller_server.models.inline_response5002 import InlineResponse5002  # noqa: E501
from seller_server import util
from seller_server.controllers.db_utility import execute_query, QueryType, Database
import pathlib
import logging
import time


src_dir = pathlib.Path(__file__).parent.parent.resolve()
logging.basicConfig(filename="{0}/logs/seller_server_throughput.log".format(src_dir),
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


def login_post(username, password):  # noqa: E501
    """Login

     # noqa: E501

    :param username: 
    :type username: str
    :param password: 
    :type password: str

    :rtype: InlineResponse2001
    """
    #Invalid/Missing input
    if not username or not password:
        return InlineResponse400(message="Username or password not provided")
    
    #Check if user data exist
    if_exist =  '''
                    SELECT is_active
                    FROM Seller_Login
                    WHERE username = "{0}"
                    AND password = "{1}"
                '''.format(username, password)
    try:
        response = execute_query(if_exist,Database.CUSTOMER,QueryType.GET)
        if response["error"].get("errorCode") != 1:
            return InlineResponse400(message=response["error"]["errorMessage"])
        if response.get("rows",-4) != -4:
            seller_row = response.get("rows")[0].get("values")
            is_active = seller_row[0].get("columnValue")
            if int(is_active):
                return InlineResponse400(message="Session Active")
    except Exception as e:
        return InlineResponse400(message=str(traceback.format_exc()))
    query = '''
                UPDATE Seller_Login
                SET is_active = 1
                WHERE username = "{0}"
                AND password = "{1}"
            '''.format(username, password)
    try:
        response = execute_query(query,Database.CUSTOMER,QueryType.UPDATE)
        if response["error"].get("errorCode") != 1:
            return InlineResponse400(message=response["error"]["errorMessage"])
    except Exception as e:
        return InlineResponse400(message=str(traceback.format_exc()))
    
    return InlineResponse2001(message="Login Successful")


def logout_post(seller_id):  # noqa: E501
    """Logout

     # noqa: E501

    :param seller_id: 
    :type seller_id: str

    :rtype: InlineResponse2002
    """
    #Invalid/Missing input
    if not seller_id:
        return InlineResponse400(message="seller_id not provided")
    
    #Check if user data exist
    if_exist =  '''
                    SELECT is_active
                    FROM Seller_Login
                    WHERE seller_id = {0}
                '''.format(seller_id)
    try:
        response = execute_query(if_exist,Database.CUSTOMER,QueryType.GET)
        if response["error"].get("errorCode") != 1:
            return InlineResponse400(message=response["error"]["errorMessage"])
        if response.get("rows",-4) == -4:
            return InlineResponse400(message=json.dumps(response))
        seller_row = response.get("rows")[0].get("values")
        is_active = seller_row[0].get("columnValue")
        if not int(is_active):
            return InlineResponse400(message="Invalid Operation. Please Login")
    except Exception as e:
        return InlineResponse400(message=str(traceback.format_exc()))
    # Set is_active to false
    query = '''
                UPDATE Seller_Login
                SET is_active = 0
                WHERE seller_id = {0}
            '''.format(seller_id)
    try:
        response = execute_query(query,Database.CUSTOMER,QueryType.UPDATE)
        if response["error"].get("errorCode") != 1:
            return InlineResponse400(message=response["error"]["errorMessage"])
    except Exception as e:
        return InlineResponse400(message=str(traceback.format_exc()))
    
    return InlineResponse2001(message="logged out")

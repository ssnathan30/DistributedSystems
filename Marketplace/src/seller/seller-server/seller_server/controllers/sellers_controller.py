import json
import connexion
import six
import traceback
from seller_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from seller_server.models.inline_response4001 import InlineResponse4001  # noqa: E501
from seller_server.models.inline_response404 import InlineResponse404  # noqa: E501
from seller_server.models.inline_response5002 import InlineResponse5002  # noqa: E501
from seller_server.controllers.db_utility import execute_query, QueryType, Database
from seller_server import util
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

def session_active(seller_id):
    
    #Check if user data exist
    if_exist =  '''
                    SELECT is_active
                    FROM Seller_Login
                    WHERE seller_id = {0}
                '''.format(seller_id)
    try:
        response = execute_query(if_exist,Database.CUSTOMER,QueryType.GET)
        if response["error"].get("errorCode") != 1:
            return False, InlineResponse4001(message=response["error"]["errorMessage"])
        if response.get("rows",-4) == -4:
            return False, InlineResponse4001(message="seller_id is wrong")
        seller_row = response.get("rows")[0].get("values")
        is_active = seller_row[0].get("columnValue")
        if not int(is_active):
            return False, None
    except Exception as e:
        return False, InlineResponse4001(message=str(traceback.format_exc()))
    
    return True, None


def seller_rating_get(seller_id):  # noqa: E501
    """Get seller rating

     # noqa: E501

    :param seller_id: 
    :type seller_id: str

    :rtype: InlineResponse2003
    """
    is_active, error = session_active(seller_id)
    if error:
        return error
    if is_active:
        query = ''' SELECT (feedback_thumbs_up - feedback_thumbs_down) as Rating
                    FROM Seller
                    WHERE id = {0} 
                '''.format(seller_id)
        try:
            response = execute_query(query,Database.CUSTOMER,QueryType.GET)

            if response["error"].get("errorCode") != 1:
                return InlineResponse404(message=response["error"]["errorMessage"])
            if response.get("rows",-4) == -4:
                return InlineResponse4001(message="No Ratings Available")
        except Exception as e:
            return InlineResponse404(message=str(traceback.format_exc()))
        return InlineResponse2003(message=json.dumps(response))
    else:
        return InlineResponse4001(message="Unauthorized")

from collections import defaultdict
import json
import connexion
import six
from suds.client import Client

import uuid
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.card_details import CardDetails  # noqa: E501
from swagger_server import util
from swagger_server.controllers.db_utility import execute_query, QueryType, Database
from google.protobuf.json_format import MessageToJson
import traceback
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import pathlib
import logging
import time

soap_host = os.getenv("soap_host", "localhost")
soap_port = os.getenv("soap_port", 8888)

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

def session_active(buyer_id):
    
    #Check if user data exist
    if_exist =  '''
                    SELECT is_active
                    FROM Buyer_Login
                    WHERE buyer_id = {0}
                '''.format(buyer_id)
    try:
        response = execute_query(if_exist,Database.CUSTOMER,QueryType.GET)
        if response["error"].get("errorCode") != 1:
            return False, InlineResponse400(message=response["error"]["errorMessage"])
        if response.get("rows",-4) == -4:
            return False, InlineResponse400(message="buyer_id is wrong")
        seller_row = response.get("rows")[0].get("values")
        is_active = seller_row[0].get("columnValue")
        if not int(is_active):
            return False, None
    except Exception as e:
        return False, InlineResponse400(message=str(traceback.format_exc()))
    
    return True, None

@timer_func
def purchase_history_get(buyer_id):  # noqa: E501
    """Get purchase history

     # noqa: E501

    :param buyer_id: 
    :type buyer_id: int

    :rtype: InlineResponse2004
    """
    is_active, error = session_active(buyer_id)
    if error:
        return error
    if is_active:
        query = """ SELECT * FROM Purchase_History
                    WHERE buyer_id="{0}"
                """.format(buyer_id)
        try:
            response = execute_query(query, Database.PRODUCT, QueryType.GET)

            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
        return InlineResponse200(buyer_id=buyer_id,message=json.dumps(response))
    else:
           return InlineResponse400(message="Unauthorized")

@timer_func
def purchase_post(buyer_id, card_details):  # noqa: E501
    """Purchase items added in the cart

     # noqa: E501

    :param buyer_id: 
    :type buyer_id: int
    :param card_details: 
    :type card_details: dict | bytes

    :rtype: InlineResponse2001
    """
    if connexion.request.is_json:
        card_details = CardDetails.from_dict(connexion.request.get_json())  # noqa: E501
    
    is_active, error = session_active(buyer_id)
    if error:
        return error
    if is_active:
        query = """ SELECT * FROM cart
                    WHERE buyer_id="{0}"
                """.format(buyer_id)
        try:
            items_in_cart = execute_query(query, Database.PRODUCT, QueryType.GET)
            if items_in_cart["error"].get("errorCode") != 1:
                return InlineResponse400(message=items_in_cart["error"]["errorMessage"])
            if items_in_cart.get("rows", -4) != -4:
                # call soap server
                client = Client(f'http://{soap_host}:{soap_port}/?wsdl')
                transaction_status = client.service.process_transaction(card_details.name,card_details.card_number,card_details.expiration_date)
                if transaction_status:
                    items = []
                    for row in items_in_cart["rows"]:
                        temp = {}
                        for value in row["values"]:
                            if value["columnName"] == "item_id":
                                temp["item_id"] = value["columnValue"]
                            if value["columnName"] == "quantity":
                                temp["quantity"] = value["columnValue"]
                        items.append(temp)
                    # Unique transcation ID
                    t_id = uuid.uuid4().hex
                    #update the items table
                    for item_map in items:
                        _item_id = item_map["item_id"]
                        _quantity = item_map["quantity"]
                        try:
                            query = ''' SELECT quantity 
                                        FROM Item
                                        WHERE id = {0} 
                                    '''.format(_item_id)
                            response = execute_query(query,Database.PRODUCT,QueryType.GET)
                            if response["error"].get("errorCode") != 1:
                                return InlineResponse400(message=response["error"]["errorMessage"])
                            if response.get("rows",-4) == -4:
                                return InlineResponse400(message="Item doesn't exist or cannot be removed")
                            
                            existing_quantity = response.get("rows")[0].get("values")
                            existing_quantity = int(existing_quantity[0].get("columnValue"))

                            if int(existing_quantity) <= int(_quantity):
                                delete_query =  ''' DELETE 
                                                    FROM Item
                                                    WHERE id = {0}
                                                '''.format(_item_id)
                                response = execute_query(delete_query,Database.PRODUCT,QueryType.DELETE)
                            else:
                                to_update = int(existing_quantity)- int(_quantity)
                                update_query =  ''' UPDATE Item 
                                                    SET quantity = {0}
                                                    WHERE id = {1}
                                                '''.format(int(to_update),int(_item_id))
                                response = execute_query(update_query,Database.PRODUCT,QueryType.UPDATE)
                            
                            #update Buyer table with number items purchased
                            buyer_update =  '''
                                                UPDATE Buyer
                                                SET number_of_items_purchased = number_of_items_purchased + {0}
                                                WHERE id = {1};
                                            '''.format(int(_quantity),buyer_id)
                            response = execute_query(buyer_update,Database.PRODUCT,QueryType.UPDATE)

                            #update purchase history
                            purchase_history =  '''
                                                INSERT INTO Purchase_History
                                                (
                                                    t_id, buyer_id, item_id, quantity
                                                )
                                                VALUES
                                                (
                                                "{0}",{1},{2},{3}
                                                );
                                            '''.format(t_id,buyer_id,_item_id,_quantity)
                            response = execute_query(purchase_history,Database.PRODUCT,QueryType.INSERT)
                        except Exception as e:
                            return InlineResponse400(message=str(traceback.format_exc()))  
                    #clear cart
                    query = """ DELETE FROM cart
                                WHERE buyer_id="{0}"
                            """.format(buyer_id)
                    response = execute_query(query, Database.PRODUCT, QueryType.DELETE)
                else:
                    return InlineResponse400(message="Transaction Failed. Please try again")
            else:
                return InlineResponse2001(message="Cart is empty. Purchase cannot be made")
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
        return InlineResponse2001(message="Order Purchased with Transaction ID : {0}".format(t_id))
    else:
        return InlineResponse400(message="Unauthorized")

@timer_func
def search_items_get(item_category, keywords, buyer_id):  # noqa: E501
    """Search for items

     # noqa: E501

    :param item_category: 
    :type item_category: int
    :param keywords: 
    :type keywords: str
    :param buyer_id: 
    :type buyer_id: int

    :rtype: InlineResponse200
    """

    is_active, error = session_active(buyer_id)
    if error and error != "":
        return error
    if is_active:
        query = ''' SELECT id,item_name,keywords
                    FROM Item
                    WHERE item_category = {0}
                '''.format(item_category)
        try:
            response = execute_query(query,Database.PRODUCT,QueryType.GET)
            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
            if response.get("rows",-4) == -4:
                return InlineResponse400(message="No Ratings Available")
            key_map = defaultdict(list)
            for row in response["rows"]:
                temp = {}
                for value in row["values"]:
                    if value["columnName"] == "keywords":
                        temp["keywords"] = value["columnValue"].split(",")
                    if value["columnName"] == "item_name":
                        temp["item_name"] = value["columnValue"]
                    if value["columnName"] == "id":
                        temp["id"] = value["columnValue"]
                for word in temp["keywords"]:
                    key_map[word].append((temp["item_name"],temp["id"]))
            choices = key_map.keys()
            result = []
            for word in keywords.split(","):
                match = process.extract(word, choices, limit=1)
                result.append(key_map[match[0][0]])
            return InlineResponse200(buyer_id=buyer_id,message=json.dumps(result))
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
    else:
        return InlineResponse400(message="Unauthorized")

@timer_func
def seller_feedback_post(seller_id, buyer_id, transaction_id, item_id, feedback_rating):  # noqa: E501
    """Provide seller Feedback

     # noqa: E501

    :param seller_id: 
    :type seller_id: int
    :param buyer_id: 
    :type buyer_id: int
    :param transaction_id: 
    :type transaction_id: str
    :param item_id: 
    :type item_id: int
    :param feedback_rating: -1 for thumbs down and 1 for thumbs up
    :type feedback_rating: int

    :rtype: InlineResponse2003
    """
    is_active, error = session_active(buyer_id)
    if error and error != "":
        return error
    if is_active:
        if feedback_rating not in [-1, 1]:
            return InlineResponse400(message="Invalid Feedback Type")
        try:
            # Check purchase history for valid purchase
            query = ''' SELECT feedback_thumbsup, feedback_thumbsdown
                    FROM Purchase_History
                    WHERE buyer_id = {0} AND
                    item_id = {1} AND
                    t_id = "{2}"
                '''.format(buyer_id,item_id,transaction_id)
            response = execute_query(query,Database.PRODUCT,QueryType.GET)
            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
            if response.get("rows",-4) == -4:
                return InlineResponse400(message="No such transaction made !! Check your inputs")
            rows = response["rows"][0]
            for value in rows["values"]:
                if value["columnName"] == "feedback_thumbsup":
                    thumbs_up = int(value["columnValue"])
                if value["columnName"] == "feedback_thumbsdown":
                    thumbs_down = int(value["columnValue"])
            if thumbs_up > 0 or thumbs_down > 0:
                return InlineResponse400(message="Only one feebback can be provided per transaction per item")

            if feedback_rating == 1:
                f_type = "feedback_thumbs_up"
            else:
                f_type = "feedback_thumbs_down"

            # Update seller table with feedback
            query = ''' UPDATE Seller
                        SET {0} = {0} + 1
                        WHERE id = {1}
                    '''.format(f_type,seller_id)
            response = execute_query(query,Database.CUSTOMER,QueryType.UPDATE)
            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])

            if feedback_rating == 1:
                f_type = "feedback_thumbsup"
            else:
                f_type = "feedback_thumbsdown"
            
            # Update purchase history with feedback
            query = ''' UPDATE Purchase_History
                        SET {0} =  1
                        WHERE buyer_id = {1} AND
                        item_id = {2} AND
                        t_id = "{3}"
                    '''.format(f_type,buyer_id,item_id,transaction_id)
            response = execute_query(query,Database.PRODUCT,QueryType.UPDATE)
            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])

            return InlineResponse2003(message="Thanks for providing feedback !!")
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
    else:
        return InlineResponse400(message="Unauthorized")

@timer_func
def seller_rating_get(seller_id, buyer_id):  # noqa: E501
    """Get seller rating

     # noqa: E501

    :param seller_id: 
    :type seller_id: int
    :param buyer_id: 
    :type buyer_id: int

    :rtype: InlineResponse2002
    """
    is_active, error = session_active(buyer_id)
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
                return InlineResponse400(message=response["error"]["errorMessage"])
            if response.get("rows",-4) == -4:
                return InlineResponse400(message="No Ratings Available")
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
        return InlineResponse2002(message=json.dumps(response),buyer_id=buyer_id)
    else:
        return InlineResponse400(message="Unauthorized")

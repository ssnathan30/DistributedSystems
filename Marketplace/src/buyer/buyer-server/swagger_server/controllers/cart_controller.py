import json
import connexion
import six

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400
from swagger_server.models.inline_response200 import InlineResponse200
from swagger_server import util
from swagger_server.controllers.db_utility import execute_query, QueryType, Database
import traceback
import logging
import pathlib
import os
import time

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


def cart_add_post(body):  # noqa: E501
    """Add item to shopping cart

    Adds an item to the shopping cart of a buyer # noqa: E501

    :param body: Item ID and quantity to be added to cart
    :type body: dict | bytes

    :rtype: Inline200
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
        is_active, error = session_active(body.buyer_id)
        if error:
            return error
        if is_active:
            query = """
                        INSERT INTO cart 
                            (buyer_id, item_id, quantity) 
                        VALUES 
                            ({0},{1},{2})                      
                    """.format(body.buyer_id,body.item_id,body.quantity)
            try:
                response = execute_query(query,Database.PRODUCT,QueryType.INSERT)

                if response["error"].get("errorCode") != 1:
                    return InlineResponse400(message=response["error"]["errorMessage"])
            except Exception as e:
                return InlineResponse400(message=str(traceback.format_exc()))
            return InlineResponse200(message=json.dumps(response),buyer_id=body.buyer_id)
        else:
            return InlineResponse400(message="Unauthorized")


def cart_remove_delete(item_id, quantity, buyer_id):  # noqa: E501
    """Remove item from shopping cart

    Removes an item from the shopping cart of a buyer # noqa: E501

    :param item_id: ID of the item to be removed from the cart
    :type item_id: int
    :param quantity: Quantity of the item to be removed from the cart
    :type quantity: int
    :param buyer_id: ID of the buyer whose cart the item should be removed from
    :type buyer_id: int

    :rtype: None
    """
    is_active, error = session_active(buyer_id)
    if error:
        return error
    if is_active:
        query = ''' SELECT quantity 
                    FROM cart
                    WHERE item_id = {0} AND
                    buyer_id = {1} 
                '''.format(item_id,buyer_id)
        try:
            response = execute_query(query,Database.PRODUCT,QueryType.GET)
            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
            if response.get("rows",-4) == -4:
                return InlineResponse400(message="Item doesn't exist or cannot be removed")
            
            existing_quantity = response.get("rows")[0].get("values")
            existing_quantity = int(existing_quantity[0].get("columnValue"))

            if int(existing_quantity) <= int(quantity):
                delete_query =  ''' DELETE 
                                    FROM cart
                                    WHERE item_id = {0} AND
                                    buyer_id = {1} 
                                '''.format(item_id,buyer_id)
                response = execute_query(delete_query,Database.PRODUCT,QueryType.DELETE)
            else:
                to_update = int(existing_quantity)- int(quantity)
                update_query =  ''' UPDATE cart 
                                    SET quantity = {0}
                                    WHERE item_id = {1} AND
                                    buyer_id = {2} 
                                '''.format(int(to_update),int(item_id),buyer_id)
                response = execute_query(update_query,Database.PRODUCT,QueryType.UPDATE)
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
        return InlineResponse200(message=json.dumps(response),buyer_id=buyer_id)
    else:
        return InlineResponse400(message="Unauthorized")


def clear_cart_post(buyer_id):  # noqa: E501
    """Clear the shopping cart for a given buyer

     # noqa: E501

    :param buyer_id: ID of the buyer whose shopping cart should be cleared
    :type buyer_id: int

    :rtype: None
    """
    is_active, error = session_active(buyer_id)
    if error:
        return error
    if is_active:
        query = """ DELETE FROM cart
                    WHERE buyer_id="{0}"
                """.format(buyer_id)
        try:
            response = execute_query(query, Database.PRODUCT, QueryType.DELETE)

            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
        return InlineResponse200(message=json.dumps(response),buyer_id=buyer_id)
    else:
           return InlineResponse400(message="Unauthorized")


def display_cart_get(buyer_id):  # noqa: E501
    """Get the contents of the shopping cart for a given buyer

     # noqa: E501

    :param buyer_id: ID of the buyer whose shopping cart should be displayed
    :type buyer_id: int

    :rtype: InlineResponse2007
    """
    is_active, error = session_active(buyer_id)
    if error:
        return error
    if is_active:
        query = """ SELECT * FROM cart
                    WHERE buyer_id="{0}"
                """.format(buyer_id)
        try:
            response = execute_query(query, Database.PRODUCT, QueryType.GET)            

            if response["error"].get("errorCode") != 1:
                return InlineResponse400(message=response["error"]["errorMessage"])
        except Exception as e:
            return InlineResponse400(message=str(traceback.format_exc()))
        return InlineResponse200(message=json.dumps(response),buyer_id=buyer_id)
    else:
           return InlineResponse400(message="Unauthorized")

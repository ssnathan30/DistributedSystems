import json
import connexion
import six

from seller_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from seller_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from seller_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from seller_server.models.inline_response201 import InlineResponse201  # noqa: E501
from seller_server.models.inline_response4002 import InlineResponse4002  # noqa: E501
from seller_server.models.inline_response401 import InlineResponse401  # noqa: E501
from seller_server.models.inline_response404 import InlineResponse404  # noqa: E501
from seller_server.models.inline_response4041 import InlineResponse4041  # noqa: E501
from seller_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from seller_server import util
from seller_server.controllers.db_utility import execute_query, QueryType, Database
import traceback
import pathlib
import logging
import time

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
            return False, InlineResponse4002(message=response["error"]["errorMessage"])
        if response.get("rows",-4) == -4:
            return False, InlineResponse4002(message="seller_id is wrong")
        seller_row = response.get("rows")[0].get("values")
        is_active = seller_row[0].get("columnValue")
        if not int(is_active):
            return False, None
    except Exception as e:
        return False, InlineResponse4002(message=str(traceback.format_exc()))
    
    return True, None


def display_get(seller_id):  # noqa: E501
    """Display items

     # noqa: E501

    :param seller_id: 
    :type seller_id: str

    :rtype: InlineResponse2007
    """
    #Invalid/Missing input
    is_active, error = session_active(seller_id)
    if error:
        return error
    if is_active:
        query = ''' SELECT *  
                    FROM Item
                    WHERE seller_id = {0} 
                '''.format(seller_id)
        try:
            response = execute_query(query,Database.PRODUCT,QueryType.GET)

            if response["error"].get("errorCode") != 1:
                return InlineResponse404(message=response["error"]["errorMessage"])
            if response.get("rows",-4) == -4:
                return InlineResponse4002(message="Item doesn't exist or cannot be removed")
        except Exception as e:
            return InlineResponse404(message=str(traceback.format_exc()))
        return InlineResponse2007(message=json.dumps(response))
    else:
        return InlineResponse401(message="Unauthorized")


def items_item_id_delete(item_id,quantity,seller_id):  # noqa: E501
    """Remove an item from sale

     # noqa: E501

    :param item_id: 
    :type item_id: str
    :param quantity: 
    :type quantity: int
    :param seller_id: 
    :type seller_id: str

    :rtype: InlineResponse2005
    """
    is_active, error = session_active(seller_id)
    if error:
        return error
    if is_active:
        query = ''' SELECT quantity 
                        FROM Item
                        WHERE id = {0} AND
                        seller_id = {1} 
                    '''.format(item_id,seller_id)
        try:
            response = execute_query(query,Database.PRODUCT,QueryType.GET)

            if response["error"].get("errorCode") != 1:
                return InlineResponse404(message=response["error"]["errorMessage"])
            if response.get("rows",-4) == -4:
                return InlineResponse4002(message="Item doesn't exist or cannot be removed")
            
            existing_quantity = response.get("rows")[0].get("values")
            existing_quantity = int(existing_quantity[0].get("columnValue"))

            if int(existing_quantity) <= int(quantity):
                delete_query =  ''' DELETE 
                                    FROM Item
                                    WHERE id = {0} AND
                                    seller_id = {1} 
                                '''.format(item_id,seller_id)
                response = execute_query(delete_query,Database.PRODUCT,QueryType.DELETE)
            else:
                to_update = int(existing_quantity)- int(quantity)
                update_query =  ''' UPDATE Item 
                                    SET quantity = {0}
                                    WHERE id = {1} AND
                                    seller_id = {2} 
                                '''.format(int(to_update),int(item_id),seller_id)
                response = execute_query(update_query,Database.PRODUCT,QueryType.UPDATE)
        except Exception as e:
            return InlineResponse404(message=str(traceback.format_exc()))
        return InlineResponse2005(message=json.dumps(response))
    else:
        return InlineResponse401(message="Unauthorized")


def items_item_id_sale_price_put(item_id, new_sale_price, seller_id):  # noqa: E501
    """Change the sale price of an item

     # noqa: E501

    :param item_id: 
    :type item_id: str
    :param new_sale_price: 
    :type new_sale_price: float
    :param seller_id: 
    :type seller_id: str

    :rtype: InlineResponse2004
    """
    is_active, error = session_active(seller_id)
    if error:
        return error
    if is_active:
        query = '''
                UPDATE Item
                SET sale_price = {0}
                WHERE seller_id = {1}
                AND id = {2}
            '''.format(new_sale_price, seller_id, item_id)
        try:
            response = execute_query(query,Database.PRODUCT,QueryType.UPDATE)
            if response["error"].get("errorCode") != 1:
                return InlineResponse404(message=response["error"]["errorMessage"])
        except Exception as e:
            return InlineResponse404(message=str(traceback.format_exc()))
        return InlineResponse2004(message=json.dumps(response))
    else:
        return InlineResponse401(message="Unauthorized") 


def items_post(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id):  # noqa: E501
    """Put an item for sale

     # noqa: E501

    :param item_id: 
    :type item_id: str
    :param item_name: 
    :type item_name: str
    :param item_category: 
    :type item_category: str
    :param keywords: 
    :type keywords: List[str]
    :param condition: 
    :type condition: str
    :param sale_price: 
    :type sale_price: float
    :param quantity: 
    :type quantity: int
    :param seller_id: 
    :type seller_id: str

    :rtype: InlineResponse201
    """
    is_active, error = session_active(seller_id)
    if error:
        return error
    if is_active:
        #Insert data to Seller table
        query_ = '''
                    INSERT INTO Item 
                        (   
                            id,
                            item_name,
                            item_category,
                            keywords,
                            condition,
                            sale_price,
                            seller_id,
                            quantity
                        ) 
                    VALUES 
                        ({0},"{1}",{2},"{3}","{4}",{5},{6},{7})
                '''.format(item_id, item_name,item_category,keywords,condition,sale_price,seller_id,quantity)
        try:
            response = execute_query(query_,Database.PRODUCT,QueryType.INSERT)
            if response["error"].get("errorCode",-2) != -2:
                return InlineResponse4002(message=response["error"]["errorMessage"])
        except Exception as e:
            return InlineResponse4002(message=str(traceback.format_exc()))
        
        return InlineResponse201(message=json.dumps(response))
    else:
        return InlineResponse4002(message="Unauthorized") 

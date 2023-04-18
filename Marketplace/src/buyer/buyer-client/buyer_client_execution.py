from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from buyer_client import configuration
from pprint import pprint
import logging
from time import time
import pathlib

#config = buyer_client.Configuration()
#config.host = "http://10.0.0.108:8080"

buyer_account_instance = buyer_client.BuyerAccountApi(buyer_client.ApiClient())
cart_instance = buyer_client.CartApi()
buyer_action_instance = buyer_client.BuyerActionsApi()

src_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
logging.basicConfig(filename="{0}/logs/buyer_client_response.log".format(src_dir),
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

@timer_func
def create_account(username,password,buyer_id,name):
    account = buyer_client.Account(username=username,password=password,buyer_id=buyer_id,name=name) # Account | 
    try:
        # Create a new buyer account
        api_response = buyer_account_instance.account_post(account)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BuyerAccountApi->account_post: %s\n" % e)

@timer_func
def login(username,password):
    credentials = buyer_client.Credentials(username=username,password=password) # Credentials | 
    try:
        # Log in to an existing account
        api_response = buyer_account_instance.login_post(credentials)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BuyerAccountApi->login_post: %s\n" % e)

@timer_func
def logout(buyer_id):
    try:
        # Log out of an existing account
        api_response = buyer_account_instance.logout_buyer_id_get(buyer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BuyerAccountApi->logout_buyer_id_get: %s\n" % e)

@timer_func
def add_into_cart(item_id,buyer_id,quantity):
    body = buyer_client.Body(item_id=item_id,buyer_id=buyer_id,quantity=quantity) # Body | Item ID and quantity to be added to cart
    try:
        # Add item to shopping cart
        api_response = cart_instance.cart_add_post(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CartApi->cart_add_post: %s\n" % e)

@timer_func
def remove_from_cart(item_id,quantity,buyer_id):
    item_id = item_id   # int | ID of the item to be removed from the cart
    quantity = quantity # int | Quantity of the item to be removed from the cart
    buyer_id = buyer_id # int | ID of the buyer whose cart the item should be removed from

    try:
        # Remove item from shopping cart
        api_response = cart_instance.cart_remove_delete(item_id, quantity, buyer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CartApi->cart_remove_delete: %s\n" % e)

@timer_func
def clear_cart(buyer_id):
    buyer_id = buyer_id # int | ID of the buyer whose shopping cart should be cleared

    try:
        # Clear the shopping cart for a given buyer
        api_response = cart_instance.clear_cart_post(buyer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CartApi->clear_cart_post: %s\n" % e)

@timer_func
def display_cart(buyer_id):
    try:
        # Get the contents of the shopping cart for a given buyer
        api_response = cart_instance.display_cart_get(buyer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CartApi->display_cart_get: %s\n" % e)

@timer_func
def purchase_history(buyer_id):
    try:
        # Get purchase history
        api_response = buyer_action_instance.purchase_history_get(buyer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BuyerActionsApi->purchase_history_get: %s\n" % e)

@timer_func
def purchase(name,card_number,expiration_date,buyer_id):
    card_details = buyer_client.CardDetails(name=name,card_number=card_number,expiration_date=expiration_date,buyer_id=buyer_id) # CardDetails | 

    try:
        # Purchase items added in the cart
        api_response = buyer_action_instance.purchase_post(buyer_id, card_details)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BuyerActionsApi->purchase_post: %s\n" % e)

@timer_func
def search_items(item_category,keywords,buyer_id):
    try:
        # Search for items
        api_response = buyer_action_instance.search_items_get(item_category, keywords, buyer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BuyerActionsApi->search_items_get: %s\n" % e)

@timer_func
def send_feedback(seller_id, buyer_id, transaction_id, item_id, feedback_rating):
    try:
        # Provide seller Feedback
        api_response = buyer_action_instance.seller_feedback_post(seller_id, buyer_id, transaction_id, item_id, feedback_rating)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BuyerActionsApi->seller_feedback_post: %s\n" % e)

@timer_func
def seller_rating(seller_id,buyer_id):
    try:
        # Get seller rating
        api_response = buyer_action_instance.seller_rating_get(seller_id, buyer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BuyerActionsApi->seller_rating_get: %s\n" % e)

def execute():
    create_account(username="buyer_swami",password="buyer",buyer_id=1234,name="Swaminathan")
    login(username="buyer_swami",password="buyer")
    
    add_into_cart(item_id=100,buyer_id=1234,quantity=5)
    add_into_cart(item_id=101,buyer_id=1234,quantity=5)
    remove_from_cart(item_id=101,buyer_id=1234,quantity=3)
    display_cart(buyer_id=1234)
    
    search_items(item_category=9,keywords="Toy,violet",buyer_id=1234)
    search_items(item_category=1,keywords="violet",buyer_id=1234)
    
    purchase(name="swaminathan",card_number=1234567,expiration_date="01/01/1997",buyer_id=1234)
    purchase_history(buyer_id=1234)
    
    seller_rating(seller_id=1,buyer_id=1234)
    seller_rating(seller_id=123,buyer_id=1234)
    
    for i in range(100):
        add_into_cart(item_id=1,buyer_id=1234,quantity=1)
        clear_cart(buyer_id=1234)


if __name__ == '__main__':
    execute()

from __future__ import print_function
from time import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint
import pathlib
import logging


account_instance = seller_client.AccountsApi(seller_client.ApiClient())
auth_instance = seller_client.AuthenticationApi()
item_instance = seller_client.ItemsApi()
seller_instance = seller_client.SellersApi()

src_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
logging.basicConfig(filename="{0}/logs/seller_client_response.log".format(src_dir),
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
def create_account(username,password,seller_id,name):
    try:
        # Create an account
        api_response = account_instance.accounts_post(username, password, seller_id, name=name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AccountsApi->accounts_post: %s\n" % e)

@timer_func
def login(username,password):
    try:
        # Login
        api_response = auth_instance.login_post(username, password)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AuthenticationApi->login_post: %s\n" % e)

@timer_func
def logout(seller_id):
    try:
        # Logout
        api_response = auth_instance.logout_post(seller_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AuthenticationApi->logout_post: %s\n" % e)

@timer_func
def display_items(seller_id):
    try:
        # Display items
        api_response = item_instance.display_get(seller_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ItemsApi->display_get: %s\n" % e)

@timer_func
def remove_item(item_id,quantity,seller_id):
    try:
        # Remove an item from sale
        api_response = item_instance.items_item_id_delete(item_id, quantity, seller_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ItemsApi->items_item_id_delete: %s\n" % e)

@timer_func
def update_price(item_id,seller_id,new_sale_price):
    try:
        # Change the sale price of an item
        api_response = item_instance.items_item_id_sale_price_put(item_id, new_sale_price, seller_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ItemsApi->items_item_id_sale_price_put: %s\n" % e)

@timer_func
def add_item(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id):
    try:
        # Put an item for sale
        api_response = item_instance.items_post(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ItemsApi->items_post: %s\n" % e)

@timer_func
def seller_rating(seller_id):
    try:
        # Get seller rating
        api_response = seller_instance.seller_rating_get(seller_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SellersApi->seller_rating_get: %s\n" % e)

def execute():
    create_account(username="seller_swami",password="seller",name="Swaminathan",seller_id=123)
    login(username="seller_swami",password="seller")
    add_item(item_id=100, item_name="batman", item_category=9, keywords="Toy,Kids,Hero", condition="new", sale_price=100, quantity=200, seller_id=123)
    add_item(item_id=101, item_name="superman", item_category=9, keywords="Toy,Kids,Hero", condition="new", sale_price=100, quantity=202, seller_id=123)
    add_item(item_id=102, item_name="spiderman", item_category=9, keywords="Toy,Kids,Hero", condition="new", sale_price=100, quantity=200, seller_id=123)
    
    for i in range(100):
        update_price(item_id=101,seller_id=123,new_sale_price=99)

    remove_item(item_id=101,quantity=1,seller_id=123)
    display_items(seller_id=123)
    seller_rating(seller_id=123)
    logout(seller_id=123)


if __name__ == '__main__':
    execute()
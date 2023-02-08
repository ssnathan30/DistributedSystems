import socket
import sqlite3
import json
import time
import os
import sys
import logging
import traceback
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from heapq import *

class server_buyer:
    def __init__(self,db_host="localhost",db_port=7777) -> None:
        self.active = False
        self.db_host = db_host
        self.db_port = db_port

    def create_account(self,value):
        result = {}
        if self.active:
            result = {"message": "User session active"}
        else:
            buyer_id   = value["buyer_id"]
            username    = value["username"]
            password    = value["password"]
            query = '''
                        INSERT INTO buyers_info 
                            (   
                                id,
                                username, 
                                password
                            ) 
                        VALUES 
                            ("{0}","{1}","{2}")
                    '''.format(buyer_id, username, password)
            error_code, message, value  = self.execute_query(query)    
            if error_code == -1:
                result = {"message": message}
            else:
                result = {"message": "Account Created"}
        return 0, json.dumps(result)

    def login(self,value):
        result = {}
        if not self.active:
            buyer_id   = value["buyer_id"]
            username    = value["username"]
            password    = value["password"]
            query = '''
                        SELECT * FROM buyers_info 
                        WHERE username="{0}" AND
                        password="{1}" AND
                        id={2}
                    '''.format(username, password, buyer_id)
            
            error_code, message, value  = self.execute_query(query,True)

            if error_code == -1:
                result = {"message": message}
            else:
                if value is None or value == "":
                    result = {"message": "Login Failed !! Check your credentials or Sign up"} 
                else:
                    result = {"message": "Login Sucess !!"}
                    self.active = True
                    self.username = username
                    self.buyer_id = buyer_id
        else:
            result = {"message": "User session active"}
        return 0, json.dumps(result)

    def logout(self):
        if self.active:
            self.active = False
            self.username = None
            self.buyer_id = None
            return -1, json.dumps({"message": "Sucessfully Logged Out !!"})
        else:
            return 0, json.dumps({"message": "Invalid Operation. Please login!!"})

    def search_sale_items(self,value):
        result = ""
        if self.active:
            item_category = value["item_category"]
            keywords = value["keywords"]
            keywords = keywords.split(",")

            query = '''
                        SELECT id, name, keywords FROM items 
                        WHERE category="{0}"
                    '''.format(item_category)
            
            error_code, message, value  = self.execute_query(query,True)

            if error_code == -1:
                result = {"message": message}
            else:
                scores = []
                for item in value:
                    item_id = item[0]
                    item_name = item[1]
                    item_keywords = item[2].split(",")
                    for word in item_keywords:
                        score = int(process.extractOne(word, keywords)[1])
                        scores.append((-score,(item_id,item_name)))
                heapify(scores)
                
                ## Select top item
                items = []
                while score and len(items) < 1:
                    items.append(heappop(scores)[1])
                result = {"message": message, "value" : items}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)

    def add_item_to_cart(self,value):
        result = ""
        if self.active:
            item_id = value["item_id"]
            quantity = value["quantity"]

            query = """
                        INSERT INTO cart 
                            (buyer_id, item_id, quantity) 
                        VALUES 
                            ({0},{1},{2})                      
                    """.format(self.buyer_id,item_id,quantity)
            error_code, message, value  = self.execute_query(query)
            if error_code == -1:
                result = {"message": message}
            else:
                result = {"message": "Item Added to Cart !!"}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)

    def remove_item_from_cart(self,value):
        result = ""
        if self.active:
            item_id = value["item_id"]
            quantity = value["quantity"]

            query = ''' SELECT quantity 
                        FROM cart
                        WHERE id = {0} AND
                        buyer_id = {1} 
                    '''.format(item_id,self.buyer_id)
            error_code, message, value  = self.execute_query(query,True)
            if error_code == -1:
                result = {"message": message}
            else:
                if not value or value == "" or value[0][0] is None:
                    result = {"message": "Item cannot be removed."}
                else:
                    existing_amount = value[0][0]
                    update_query = ""
                    if int(existing_amount) <= int(quantity):
                        update_query =  ''' DELETE 
                                            FROM cart
                                            WHERE id = {0} AND
                                            buyer_id = {1} 
                                        '''.format(int(item_id),self.buyer_id)
                    else:
                        to_update = int(existing_amount)- int(quantity)
                        update_query =  ''' UPDATE cart 
                                            SET quantity = {0}
                                            WHERE id = {1} AND
                                            buyer_id = {2} 
                                        '''.format(int(to_update),int(item_id),self.buyer_id)
                    error_code, message, value  = self.execute_query(update_query)
                    if error_code == -1:
                        result = {"message": message}
                    else:
                        result = {"message": "Removed/Updated Items from Cart"}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)

    def clear_cart(self):
        result = ""
        if self.active:
            query = """
                        DELETE FROM cart 
                        WHERE buyer_id="{0}"
                    """.format(self.buyer_id)
            
            error_code, message, value  = self.execute_query(query)
            
            if error_code == -1:
                result = {"message": message}
            else:
                result = {"message": "Cleared Cart !!"}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)

    def display_cart(self):
        result = ""
        if self.active:
            query = """
                        SELECT * FROM cart 
                        WHERE buyer_id="{0}"
                    """.format(self.buyer_id)
            
            error_code, message, value  = self.execute_query(query,True)

            if error_code == -1:
                result = {"message": message}
            else:
                result = {"message": message, "value": value}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)

    def provide_feedback(self,feedback):
        pass

    def get_seller_rating(self,value):
        result = ""
        if self.active:
            seller_id = value["seller_id"]
            query = '''
                        SELECT feedback_thumbs_up, feedback_thumbs_down FROM sellers_info 
                        WHERE id="{0}" 
                    '''.format(seller_id)
            error_code, message, value  = self.execute_query(query,True)
            if error_code == -1:
                result = {"message": message}
            else:
                if (value[0][0] and value[0][1]) is None:
                    result = {"message": "No Ratings Available"}
                else:
                    result = {"message": message, "value": value}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)

    def get_purchase_history(self):
        pass

    def process(self,op_code,value,action):
        if op_code == 1: # Create Account
            return self.create_account(value)
        elif op_code == 2: # Login
            return self.login(value)
        elif op_code == 3: # Logout
            return self.logout()
        elif op_code == 4: # Seller rating
            return self.get_seller_rating(value)
        elif op_code == 5: # Add item to cart
            return self.add_item_to_cart(value)
        elif op_code == 6: # Remove item from cart
            return self.remove_item_from_cart(value)
        elif op_code == 7: # Clear cart
            return self.clear_cart()
        elif op_code == 8:
            return self.display_cart()
        elif op_code == 9:
            return self.search_sale_items(value)
        else:
            return 0, json.dumps({"message" : "No operation"})
    
    def execute_query(self,query,get_result=False):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.db_host, self.db_port))
            payload = {"query" : query, "get_result": get_result}
            payload = json.dumps(payload)
            s.sendall(payload.encode())
            data = s.recv(1024)
        try:
            data = json.loads(data)
            message = data["message"]
            error_code = data["error_code"]
            value = data["value"]
            return error_code, message, value
        except Exception as e:
            return -1, str(traceback.format_exc()), ""
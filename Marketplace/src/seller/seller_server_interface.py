import logging
import json
import selectors
import socket
import time
import traceback

class server_seller:
    def __init__(self,db_host="localhost",db_port=7777) -> None:
        self.active = False
        self.db_host = db_host
        self.db_port = db_port

    def create_account(self,value,action):
        result = {}
        if self.active:
            result = {"message": "User session active"}
        else:
            seller_id   = value["seller_id"]
            username    = value["username"]
            password    = value["password"]
            query = '''
                        INSERT INTO sellers_info 
                            (   
                                id,
                                username, 
                                password
                            ) 
                        VALUES 
                            ("{0}","{1}","{2}")
                    '''.format(seller_id, username, password)
            error_code, message, value  = self.execute_query(query)    
            if error_code == -1:
                result = {"message": message}
            else:
                result = {"message": "Account Created"}
        return 0, json.dumps(result)
    
    def login(self,value,action):
        result = {}
        if not self.active:
            seller_id   = value["seller_id"]
            username    = value["username"]
            password    = value["password"]
            query = '''
                        SELECT * FROM sellers_info 
                        WHERE username="{0}" AND
                        password="{1}" AND
                        id={2}
                    '''.format(username, password, seller_id)
            
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
                    self.seller_id = seller_id
        else:
            result = {"message": "User session active"}
        return 0, json.dumps(result)
    
    def logout(self):
        if self.active:
            self.active = False
            self.username = None
            self.seller_id = None
            return -1, json.dumps({"message": "Sucessfully Logged Out !!"})
        else:
            return 0, json.dumps({"message": "Invalid Operation. Please login!!"})
    
    def get_seller_rating(self):
        result = ""
        if self.active:
            query = '''
                        SELECT feedback_thumbs_up, feedback_thumbs_down FROM sellers_info 
                        WHERE id="{0}" 
                    '''.format(self.seller_id)
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
    
    def add_item(self,value):
        result = ""
        if self.active:
            item = value["item"]
            item_id = int(item["item_id"])
            item_name = item["item_name"]
            item_category = int(item["item_category"])
            keywords = item["keywords"]
            condition = item["condition"]
            sale_price = float(item["sale_price"])
            quantity = int(value["quantity"])

            query = """
                            INSERT INTO items 
                                (id, name, category, keywords, condition, sale_price, quantity, seller_id) 
                            VALUES 
                                ({0},"{1}",{2},"{3}","{4}",{5},{6},{7})                      
                    """.format(item_id,item_name,item_category,keywords,condition,sale_price,quantity,self.seller_id)
            error_code, message, value  = self.execute_query(query)
            if error_code == -1:
                result = {"message": message}
            else:
                result = {"message": "Item Added !!"}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)
    
    def change_price(self,value):
        result = ""
        if self.active:
            item_id = value["item_id"]
            sale_price = value["sale_price"]
            query = ''' UPDATE items
                        SET sale_price = {0}
                        WHERE id = {1} AND
                        seller_id = {2}
                    '''.format(sale_price,item_id,self.seller_id)
            error_code, message, value  = self.execute_query(query)
            if error_code == -1:
                result = {"message": message}
            else:
                result = {"message": "Updated Item price !!"}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)

    def remove_item(self,value):
        result = ""
        if self.active:
            item_id = value["item_id"]
            quantity = value["quantity"]
            query = ''' SELECT quantity 
                        FROM items
                        WHERE id = {0} AND
                        seller_id = {1} 
                    '''.format(item_id,self.seller_id)
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
                                            FROM items
                                            WHERE id = {0} AND
                                            seller_id = {1} 
                                        '''.format(int(item_id),self.seller_id)
                    else:
                        to_update = int(existing_amount)- int(quantity)
                        update_query =  ''' UPDATE items 
                                            SET quantity = {0}
                                            WHERE id = {1} AND
                                            seller_id = {2} 
                                        '''.format(int(to_update),int(item_id),self.seller_id)
                    error_code, message, value  = self.execute_query(update_query)
                    if error_code == -1:
                        result = {"message": message}
                    else:
                        result = {"message": "Removed/Updated Items"}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)
    
    def display_items(self):
        result = ""
        if self.active:
            query = """
                        SELECT * FROM items 
                        WHERE seller_id="{0}"
                    """.format(self.seller_id)
            
            error_code, message, value  = self.execute_query(query,True)
            
            if error_code == -1:
                result = {"message": message}
            else:
                result = {"message": message, "value": value}
        else:
            result = {"message": "Invalid Operation. Please login!!"}
        return 0, json.dumps(result)
    
    def process(self,op_code,value,action):
        if op_code == 1: # Create Account
            return self.create_account(value,action)
        elif op_code == 2: # Logi
            return self.login(value,action)
        elif op_code == 3:
            return self.logout()
        elif op_code == 4:
            return self.get_seller_rating()
        elif op_code == 5:
            return self.add_item(value)
        elif op_code == 6:
            return self.change_price(value)
        elif op_code == 7:
            return self.remove_item(value)
        elif op_code == 8:
            return self.display_items()
        else:
            return "No OP"
    
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

        
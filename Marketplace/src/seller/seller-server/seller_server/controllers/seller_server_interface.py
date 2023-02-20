
from enum import Enum
import logging
import json
import time
import traceback
import customer_pb2
import customer_pb2_grpc
import product_pb2
import product_pb2_grpc
import grpc
from google.protobuf.json_format import MessageToJson

class Database(Enum):
    CUSTOMER = 1
    PRODUCT = 2

class QueryType(Enum):
    GET = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4

class server_seller:
    def __init__(self,customer_db_host="localhost",customer_db_port=50051,product_db_host="localhost",product_db_port=8888) -> None:
        self.active = False
        self.customer_db_host = customer_db_host
        self.customer_db_port = customer_db_port
        self.product_db_host = product_db_host
        self.product_db_port = product_db_port

    def create_account(self,value,action):
        result = {}
        if self.active:
            result = {"message": "User session active"}
        else:
            seller_id   = value["seller_id"]
            username    = value["username"]
            password    = value["password"]
            name        = value["name"]
            query = '''
                        INSERT INTO Seller 
                            (   
                                id,
                                seller_name
                            ) 
                        VALUES 
                            ("{0}","{1}")
                    '''.format(seller_id, name)
            error_code, message, value  = self.execute_query(query,Database.CUSTOMER,QueryType.INSERT)    
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
        if op_code == 1:   # Create Account
            return self.create_account(value,action)
        elif op_code == 2: # Login
            return self.login(value,action)
        elif op_code == 3: # Logout
            return self.logout()
        elif op_code == 4: # GetSellerRating
            return self.get_seller_rating()
        elif op_code == 5: # AddItem
            return self.add_item(value)
        elif op_code == 6: # ChangePrice
            return self.change_price(value)
        elif op_code == 7: # RemoveItem
            return self.remove_item(value)
        elif op_code == 8: # Display
            return self.display_items()
        else:
            return "No OP"
    
    def execute_query(self,query,database,query_type="GET"):

        if database is Database.CUSTOMER:
            # Connect to the GRPC server
            channel = grpc.insecure_channel(f'{self.customer_db_host}:{self.customer_db_port}')
            stub = customer_pb2_grpc.DatabaseServerStub(channel)

            if query_type is QueryType.GET:
                get_data_request = customer_pb2.GetDataRequest(
                    query
                )
                # Call the GetData rpc
                get_data_response = stub.GetData(get_data_request)
                return get_data_response
            elif query_type is QueryType.INSERT :
                get_insert_request = customer_pb2.InsertDataRequest(
                    query
                )
                # Call the InsertData rpc
                get_insert_response = stub.InsertData(get_insert_request)
                return get_insert_response
            elif query_type is QueryType.UPDATE :
                get_update_request = customer_pb2.UpdateDataRequest(
                    query
                )
                # Call the UpdateData rpc
                get_update_response = stub.UpdateData(get_update_request)

                return get_update_response
            else:
                get_delete_request = customer_pb2.DeleteDataRequest(
                    query
                )
                # Call the DeleteData rpc
                get_delete_response = stub.DeleteData(get_delete_request)
                return get_delete_response
        else:
            # Connect to the GRPC server
            channel = grpc.insecure_channel(f'{self.product_db_host}:{self.product_db_port}')
            stub = product_pb2_grpc.DatabaseServerStub(channel)

            if query_type is QueryType.GET:
                get_data_request = product_pb2.GetDataRequest(
                    query
                )
                # Call the GetData rpc
                get_data_response = stub.GetData(get_data_request)
                return get_data_response
            elif query_type is QueryType.INSERT :
                get_insert_request = product_pb2.InsertDataRequest(
                    query
                )
                # Call the InsertData rpc
                get_insert_response = stub.InsertData(get_insert_request)
                return get_insert_response
            elif query_type is QueryType.UPDATE:
                get_update_request = product_pb2.UpdateDataRequest(
                    query
                )
                # Call the UpdateData rpc
                get_update_response = stub.UpdateData(get_update_request)
                return get_update_response
            else:
                get_delete_request = product_pb2.DeleteDataRequest(
                    query
                )
                # Call the DeleteData rpc
                get_delete_response = stub.DeleteData(get_delete_request)
                return get_delete_response

        
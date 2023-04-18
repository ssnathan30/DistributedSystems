from enum import Enum
import logging
import json
import os
import random
import time
import traceback
import grpc
from google.protobuf.json_format import MessageToJson
from swagger_server.controllers.customer_pb2 import *
from swagger_server.controllers.customer_pb2_grpc import *
from swagger_server.controllers.product_pb2 import *
from swagger_server.controllers.product_pb2_grpc import *

class Database(Enum):
    CUSTOMER = 1
    PRODUCT = 2

class QueryType(Enum):
    GET = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4

#customer_db_host = os.getenv("customer_host","localhost")
#customer_db_port = os.getenv("customer_port",50080)
#product_db_host = os.getenv("product_host","localhost")
#product_db_port = os.getenv("product_port",50060)

customer_db_list = list(os.getenv("customer_host_port").split(","))
product_db_list = list(os.getenv("product_host_port").split(","))

def execute_query(_query,database,query_type):
    if database is Database.CUSTOMER:
        # Connect to the GRPC server
        channel = grpc.insecure_channel(random.choice(customer_db_list))
        stub = CustomerDatabaseServerStub(channel)

        if query_type is QueryType.GET:
            get_data_request = GetDataRequest(
                query=_query
            )
            # Call the GetData rpc
            get_data_response = stub.GetData(get_data_request)
            return json.loads(MessageToJson(get_data_response))
        elif query_type is QueryType.INSERT :
            get_insert_request = InsertDataRequest(
                query=_query
            )
            # Call the InsertData rpc
            get_insert_response = stub.InsertData(get_insert_request)
            return json.loads(MessageToJson(get_insert_response))
        elif query_type is QueryType.UPDATE :
            get_update_request = UpdateDataRequest(
                query=_query
            )
            # Call the UpdateData rpc
            get_update_response = stub.UpdateData(get_update_request)
            return json.loads(MessageToJson(get_update_response))
        else:
            get_delete_request = DeleteDataRequest(
                query=_query
            )
            # Call the DeleteData rpc
            get_delete_response = stub.DeleteData(get_delete_request)
            return json.loads(MessageToJson(get_delete_response))
    else:
        # Connect to the GRPC server
        channel = grpc.insecure_channel(random.choice(product_db_list))
        stub = ProductDatabaseServerStub(channel)

        if query_type is QueryType.GET:
            get_data_request = GetRequest(
                query=_query
            )
            # Call the GetData rpc
            get_data_response = stub.Get(get_data_request)
            return json.loads(MessageToJson(get_data_response))
        elif query_type is QueryType.INSERT :
            get_insert_request = InsertRequest(
                query=_query
            )
            # Call the InsertData rpc
            get_insert_response = stub.Insert(get_insert_request)
            return json.loads(MessageToJson(get_insert_response))
        elif query_type is QueryType.UPDATE:
            get_update_request = UpdateRequest(
                query=_query
            )
            # Call the UpdateData rpc
            get_update_response = stub.Update(get_update_request)
            return json.loads(MessageToJson(get_update_response))
        else:
            get_delete_request = DeleteRequest(
                query=_query
            )
            # Call the DeleteData rpc
            get_delete_response = stub.Delete(get_delete_request)
            return json.loads(MessageToJson(get_delete_response))
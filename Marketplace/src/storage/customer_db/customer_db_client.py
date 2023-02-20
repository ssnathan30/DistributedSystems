import customer_pb2
import customer_pb2_grpc
import grpc
import json
from google.protobuf.json_format import MessageToJson

# Connect to the GRPC server
channel = grpc.insecure_channel('localhost:50051')
stub = customer_pb2_grpc.DatabaseServerStub(channel)

# Create a request object
get_data_request = customer_pb2.GetDataRequest(
    query='select * from Seller',
)

# Create a request object
get_update_request = customer_pb2.UpdateDataRequest(
    query='Update Seller set number_of_items_sold=100 where id=1',
)

# Create a request object
get_insert_request = customer_pb2.InsertDataRequest(
    query='INSERT INTO Seller VALUES (4, "seller4", 3, 2, 10)',
)

# Create a request object
get_delete_request = customer_pb2.DeleteDataRequest(
    query='Delete from Seller where id=1',
)


# Call the GetData rpc
get_data_response   = stub.GetData(get_data_request)
# Print the response
for row in get_data_response.rows:
    print(row)
print(MessageToJson(get_data_response))

insert_response     = stub.InsertData(get_insert_request)
print(insert_response.insert_id)
print(insert_response.error)

update_response     = stub.UpdateData(get_update_request)
print(update_response.affected_rows)
print(update_response.error)

delete_response     = stub.DeleteData(get_delete_request)
print(delete_response.affected_rows)
print(delete_response.error)

get_data_response   = stub.GetData(get_data_request)
# Print the response
for row in get_data_response.rows:
    print(row)

print(get_data_response.error)


import product_pb2
import product_pb2_grpc
import grpc

# Connect to the GRPC server
channel = grpc.insecure_channel('localhost:40080')
stub = product_pb2_grpc.ProductDatabaseServerStub(channel)

# Create a request object
get_data_request = product_pb2.GetRequest(
    query='select * from Item',
)

# Call the GetData rpc
get_data_response = stub.Get(get_data_request)

# Print the response
for row in get_data_response.rows:
    print(row)

print(get_data_response.error)
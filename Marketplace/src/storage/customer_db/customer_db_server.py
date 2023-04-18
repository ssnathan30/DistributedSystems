from concurrent import futures
import os
import pathlib
import grpc
import sqlite3
import customer_pb2
import customer_pb2_grpc
import sys
from replica import *

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(parent_dir)

class CustomerDatabaseServerServicer(customer_pb2_grpc.CustomerDatabaseServerServicer):

    def __init__(self) -> None:
        super().__init__()
        ## Start Replica
        e_replica_id = int(os.getenv("replica_id"))
        e_udp_port = int(os.getenv("replica_port"))
        e_host = os.getenv("customer_host")

        e_peers = list(os.getenv("peers").split(","))
        e_peers = [tuple(peer.split(":")) for peer in e_peers]
        peer_list = {int(peer[0]) :(peer[1],int(peer[2])) for peer in e_peers}

        print(peer_list)
        # Create a replica and start the instance
        self.replica_instance = replica(replica_id=e_replica_id,peers=peer_list,udp_port=e_udp_port,total_replicas=len(peer_list) + 1,host=e_host)
        self.replica_instance.start()

        db_ops = db_operations()


    def GetData(self, request, context):
        # Connect to the database
        data =  {
                    "type" : "request_message",
                    "message" : request.query,
                    "req_type" : "get"
                }
        request_id = self.replica_instance.send_broadcast_message(request=json.dumps(data))
        return self.replica_instance.processed_requests[request_id]

    def InsertData(self, request, context):
        data =  {
                    "type" : "request_message",
                    "message" : request.query,
                    "req_type" : "insert"
                }
        request_id = self.replica_instance.send_broadcast_message(request=json.dumps(data))
        return self.replica_instance.processed_requests[request_id]
        
    
    def UpdateData(self, request, context):
        data =  {
                    "type" : "request_message",
                    "message" : request.query,
                    "req_type" : "update"
                }
        request_id = self.replica_instance.send_broadcast_message(request=json.dumps(data))
        return self.replica_instance.processed_requests[request_id]

    def DeleteData(self, request, context):
        data =  {
                    "type" : "request_message",
                    "message" : request.query,
                    "req_type" : "delete"
                }
        request_id = self.replica_instance.send_broadcast_message(request=json.dumps(data))
        return self.replica_instance.processed_requests[request_id]

def serve():
    customer_host = os.getenv("customer_host","localhost")
    customer_port = os.getenv("customer_port",50080)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
    customer_pb2_grpc.add_CustomerDatabaseServerServicer_to_server(CustomerDatabaseServerServicer(), server)
    server.add_insecure_port(f'{customer_host}:{customer_port}')
    print(f'Listening on hostname: {customer_host}, port {customer_port}')

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

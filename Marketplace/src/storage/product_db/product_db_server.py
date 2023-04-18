from concurrent import futures
import os
import pathlib
import grpc
import sqlite3
import product_pb2
import product_pb2_grpc
import sys
from db_operations import *

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(parent_dir)

class ProductDatabaseServerServicer(product_pb2_grpc.ProductDatabaseServerServicer):

    def __init__(self) -> None:
        super().__init__()
        ## Start Raft
        e_udp_port = int(os.getenv("replica_port"))
        e_host = os.getenv("product_host","localhost")

        e_peers = list(os.getenv("peers").split(","))
        e_peers = [tuple(peer.split(":")) for peer in e_peers]
        peer_list = [f"{peer[1]}:{int(peer[2])}" for peer in e_peers]
        try:
            self.db_ops = db_operations(self_node=f"{e_host}:{e_udp_port}",peer_nodes=peer_list)
        except Exception as e:
            print(e)

    def Get(self, request, context):
        print(self.db_ops.getStatus())
        print("Request received")        
        return self.db_ops.Get(request)

    def Insert(self, request, context):
        return self.db_ops.Insert(request)    
    
    def Update(self, request, context):
        return self.db_ops.Update(request)

    def Delete(self, request, context):
        return self.db_ops.Delete(request)

def serve():
    product_host = os.getenv("product_host","localhost")
    product_port = os.getenv("product_port",50060)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductDatabaseServerServicer_to_server(ProductDatabaseServerServicer(), server)
    server.add_insecure_port(f'{product_host}:{product_port}')
    print(f'Listening on hostname: {product_host}, port {product_port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

# server.py

import logging
import selectors
import socket
import time
import json
import sys
import os
import pathlib
import traceback
from buyer_server_interface import server_buyer

#For importing packages from other folder
#file_dir = os.path.dirname(__file__)
#sys.path.append(os.path.abspath(os.path.join(file_dir, os.pardir)))

# path to src directory
src_dir = pathlib.Path(__file__).parent.parent.resolve()

sel = selectors.DefaultSelector()
clients = {}
client_session = {}

# Create and configure logger
logging.basicConfig(filename="{0}/logs/buyer_server_throughput.log".format(src_dir),
                    format='%(message)s',
                    )

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def accept(sock, mask):
    conn, addr = sock.accept()
    print('Accepted connection from', addr)
    conn.setblocking(False)
    
    # Create client session
    buyer_obj = server_buyer()
    clients[conn.fileno()] = conn
    client_session[conn] = buyer_obj
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print('Received data:', data.decode())
        input  = json.loads(data.decode())
        
        op_code = input["op_code"]
        action = input["action"]
        value = input["value"]

        buyer = client_session[conn]
        
        try :
            # Time the execution
            start_time = time.time()
            opcode = None
            result = None
            opcode, result = buyer.process(op_code, value, action)
            
            end_time = time.time()
            logger.info(f'{(end_time-start_time):.9f}')

            if opcode == -1:
                conn.sendall(bytes(result.encode()))
                print('Closing connection to', conn)
                sel.unregister(conn)
                del clients[conn.fileno()]
                del client_session[conn]
                conn.close()
            else:
                conn.sendall(bytes(result.encode()))
        except:
            print(str(traceback.format_exc()))
        """
        for fileno, client in clients.items():
            if fileno == conn.fileno():
                client.sendall(bytes(result.encode()))
        """
    else:
        print('Closing connection to', conn)
        sel.unregister(conn)
        del clients[conn.fileno()]
        del client_session[conn]
        conn.close()

def run_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8888))
        server.listen()
        server.setblocking(False)
        sel.register(server, selectors.EVENT_READ, accept)
        print("Server Available for Connection")
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except Exception as e:
        print("Closing server")
        print(str(traceback.format_exc()))
        server.close()
    finally:
        print("Closing server")
        server.close()

run_server()

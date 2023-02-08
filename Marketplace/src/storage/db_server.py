import selectors
import traceback
from db_utility import db
import logging
import socket
import json
import sys, os
import time
import pathlib

# Parent dir
parent_dir = pathlib.Path(__file__).parent.resolve()

# Intialize selector
sel = selectors.DefaultSelector()

# Create and configure logger
logging.basicConfig(filename="{0}/marketplace_db.log".format(parent_dir),format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Map to store the client-file_info
clients = {}

def accept(sock, mask):
    conn, addr = sock.accept()
    print('Accepted connection from', addr)
    conn.setblocking(False)
    
    # Create client session
    clients[conn.fileno()] = conn
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print('Received data:', data.decode())
        payload  = json.loads(data.decode())
        query = payload["query"]
        get_result = payload["get_result"]

        # Calculate the execution
        start_time = time.time()
        result = db.execute(query,get_result)
        result = json.dumps(result)
        end_time = time.time()

        # Log the execution time
        logger.info(f'{(end_time-start_time):.9f}')

        conn.sendall(bytes(result.encode()))
        print('Closing connection to', conn)
        sel.unregister(conn)
        del clients[conn.fileno()]
        conn.close()

def run_server(host="localhost",port=7777):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        server.setblocking(False)
        sel.register(server, selectors.EVENT_READ, accept)
        print("Database Server Available for Connection")
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except Exception as e:
        print("Closing server")
        print(str(traceback.format_exc()))
        logger.info(str(e))
        server.close()
    finally:
        print("Closing server")
        server.close()

run_server()
    
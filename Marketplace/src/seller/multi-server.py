# server.py

import selectors
import socket
from server_seller_functions import server_seller
import json
import sys, os

file_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(file_dir, os.pardir)))

from storage.init_db import marketplace_db

sel = selectors.DefaultSelector()
clients = {}
client_session = {}
db_obj = marketplace_db()
db_conn = db_obj.get_connection()

def accept(sock, mask):
    conn, addr = sock.accept()
    print('Accepted connection from', addr)
    conn.setblocking(False)
    
    # Create client session
    seller_obj = server_seller(db_conn)
    clients[conn.fileno()] = conn
    client_session[conn] = seller_obj
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print('Received data:', data.decode())
        input  = json.loads(data.decode())
        action = input["action"]
        values = input["values"]

        seller = client_session[conn]
        opcode, result = seller.process(action,values)

        if opcode == -1:
            conn.sendall(bytes(result.encode()))
            print('Closing connection to', conn)
            sel.unregister(conn)
            del clients[conn.fileno()]
            del client_session[conn]
            conn.close()
            
        else:
            conn.sendall(bytes(result.encode()))
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
        server.bind(('localhost', 6555))
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
        print(str(e))
        server.close()
    finally:
        print("Closing server")
        server.close()

run_server()

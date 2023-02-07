import selectors
import socket

sel = selectors.DefaultSelector()

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 6555))
    sel = selectors.DefaultSelector()
    sel.register(client, selectors.EVENT_READ, read)

    # Read data from command line and send to the server
    try:
        while True:
            message = input("Enter message: ")
            if message:
                client.sendall(message.encode())
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except Exception as e:
        print(str(e))
        print("Closing connection")
        sel.unregister(client)
        client.close()
    finally:
        client.close()

    
def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print('Received data:', data.decode())
    else:
        print('Closing connection to', conn)
        sel.unregister(conn)
        conn.close()

run_client()
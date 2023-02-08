import logging
import selectors
import socket
import time
import traceback
from jsonschema import validate
import json
import pathlib

# path to src directory
src_dir = pathlib.Path(__file__).parent.parent.resolve()

sel = selectors.DefaultSelector()
# Create and configure logger
logging.basicConfig(filename="{0}/logs/buyer_response_time.log".format(src_dir),
                    format='%(message)s',
                    )

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

schema = {
            "type": "object",
            "properties": {
                "op_code": {"type": "number"},
                "value": {},
                "action": {"type":"string"}
            },
            "required": ["op_code"]
        }

start_time = None
end_time = None

def run_client():
    global start_time
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8888))
    sel = selectors.DefaultSelector()
    sel.register(client, selectors.EVENT_READ, read)

    # Read data from command line and send to the server
    try:
        while True:
            message = input("Enter Input: ")
            if message:
                try :
                    json_data = json.loads(message.encode())
                    validate(instance=json_data, schema=schema)    
                except:
                    print("Invalid input")
                    continue
                start_time = time.time()
                client.sendall(message.encode())
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except Exception as e:
        print(str(traceback.format_exc()))
        print("Closing connection")
        sel.unregister(client)
        client.close()
    finally:
        client.close()

    
def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print('Received data:', data.decode())
        end_time = time.time()
        response_time = end_time - start_time
        logger.info(f'{(response_time):.9f}')
    else:
        print('Closing connection to', conn)
        sel.unregister(conn)
        conn.close()

run_client()
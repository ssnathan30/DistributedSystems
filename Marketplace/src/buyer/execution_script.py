import json
import pathlib

parent_dir = pathlib.Path(__file__).parent.resolve()

def read_input():
    with open("{0}/buyer_input.json".format(parent_dir)) as f:
        data = f.read()
    return data

def parse_data(data):
    data = json.loads(data)
    for action in data:
        if action["op_code"] == 8:
            for i in range(1000):
                print(json.dumps(action))
        else:
            print(json.dumps(action))

parse_data(read_input())
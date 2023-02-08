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
        print(json.dumps(action))


parse_data(read_input())
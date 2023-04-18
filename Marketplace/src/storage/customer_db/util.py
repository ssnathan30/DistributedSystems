import json
import jsonpickle
from flask import Response


def dict_to_bytes(map):
    return bytes(json.dumps(map), encoding='utf-8')


def bytes_to_json(payload):
    json_dump = None
    try:
        json_dump = json.loads(bytes.decode(payload))
    except:
        print("E: invalid json " + str(payload))
    return json_dump


def dict_to_json(object):
    return jsonpickle.dumps(object)


def json_to_dic(payload):
    json_dump = None
    try:
        json_dump = jsonpickle.loads(payload)
    except:
        print("E: invalid json " + str(payload))
    return json_dump


def get_response_object(response, status_code):
    response_pickled = None
    if response is not None:
        response_pickled = jsonpickle.dumps(response)
    return Response(response=response_pickled, status=status_code, mimetype="application/json")
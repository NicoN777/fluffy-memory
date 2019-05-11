import json


def from_file(filename):
    with open(filename, 'r') as fin:
        return json.dumps(fin)

def from_obj(obj):
    return json.dumps(obj)

def from_str(string):
    return json.loads(string)
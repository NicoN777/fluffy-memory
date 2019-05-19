import json

def from_file(filename):
    with open(filename, 'r') as fin:
        return json.dump(fin)

def from_obj(obj):
    return json.dumps(obj)

def to_str(string):
    return json.loads(string)

def to_obj(obj):
    return json.dump(obj)


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr
    return start
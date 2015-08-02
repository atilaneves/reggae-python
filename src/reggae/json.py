from json import JSONEncoder


class ReggaeEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'json_dict'):
            return o.json_dict()
        else:
            super().default(o)

from json import JSONEncoder


class ReggaeEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'jsonify'):
            return o.jsonify()
        else:
            super().default(o)

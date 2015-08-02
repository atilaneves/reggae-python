class Target(object):
    def __init__(self, outputs, cmd="", deps=[], implicits=[]):
        if not isinstance(outputs, list):
            outputs = [outputs]

        self.outputs = outputs
        self.cmd = cmd
        self.deps = deps
        self.implicits = implicits

    def jsonify(self):
        return {'outputs': self.outputs,
                'command': self.cmd,
                'dependencies': [t.jsonify() for t in self.deps],
                'implicits': [t.jsonify() for t in self.implicits]}


class Build(object):
    def __init__(self, *targets):
        self.targets = targets

    def jsonify(self):
        return [t.jsonify() for t in self.targets]

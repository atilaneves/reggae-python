class Target(object):
    def __init__(self, outputs, cmd="", deps=[], implicits=[]):
        if not isinstance(outputs, list):
            outputs = [outputs]

        self.outputs = outputs
        self.cmd = cmd
        self.deps = deps
        self.implicits = implicits

    def json_dict(self):
        return {'outputs': self.outputs,
                'command': self.cmd,
                'dependencies': [t.json_dict() for t in self.deps],
                'implicits': [t.json_dict() for t in self.implicits]}


class Build(object):
    def __init__(self, *targets):
        self.targets = targets

    def json_dict(self):
        return [t.json_dict() for t in self.targets]

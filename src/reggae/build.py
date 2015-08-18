class Target(object):
    def __init__(self, outputs, cmd="", deps=[], implicits=[]):
        outputs = _listify(outputs)
        deps = _listify(deps)
        implicits = _listify(implicits)

        self.outputs = outputs
        self.cmd = cmd
        self.deps = deps
        self.implicits = implicits

    def jsonify(self):
        return {'outputs': self.outputs,
                'command': self.cmd,
                'dependencies': [t.jsonify() for t in self.deps],
                'implicits': [t.jsonify() for t in self.implicits]}


def _listify(arg):
    return arg if isinstance(arg, list) else [arg]


class Build(object):
    def __init__(self, *targets):
        self.targets = targets

    def jsonify(self):
        return [t.jsonify() for t in self.targets]

def is_command(obj):
    return hasattr(obj, 'jsonify')


class ShellCommand(object):
    def __init__(self, cmd=''):
        self.cmd = cmd

    def jsonify(self):
        if self.cmd == '':
            return {}
        return {'type': 'shell', 'cmd': self.cmd}


class Target(object):
    def __init__(self, outputs, cmd="", deps=[], implicits=[]):
        outputs = _listify(outputs)
        deps = _listify(deps)
        implicits = _listify(implicits)

        self.outputs = outputs
        self.cmd = cmd if is_command(cmd) else ShellCommand(cmd)
        self.deps = deps
        self.implicits = implicits

    def jsonify(self):
        return {'outputs': self.outputs,
                'command': self.cmd.jsonify(),
                'dependencies': [t.jsonify() for t in self.deps],
                'implicits': [t.jsonify() for t in self.implicits]}


def _listify(arg):
    return arg if isinstance(arg, list) else [arg]


class Build(object):
    def __init__(self, *targets):
        self.targets = targets

    def jsonify(self):
        return [t.jsonify() for t in self.targets]

class Target(object):
    def __init__(self, outputs, cmd="", deps=[], implicits=[]):
        outputs = _listify(outputs)
        deps = _listify(deps)
        implicits = _listify(implicits)

        self.outputs = outputs
        self.cmd = cmd if _is_command(cmd) else ShellCommand(cmd)
        self.deps = FixedDependencies(deps)
        self.implicits = FixedDependencies(implicits)

    def jsonify(self):
        return {'outputs': self.outputs,
                'command': self.cmd.jsonify(),
                'dependencies': self.deps.jsonify(),
                'implicits': self.implicits.jsonify()}


def _listify(arg):
    return arg if isinstance(arg, list) else [arg]


def _is_command(obj):
    return hasattr(obj, 'jsonify')


class ShellCommand(object):
    def __init__(self, cmd=''):
        self.cmd = cmd

    def jsonify(self):
        if self.cmd == '':
            return {}
        return {'type': 'shell', 'cmd': self.cmd}


class FixedDependencies(object):
    def __init__(self, deps):
        self.deps = deps

    def jsonify(self):
        return {'type': 'fixed', 'targets': [t.jsonify() for t in self.deps]}


class Build(object):
    def __init__(self, *targets):
        self.targets = targets

    def jsonify(self):
        return [t.jsonify() for t in self.targets]

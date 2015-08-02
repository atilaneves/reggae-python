class Target(object):
    def __init__(self, outputs, cmd="", deps=[], implicits=[]):
        self.outputs = outputs
        self.cmd = cmd
        self.deps = deps
        self.implicits = implicits


class Build(object):
    def __init__(self, targets):
        self.targets = targets

from reggae.build import Target


def link(exe_name=None, dependencies=None, flags=''):
    assert exe_name is not None
    assert dependencies is not None
    return Target([exe_name], LinkCommand(flags), dependencies)


class LinkCommand(object):
    def __init__(self, flags=''):
        self.flags = flags

    def jsonify(self):
        return {'type': 'link', 'flags': self.flags}

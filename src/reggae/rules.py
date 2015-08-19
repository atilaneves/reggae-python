from reggae.build import Target, Dependencies


def objectFiles(src_dirs=[],
                exclude_dirs=[],
                src_files=[],
                exclude_files=[],
                flags='',
                includes=[],
                string_imports=[]):
    return DynamicDependencies('objectFiles',
                               src_dirs=src_dirs,
                               exclude_dirs=exclude_dirs,
                               src_files=src_files,
                               exclude_files=exclude_files,
                               flags=flags,
                               includes=includes,
                               string_imports=string_imports)


class DynamicDependencies(Dependencies):
    def __init__(self, func_name, **kwargs):
        self.func_name = func_name
        self.kwargs = kwargs

    def jsonify(self):
        base = {'type': 'dynamic', 'func': self.func_name}
        base.update(self.kwargs)
        return base


def link(exe_name=None, flags='', dependencies=None, implicits=[]):
    assert exe_name is not None
    assert dependencies is not None
    return Target([exe_name], LinkCommand(flags), dependencies, implicits)


class LinkCommand(object):
    def __init__(self, flags=''):
        self.flags = flags

    def jsonify(self):
        return {'type': 'link', 'flags': self.flags}

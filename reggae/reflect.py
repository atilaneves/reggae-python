from reggae.build import Build
from inspect import getmembers


def get_build(module):
    return [v for n, v in getmembers(module) if isinstance(v, Build)]

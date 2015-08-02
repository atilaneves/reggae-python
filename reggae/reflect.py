from reggae.build import Build
from inspect import getmembers


def get_build(module):
    return next(v for n, v in getmembers(module) if isinstance(v, Build))

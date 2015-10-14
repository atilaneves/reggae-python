from __future__ import (unicode_literals, division,
                        absolute_import, print_function)


from reggae.build import Build
from inspect import getmembers


def get_build(module):
    builds = [v for n, v in getmembers(module) if isinstance(v, Build)]
    assert len(builds) == 1
    return builds[0]

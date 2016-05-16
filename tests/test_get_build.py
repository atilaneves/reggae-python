from reggae.reflect import get_build
from reggae.build import Build, Target, DefaultOptions
from reggae.reggae_json_build import get_json
import json
import sys


build = Build(Target("foo", "dmd -offoo foo.d", [Target("foo.d")]))
def_opts = DefaultOptions(cCompiler='weirdcc', oldNinja=True)


def test_get_build():
    assert get_build(sys.modules[__name__]) == build


def test_get_json_for_module():
    assert json.loads(get_json(sys.modules[__name__])) == \
        [{'command': {'cmd': 'dmd -offoo foo.d', 'type': 'shell'},
          'dependencies': {'targets': [{'command': {},
                                        'dependencies': {'targets': [],
                                                         'type': 'fixed'},
                                        'implicits': {'targets': [],
                                                      'type': 'fixed'},
                                        'outputs': ['foo.d'],
                                        'type': 'fixed'}],
                           'type': 'fixed'},
          'implicits': {'targets': [], 'type': 'fixed'},
          'outputs': ['foo'],
          'type': 'fixed'},
         {'type': 'defaultOptions',
          'cCompiler': 'weirdcc',
         'oldNinja': True}]

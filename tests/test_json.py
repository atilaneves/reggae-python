from reggae.json import ReggaeEncoder
from reggae.build import Target, Build
from reggae.rules import link
from json import dumps, loads


def test_target():
    tgt = Target("foo.d")
    assert tgt.jsonify() == {'command': {},
                             'outputs': ['foo.d'],
                             'dependencies': [],
                             'implicits': []}

    json = dumps(tgt, cls=ReggaeEncoder)
    assert loads(json) == tgt.jsonify()


def test_build():
    build = Build(Target("foo", "dmd -offoo foo.d", [Target("foo.d")]))
    assert build.jsonify() == [{'command': {'type': 'shell',
                                            'cmd': 'dmd -offoo foo.d'},
                                'outputs': ['foo'],
                                'dependencies': [{'command': {},
                                                  'outputs': ['foo.d'],
                                                  'dependencies': [],
                                                  'implicits': []}],
                                'implicits': []}]

    json = dumps(build, cls=ReggaeEncoder)
    assert(loads(json) == build.jsonify())


def test_link():
    mainObj = Target('main.o',
                     'dmd -I$project/src -c $in -of$out',
                     Target('src/main.d'))
    mathsObj = Target('maths.o',
                      'dmd -c $in -of$out',
                      Target('src/maths.d'))
    app = link(exe_name='myapp',
               dependencies=[mainObj, mathsObj],
               flags='-L-M')
    bld = Build(app)

    assert bld.jsonify() == \
        [{'command': {'type': 'link', 'flags': '-L-M'},
          'outputs': ['myapp'],
          'dependencies':
          [{'command': {'type': 'shell', 'cmd':
                        'dmd -I$project/src -c $in -of$out'},
            'outputs': ['main.o'],
            'dependencies': [{'command': {}, 'outputs': ['src/main.d'],
                              'dependencies': [], 'implicits': []}],
            'implicits': []},
           {'command': {'type': 'shell', 'cmd':
                        'dmd -c $in -of$out'},
            'outputs': ['maths.o'],
            'dependencies': [{'command': {}, 'outputs': ['src/maths.d'],
                              'dependencies': [], 'implicits': []}],
            'implicits': []}],
          'implicits': []}]
    json = dumps(bld, cls=ReggaeEncoder)
    assert(loads(json) == bld.jsonify())

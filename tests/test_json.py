from reggae.json import ReggaeEncoder
from reggae.build import Target, Build
from json import dumps, loads


def test_target():
    tgt = Target("foo.d")
    assert tgt.jsonify() == {'command': '',
                             'outputs': ['foo.d'],
                             'dependencies': [],
                             'implicits': []}

    json = dumps(tgt, cls=ReggaeEncoder)
    assert loads(json) == tgt.jsonify()


def test_build():
    build = Build(Target("foo", "dmd -offoo foo.d", [Target("foo.d")]))
    assert build.jsonify() == [{'command': 'dmd -offoo foo.d',
                                'outputs': ['foo'],
                                'dependencies': [{'command': '',
                                                  'outputs': ['foo.d'],
                                                  'dependencies': [],
                                                  'implicits': []}],
                                'implicits': []}]

    json = dumps(build, cls=ReggaeEncoder)
    assert(loads(json) == build.jsonify())

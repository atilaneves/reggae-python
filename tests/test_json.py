from reggae.json import ReggaeEncoder
from reggae.build import Target
from json import dumps, loads


def test_target():
    tgt = Target("foo.d")
    assert(tgt.json_dict() == {'command': '',
                               'outputs': [],
                               'dependencies': [],
                               'implicits': []})

    json = dumps(tgt, cls=ReggaeEncoder)
    assert loads(json) == tgt.json_dict()

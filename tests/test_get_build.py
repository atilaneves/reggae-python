from reggae.reflect import get_build
from reggae.build import Build, Target


build = Build(Target("foo", "dmd -offoo foo.d", [Target("foo.d")]))


def test_get_build():
    import sys
    assert get_build(sys.modules[__name__]) == build

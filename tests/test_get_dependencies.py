from reggae.reflect import get_dependencies
import os
import foo  # noqa


def test_get_deps():
    my_dir = os.path.dirname(os.path.realpath(__file__))
    my_path = os.path.join(my_dir, __name__ + ".py")
    assert get_dependencies(my_path) == [os.path.join(my_dir, "foo.py")]

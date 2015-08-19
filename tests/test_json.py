from reggae.json import ReggaeEncoder
from reggae.build import Target, Build
from reggae.rules import link, objectFiles
from json import dumps, loads


def test_target():
    tgt = Target("foo.d")
    assert tgt.jsonify() == {"command": {},
                             "outputs": ["foo.d"],
                             "dependencies": {"type": "fixed", "targets": []},
                             "implicits": {"type": "fixed", "targets": []}}

    json = dumps(tgt, cls=ReggaeEncoder)
    assert loads(json) == tgt.jsonify()


def test_build():
    build = Build(Target("foo", "dmd -offoo foo.d", [Target("foo.d")]))
    assert build.jsonify() == [{"command": {"type": "shell",
                                            "cmd": "dmd -offoo foo.d"},
                                "outputs": ["foo"],
                                "dependencies": {"type": "fixed",
                                                 "targets":
                                                 [{"command": {},
                                                   "outputs": ["foo.d"],
                                                   "dependencies": {
                                                       "type": "fixed",
                                                       "targets": []},
                                                   "implicits": {
                                                       "type": "fixed",
                                                       "targets": []}}]},
                                "implicits": {"type": "fixed", "targets": []}}]

    json = dumps(build, cls=ReggaeEncoder)
    assert(loads(json) == build.jsonify())


def test_link_foo():
    mainObj = Target("main.o",
                     "dmd -I$project/src -c $in -of$out",
                     Target("src/main.d"))
    assert mainObj.jsonify() == \
        {"command": {"type": "shell",
                     "cmd": "dmd -I$project/src -c $in -of$out"},
         "outputs": ["main.o"],
         "dependencies": {"type": "fixed",
                          "targets": [
                              {"command": {}, "outputs": ["src/main.d"],
                               "dependencies": {
                                   "type": "fixed",
                                   "targets": []},
                               "implicits": {
                                   "type": "fixed",
                                   "targets": []}}]},
         "implicits": {
             "type": "fixed",
             "targets": []}}


def test_link_fixed():
    mainObj = Target("main.o",
                     "dmd -I$project/src -c $in -of$out",
                     Target("src/main.d"))
    mathsObj = Target("maths.o",
                      "dmd -c $in -of$out",
                      Target("src/maths.d"))
    app = link(exe_name="myapp",
               dependencies=[mainObj, mathsObj],
               flags="-L-M")
    bld = Build(app)

    assert bld.jsonify() == \
        [{"command": {"type": "link", "flags": "-L-M"},
          "outputs": ["myapp"],
          "dependencies": {
              "type": "fixed",
              "targets":
              [{"command": {"type": "shell",
                            "cmd": "dmd -I$project/src -c $in -of$out"},
                "outputs": ["main.o"],
                "dependencies": {"type": "fixed",
                                 "targets": [
                                     {"command": {}, "outputs": ["src/main.d"],
                                      "dependencies": {
                                          "type": "fixed",
                                          "targets": []},
                                      "implicits": {
                                          "type": "fixed",
                                          "targets": []}}]},
                "implicits": {
                    "type": "fixed",
                    "targets": []}},
               {"command": {"type": "shell", "cmd":
                            "dmd -c $in -of$out"},
                "outputs": ["maths.o"],
                "dependencies": {
                    "type": "fixed",
                    "targets": [
                        {"command": {}, "outputs": ["src/maths.d"],
                         "dependencies": {
                             "type": "fixed",
                             "targets": []},
                         "implicits": {
                             "type": "fixed",
                             "targets": []}}]},
                "implicits": {
                    "type": "fixed",
                    "targets": []}}]},
          "implicits": {
              "type": "fixed",
              "targets": []}}]
    json = dumps(bld, cls=ReggaeEncoder)
    assert(loads(json) == bld.jsonify())


def test_link_dynamic():
    objs = objectFiles(flags='-I$project/src', src_dirs=['src'])
    app = link(exe_name="myapp",
               dependencies=objs,
               flags="-L-M")
    bld = Build(app)

    assert bld.jsonify() == \
        [{"command": {"type": "link", "flags": "-L-M"},
          "outputs": ["myapp"],
          "dependencies": {
              "type": "dynamic",
              "func": "objectFiles",
              "src_dirs": ["src"],
              "exclude_dirs": [],
              "src_files": [],
              "exclude_files": [],
              "flags": "-I$project/src",
              "includes": [],
              "string_imports": []},
          "implicits": {
              "type": "fixed",
              "targets": []}}]
    json = dumps(bld, cls=ReggaeEncoder)
    assert(loads(json) == bld.jsonify())

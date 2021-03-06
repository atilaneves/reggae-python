from reggae.build import Target, Build, optional
from reggae.rules import *  # noqa
from json import dumps, loads
import pytest


def test_target():
    tgt = Target("foo.d")
    assert tgt.jsonify() == {"type": "fixed",
                             "command": {},
                             "outputs": ["foo.d"],
                             "dependencies": {"type": "fixed", "targets": []},
                             "implicits": {"type": "fixed", "targets": []}}

    json = dumps(tgt.jsonify())
    assert loads(json) == tgt.jsonify()


def test_optional_target():
    tgt = optional(Target("foo.d"))
    assert tgt.jsonify() == {"type": "fixed",
                             "command": {},
                             "outputs": ["foo.d"],
                             "dependencies": {"type": "fixed", "targets": []},
                             "implicits": {"type": "fixed", "targets": []},
                             "optional": True}

    json = dumps(tgt.jsonify())
    assert loads(json) == tgt.jsonify()


def test_build():
    build = Build(Target("foo", "dmd -offoo foo.d", [Target("foo.d")]))
    assert build.jsonify() == [{"type": "fixed",
                                "command": {"type": "shell",
                                            "cmd": "dmd -offoo foo.d"},
                                "outputs": ["foo"],
                                "dependencies": {"type": "fixed",
                                                 "targets":
                                                 [{"type": "fixed",
                                                   "command": {},
                                                   "outputs": ["foo.d"],
                                                   "dependencies": {
                                                       "type": "fixed",
                                                       "targets": []},
                                                   "implicits": {
                                                       "type": "fixed",
                                                       "targets": []}}]},
                                "implicits": {"type": "fixed", "targets": []}}]

    json = dumps(build.jsonify())
    assert(loads(json) == build.jsonify())


def test_link_foo():
    mainObj = Target("main.o",
                     "dmd -I$project/src -c $in -of$out",
                     Target("src/main.d"))
    assert mainObj.jsonify() == \
        {"type": "fixed",
         "command": {"type": "shell",
                     "cmd": "dmd -I$project/src -c $in -of$out"},
         "outputs": ["main.o"],
         "dependencies": {"type": "fixed",
                          "targets": [
                              {"type": "fixed",
                               "command": {}, "outputs": ["src/main.d"],
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
        [{"type": "fixed",
          "command": {"type": "link", "flags": "-L-M"},
          "outputs": ["myapp"],
          "dependencies": {
              "type": "fixed",
              "targets":
              [{"type": "fixed",
                "command": {"type": "shell",
                            "cmd": "dmd -I$project/src -c $in -of$out"},
                "outputs": ["main.o"],
                "dependencies": {"type": "fixed",
                                 "targets": [
                                     {"type": "fixed",
                                      "command": {}, "outputs": ["src/main.d"],
                                      "dependencies": {
                                          "type": "fixed",
                                          "targets": []},
                                      "implicits": {
                                          "type": "fixed",
                                          "targets": []}}]},
                "implicits": {
                    "type": "fixed",
                    "targets": []}},
               {"type": "fixed",
                "command": {"type": "shell", "cmd":
                            "dmd -c $in -of$out"},
                "outputs": ["maths.o"],
                "dependencies": {
                    "type": "fixed",
                    "targets": [
                        {"type": "fixed",
                         "command": {}, "outputs": ["src/maths.d"],
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
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_link_dynamic():
    objs = object_files(flags='-I$project/src', src_dirs=['src'])
    app = link(exe_name="myapp",
               dependencies=objs,
               flags="-L-M")
    bld = Build(app)

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "link", "flags": "-L-M"},
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
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_static_lib():
    lib = static_library('libstuff.a',
                         flags='-I$project/src',
                         src_dirs=['src'])
    app = link(exe_name="myapp",
               dependencies=lib,
               flags="-L-M")
    bld = Build(app)

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "link", "flags": "-L-M"},
          "outputs": ["myapp"],
          "dependencies": {
              "type": "dynamic",
              "func": "staticLibrary",
              "name": "libstuff.a",
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
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_scriptlike():
    app = scriptlike(src_name='src/main.d',
                     exe_name='leapp',
                     flags='-g',
                     includes=['src'])
    bld = Build(app)

    assert bld.jsonify() == \
        [{"type": "dynamic",
          "func": "scriptlike",
          "src_name": "src/main.d",
          "exe_name": "leapp",
          "link_with": {"type": "fixed", "targets": []},
          "flags": "-g",
          "includes": ["src"],
          "string_imports": []}]
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_build_two_targets():
    objs1 = object_files(flags='-I$project/src',
                         src_dirs=['src'])
    app1 = link(exe_name="app1",
                dependencies=objs1,
                flags="-L-M")
    objs2 = object_files(flags='-I$project/other',
                         src_dirs=['other', 'yetanother'])
    app2 = link(exe_name="app2",
                dependencies=objs2)

    bld = Build(app1, app2)

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "link", "flags": "-L-M"},
          "outputs": ["app1"],
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
              "targets": []}},
         {"type": "fixed",
          "command": {"type": "link", "flags": ""},
          "outputs": ["app2"],
          "dependencies": {
              "type": "dynamic",
              "func": "objectFiles",
              "src_dirs": ["other", "yetanother"],
              "exclude_dirs": [],
              "src_files": [],
              "exclude_files": [],
              "flags": "-I$project/other",
              "includes": [],
              "string_imports": []},
          "implicits": {
              "type": "fixed",
              "targets": []}}]
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_object_files_error():
    with pytest.raises(TypeError):
        object_files('')

    with pytest.raises(TypeError):
        object_files([], '')

    with pytest.raises(TypeError):
        object_files([], [], '')

    with pytest.raises(TypeError):
        object_files([], [], [], '')

    with pytest.raises(TypeError):
        object_files([], [], [], [], [])

    with pytest.raises(TypeError):
        object_files([], [], [], [], '', '')

    with pytest.raises(TypeError):
        object_files([], [], [], [], '', [], '')


def test_target_concat():
    mainObj = Target("main.o",
                     "dmd -I$project/src -c $in -of$out",
                     Target("src/main.d"))
    mathsObj = Target("maths.o",
                      "dmd -c $in -of$out",
                      Target("src/maths.d"))
    app = link(exe_name="myapp",
               dependencies=target_concat(mainObj, mathsObj),
               flags="-L-M")
    bld = Build(app)

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "link", "flags": "-L-M"},
          "outputs": ["myapp"],
          "dependencies": {
              "type": "dynamic",
              "func": "targetConcat",
              "dependencies": [
                  {"type": "fixed",
                   "command": {"type": "shell",
                               "cmd": "dmd -I$project/src -c $in -of$out"},
                   "outputs": ["main.o"],
                   "dependencies": {"type": "fixed",
                                    "targets": [
                                        {"type": "fixed",
                                         "command": {},
                                         "outputs": ["src/main.d"],
                                         "dependencies": {
                                             "type": "fixed",
                                             "targets": []},
                                         "implicits": {
                                             "type": "fixed",
                                             "targets": []}}]},
                   "implicits": {
                       "type": "fixed",
                       "targets": []}},
                  {"type": "fixed",
                   "command": {"type": "shell", "cmd":
                               "dmd -c $in -of$out"},
                   "outputs": ["maths.o"],
                   "dependencies": {
                       "type": "fixed",
                       "targets": [
                           {"type": "fixed",
                            "command": {}, "outputs": ["src/maths.d"],
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

    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_link_dynamic_concat():
    main_obj = Target("main.o",
                      "dmd -I$project/src -c $in -of$out",
                      Target("src/main.d"))
    objs = object_files(flags='-I$project/src', src_dirs=['src'])
    app = link(exe_name="myapp",
               dependencies=[objs, main_obj],
               flags="-L-M")
    bld = Build(app)

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "link", "flags": "-L-M"},
          "outputs": ["myapp"],
          "implicits": {"type": "fixed", "targets": []},
          "dependencies": {
              "type": "dynamic",
              "func": "targetConcat",
              "dependencies": [
                  {"type": "dynamic",
                   "func": "objectFiles",
                   "src_dirs": ["src"],
                   "exclude_dirs": [],
                   "src_files": [],
                   "exclude_files": [],
                   "flags": "-I$project/src",
                   "includes": [],
                   "string_imports": []},
                  {"type": "fixed",
                   "command": {"type": "shell",
                               "cmd": "dmd -I$project/src -c $in -of$out"},
                   "outputs": ["main.o"],
                   "dependencies": {"type": "fixed",
                                    "targets": [
                                        {"type": "fixed",
                                         "command": {},
                                         "outputs": ["src/main.d"],
                                         "dependencies": {
                                             "type": "fixed",
                                             "targets": []},
                                         "implicits": {
                                             "type": "fixed",
                                             "targets": []}}]},
                   "implicits": {
                       "type": "fixed",
                       "targets": []}},
              ]

          }}]
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_src_files():
    objs = object_files(flags='-g -pg',
                        src_dirs=['src'],
                        src_files=['main.cpp'])
    app = link(exe_name='myapp', dependencies=objs)
    bld = Build(app)

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "link", "flags": ""},
          "outputs": ["myapp"],
          "dependencies": {
              "type": "dynamic",
              "func": "objectFiles",
              "src_dirs": ["src"],
              "exclude_dirs": [],
              "src_files": ['main.cpp'],
              "exclude_files": [],
              "flags": "-g -pg",
              "includes": [],
              "string_imports": []},
          "implicits": {
              "type": "fixed",
              "targets": []}}]
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_list_with_one_item():
    objs = object_files(src_dirs=['src'])
    app = link(exe_name='myapp', dependencies=[objs])
    bld = Build(app)

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "link", "flags": ""},
          "outputs": ["myapp"],
          "dependencies": {
              "type": "dynamic",
              "func": "objectFiles",
              "src_dirs": ["src"],
              "exclude_dirs": [],
              "src_files": [],
              "exclude_files": [],
              "flags": "",
              "includes": [],
              "string_imports": []},
          "implicits": {
              "type": "fixed",
              "targets": []}}]
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_mix_dynamic_and_static():
    objs = object_files(flags='-I$project/src', src_dirs=['src'])
    app = Target('app',
                 'cmd',
                 [objs, Target('libfoo.a')])
    bld = Build(app)

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "shell", "cmd": "cmd"},
          "outputs": ["app"],
          "implicits": {"type": "fixed", "targets": []},
          "dependencies": {
              "type": "dynamic",
              "func": "targetConcat",
              "dependencies": [
                  {"type": "dynamic",
                   "func": "objectFiles",
                   "src_dirs": ["src"],
                   "exclude_dirs": [],
                   "src_files": [],
                   "exclude_files": [],
                   "flags": "-I$project/src",
                   "includes": [],
                   "string_imports": []},
                  {"type": "fixed",
                   "command": {},
                   "outputs": ["libfoo.a"],
                   "dependencies": {"type": "fixed",
                                    "targets": []},
                   "implicits": {
                       "type": "fixed",
                       "targets": []}},
              ]

          }}]
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())


def test_executable():
    bld = Build(executable(name="myapp",
                           compiler_flags='-I$project/src',
                           src_dirs=['src'],
                           linker_flags='-L-M'))

    assert bld.jsonify() == \
        [{"type": "fixed",
          "command": {"type": "link", "flags": "-L-M"},
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
    json = dumps(bld.jsonify())
    assert(loads(json) == bld.jsonify())

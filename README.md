Reggae-Python
=============
[![Build Status](https://travis-ci.org/atilaneves/reggae-python.png?branch=master)](https://travis-ci.org/atilaneves/reggae-python)

A Python interface / front-end to [the reggae meta-build system](https://github.org/atilaneves/reggae).


Installation
------------

    pip install reggae


Usage
------------

This packge makes available a few classes and functions that allow the user to write
build descriptions in Python. It is essentially the same API as the D version but in
Python syntax. A simple C build could be written like this:

    from reggae import *
    main_obj = Target('main.o', 'gcc -I$project/src -c $in -o $out', Target('src/main.c'))
    maths_obj = Target('maths.o', 'gcc -c $in -o $out', Target('src/maths.c'))
    app = Target('myapp', 'gcc -o $out $in', [main_obj, maths_obj])
    bld = Build(app)

This should be contained in a file named `reggaefile.py` in the project's root directory.
Running the `reggae` D binary on that directory will produce a build with the requested backend
(ninja, make, etc.)

Most builds will probably not resort to low-level primitives as above. A better way to describe
that C build would be:

    from reggae import *
    objs =  object_files(flags='-I$project/src', src_dirs=['src'])
    app = link(exe_name='app', dependencies=objs)
    bld = Build(app)


Please consult the [reggae documentation](https://github.com/atilaneves/reggae/tree/master/doc/index.md)
for more details.

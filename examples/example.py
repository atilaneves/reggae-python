from reggae.build import Target, Build


target = Target("foo", "dmd -offoo foo.d", [Target("foo.d")])
build = Build([target])

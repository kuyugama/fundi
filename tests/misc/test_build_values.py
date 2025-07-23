from fundi import scan


def test_default():
    def dep(arg: int, arg2: str): ...

    info = scan(dep)

    values = info.build_values(arg=1, arg2="1")

    assert values == {"arg": 1, "arg2": "1"}


def test_posonly():
    def dep(arg: int, /, arg2: str): ...

    info = scan(dep)

    values = info.build_values(arg=1, arg2="1")

    assert values == {"arg": 1, "arg2": "1"}


def test_kwonly():
    def dep(arg: int, *, arg2: str): ...

    info = scan(dep)

    values = info.build_values(1, "1")

    assert values == {"arg": 1, "arg2": "1"}


def test_varargs():
    def dep(*args: int | str): ...

    info = scan(dep)

    values = info.build_values(1, "1")

    assert values == {"args": (1, "1")}


def test_varkw():
    def dep(**args: int | str): ...

    info = scan(dep)

    values = info.build_values(arg=1, arg2="1")

    assert values == {"args": {"arg": 1, "arg2": "1"}}

from fundi import scan


def test_default():
    def dep(arg: int, arg2: str): ...

    info = scan(dep)

    args, kwargs = info.build_arguments({"arg": 1, "arg2": "1"})

    assert args == (1, "1")
    assert kwargs == {}


def test_posonly():
    def dep(arg: int, /, arg2: str): ...

    info = scan(dep)

    args, kwargs = info.build_arguments({"arg": 1, "arg2": "1"})

    assert args == (1, "1")
    assert kwargs == {}


def test_kwonly():
    def dep(arg: int, *, arg2: str): ...

    info = scan(dep)

    args, kwargs = info.build_arguments({"arg": 1, "arg2": "1"})

    assert args == (1,)
    assert kwargs == {"arg2": "1"}


def test_varargs():
    def dep(*args: int | str): ...

    info = scan(dep)

    args, kwargs = info.build_arguments({"args": (1, "1")})

    assert args == (1, "1")
    assert kwargs == {}


def test_varkw():
    def dep(**args: int | str): ...

    info = scan(dep)

    args, kwargs = info.build_arguments({"args": {"arg": 1, "arg2": "1"}})

    assert args == ()
    assert kwargs == {"arg": 1, "arg2": "1"}

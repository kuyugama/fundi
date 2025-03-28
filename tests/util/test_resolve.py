from fundi import resolve, from_, scan


def test_resolve_sync():
    def dep():
        pass

    def func(arg: int, arg1: str, arg2: None = from_(dep)):
        pass

    for result in resolve({"arg": 1, "arg1": "value"}, scan(func), {}):
        if not result.resolved:
            assert result.dependency is not None
            assert result.dependency.call is dep

        if result.resolved:
            assert result.parameter_name in ("arg", "arg1")

            if result.parameter_name == "arg1":
                assert result.value == "value"

            if result.parameter_name == "arg":
                assert result.value == 1


def test_resolve_async():
    async def dep():
        pass

    async def func(arg: int, arg1: str, arg2: None = from_(dep)):
        pass

    for result in resolve({"arg": 1, "arg1": "value"}, scan(func), {}):
        if not result.resolved:
            assert result.dependency is not None
            assert result.dependency.call is dep

        if result.resolved:
            assert result.parameter_name in ("arg", "arg1")

            if result.parameter_name == "arg1":
                assert result.value == "value"

            if result.parameter_name == "arg":
                assert result.value == 1

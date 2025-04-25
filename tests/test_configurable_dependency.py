import warnings

from fundi import configurable_dependency, MutableConfigurationWarning


def test_configurable_dependency_caching():
    @configurable_dependency
    def factory(require_admin: bool = False):
        def checker(): ...

        return checker


    assert factory() is factory()
    assert factory(require_admin=True) is not factory()
    assert factory(require_admin=False) is not factory()
    assert factory(require_admin=True) is factory(require_admin=True)
    assert factory(require_admin=False) is factory(require_admin=False)


def test_configurable_dependency_mutable_argument():
    @configurable_dependency
    def factory(permissions: list[str]):
        def checker(): ...

        return checker

    assert factory(("permissions",)) is factory(("permissions",))

    with warnings.catch_warnings(record=True) as got_warnings:
        assert factory(["permissions"]) is not factory(["permissions"])

    assert got_warnings
    assert got_warnings[0].category is MutableConfigurationWarning


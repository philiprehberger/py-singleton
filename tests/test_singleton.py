"""Tests for singleton and multiton decorators."""

from philiprehberger_singleton import multiton, singleton


class TestSingleton:
    """Tests for the @singleton decorator."""

    def test_singleton_returns_same_instance(self) -> None:
        @singleton
        class MyService:
            pass

        a = MyService()
        b = MyService()
        assert a is b

    def test_singleton_with_args(self) -> None:
        @singleton
        class Config:
            def __init__(self, value: int) -> None:
                self.value = value

        first = Config(42)
        second = Config(99)
        assert first is second
        assert first.value == 42

    def test_singleton_reset(self) -> None:
        @singleton
        class Counter:
            def __init__(self, start: int = 0) -> None:
                self.start = start

        a = Counter(1)
        assert a.start == 1

        Counter.reset()

        b = Counter(2)
        assert b.start == 2
        assert a is not b


class TestMultiton:
    """Tests for the @multiton decorator."""

    def test_multiton_same_key_returns_same_instance(self) -> None:
        @multiton(key="name")
        class Connection:
            def __init__(self, name: str) -> None:
                self.name = name

        a = Connection("db")
        b = Connection("db")
        assert a is b

    def test_multiton_different_keys_return_different_instances(self) -> None:
        @multiton(key="name")
        class Connection:
            def __init__(self, name: str) -> None:
                self.name = name

        a = Connection("db")
        b = Connection("cache")
        assert a is not b
        assert a.name == "db"
        assert b.name == "cache"


class TestClearOnExit:
    def test_resets_on_exit(self) -> None:
        from philiprehberger_singleton import clear_on_exit, singleton

        @clear_on_exit
        @singleton
        class Service:
            def __init__(self) -> None:
                self.started = True

        s1 = Service()
        assert s1.started is True

        with Service() as s:
            assert s is s1

        # After context exit, singleton should be reset
        s2 = Service()
        assert s2 is not s1

    def test_works_as_context_manager(self) -> None:
        from philiprehberger_singleton import clear_on_exit, singleton

        @clear_on_exit
        @singleton
        class Cache:
            pass

        with Cache() as c:
            assert c is not None

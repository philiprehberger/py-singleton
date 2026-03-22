# philiprehberger-singleton

[![PyPI](https://img.shields.io/pypi/v/philiprehberger-singleton)](https://pypi.org/project/philiprehberger-singleton/)
[![Python](https://img.shields.io/pypi/pyversions/philiprehberger-singleton)](https://pypi.org/project/philiprehberger-singleton/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Thread-safe singleton and multiton pattern decorators.

## Requirements

- Python >= 3.10

## Installation

```bash
pip install philiprehberger-singleton
```

## Usage

### Singleton

The `@singleton` decorator ensures only one instance of a class exists:

```python
from philiprehberger_singleton import singleton

@singleton
class Database:
    def __init__(self, url: str) -> None:
        self.url = url

db1 = Database("postgres://localhost/mydb")
db2 = Database("postgres://localhost/other")

assert db1 is db2  # same instance
assert db1.url == "postgres://localhost/mydb"
```

#### Reset

Use `reset()` to discard the cached instance (useful in tests):

```python
Database.reset()
db3 = Database("postgres://localhost/new")
assert db3.url == "postgres://localhost/new"
```

### Multiton

The `@multiton(key=...)` decorator maintains one instance per unique key value:

```python
from philiprehberger_singleton import multiton

@multiton(key="name")
class Connection:
    def __init__(self, name: str, timeout: int = 30) -> None:
        self.name = name
        self.timeout = timeout

cache = Connection("cache", timeout=10)
db = Connection("db", timeout=60)
cache2 = Connection("cache")

assert cache is cache2       # same key -> same instance
assert cache is not db        # different key -> different instance
```

#### Reset

Use `reset()` to discard all cached instances:

```python
Connection.reset()
```

## API

| Name | Type | Description |
|------|------|-------------|
| `singleton` | decorator | Makes a class a thread-safe singleton. Returns the same instance on every call. |
| `multiton(key)` | decorator factory | Makes a class a thread-safe multiton. One instance per unique value of the named parameter. |
| `cls.reset()` | class method | Discards cached instance(s), added by both decorators. |

## Development

```bash
pip install -e .
pytest
```

## License

[MIT](LICENSE)

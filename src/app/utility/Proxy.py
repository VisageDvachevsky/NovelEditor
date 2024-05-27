from typing import TypeVar, Generic, Callable, Any

T = TypeVar("T")


class Proxy(Generic[T], Any):
    def __init__(self, getter: Callable[[], T]):
        self._getter = getter

    def __eq__(self, other: Any) -> bool:
        return self._getter() == other

    def __getattr__(self, name):
        return object.__getattribute__(self._getter(), name)

    def __getitem__(self, index):
        return self._getter()[index]

    def __setattr__(self, name, value):
        if name == "_getter":
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self._getter(), name, value)

    def __iter__(self):
        return iter(self._getter())

    def __len__(self):
        return len(self._getter())

    def __add__(self, other):
        return self._getter() + other

    def __radd__(self, other):
        return other + self._getter()

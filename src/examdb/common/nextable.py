#!/usr/bin/env python3

from typing import Iterator


class Nextable:
    def __init__(self, iter: Iterator[str]):
        self._iter: Iterator[str] = iter
        self._next: str | None = None

    def next(self) -> str | None:
        if self._next is not None:
            result = self._next
            self._next = None
            return result

        return self._get_next()

    def peek(self) -> str | None:
        if self.has_next():
            return self._next

        return None

    def has_next(self) -> bool:
        if self._next is not None:
            return True

        self._next = self._get_next()

        return self._next is not None

    def _get_next(self) -> str | None:
        try:
            return self._iter.__next__()
        except StopIteration:
            return None

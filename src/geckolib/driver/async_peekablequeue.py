"""A peekable async queue"""

import asyncio
from typing import Any


class AsyncPeekableQueue:
    """A peekable async queue which allows queue filtering in consumers"""

    def __init__(self):
        self._queue = asyncio.Queue()
        self._wait_future = None
        self._marked = False

    def put_nowait(self, item):
        self._queue.put_nowait(item)
        if self._wait_future is not None:
            self._wait_future.set_result(True)
            self._wait_future = None

    @property
    def head(self) -> Any:
        """The head property will reveal the item at the head of the queue
        if there is one, or None if there isn't one"""
        if self._queue.qsize() > 0:
            return self._queue._queue[0]  # type: ignore
        return None

    async def data_available(self):
        if self._queue.qsize() < 1:
            if self._wait_future is None:
                self._wait_future = self._queue._get_loop().create_future()
            return await self._wait_future
        else:
            return True

    @property
    def is_marked(self) -> bool:
        return self._marked

    def pop(self) -> Any:
        self._queue.get_nowait()
        self._marked = False

    def mark(self) -> None:
        self._marked = True

"""Application-lifetime, in-memory spare proxies for Profile creation."""
from __future__ import annotations

from collections import deque
from threading import Lock
from typing import Iterable

from .bulk_input import MAX_PROXY_CANDIDATES
from .core import ToolError
from .swarmote_desktop import ProxyConfig


def proxy_key(proxy: ProxyConfig) -> tuple[str, str, int, str, str]:
    return (proxy.kind, proxy.host.casefold(), proxy.port,
            proxy.username, proxy.password)


class ProxyReserve:
    """FIFO pool. A consumed proxy cannot be silently re-added this session."""

    def __init__(self, batch_id: str) -> None:
        self._batch_id = batch_id
        self._available: deque[ProxyConfig] = deque()
        self._known: set[tuple[str, str, int, str, str]] = set()
        self._lock = Lock()

    def activate(self, batch_id: str) -> None:
        """Keep unused proxies while invalidating workers from the old batch."""
        with self._lock:
            self._batch_id = batch_id

    def snapshot(self) -> tuple[ProxyConfig, ...]:
        with self._lock:
            return tuple(self._available)

    def contains(self, proxy: ProxyConfig) -> bool:
        with self._lock:
            return proxy_key(proxy) in self._known

    def __len__(self) -> int:
        with self._lock:
            return len(self._available)

    def add(self, proxies: Iterable[ProxyConfig], *,
            forbidden: Iterable[ProxyConfig] = ()) -> int:
        """Append unique spares atomically; leave the pool untouched on overflow."""
        with self._lock:
            seen = self._known | {proxy_key(item) for item in forbidden}
            added = []
            for proxy in proxies:
                key = proxy_key(proxy)
                if key not in seen:
                    added.append(proxy)
                    seen.add(key)
            if len(self._available) + len(added) > MAX_PROXY_CANDIDATES:
                raise ToolError("Proxy dự phòng vượt 100 mục; danh sách cũ được giữ nguyên")
            self._available.extend(added)
            self._known.update(proxy_key(proxy) for proxy in added)
            return len(added)

    def take(self, batch_id: str, *,
             exclude: ProxyConfig | None = None) -> tuple[ProxyConfig, int] | None:
        """Give the first usable spare without consuming the current proxy."""
        with self._lock:
            if batch_id != self._batch_id or not self._available:
                return None
            excluded_key = proxy_key(exclude) if exclude is not None else None
            for index, proxy in enumerate(self._available):
                if proxy_key(proxy) != excluded_key:
                    del self._available[index]
                    return proxy, len(self._available)
            return None

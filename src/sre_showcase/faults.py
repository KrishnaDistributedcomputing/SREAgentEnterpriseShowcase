"""Bounded in-memory fault injection for non-production demonstrations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from threading import Lock

from .catalog import FaultMode

MAX_FAULT_SECONDS = 900


@dataclass(frozen=True, slots=True)
class FaultSnapshot:
    """Current fault state returned to API callers."""

    mode: FaultMode
    expires_at: datetime | None


class FaultController:
    """Thread-safe controller that automatically expires injected faults."""

    def __init__(self) -> None:
        self._mode: FaultMode = "none"
        self._expires_at: datetime | None = None
        self._lock = Lock()

    def activate(self, mode: FaultMode, duration_seconds: int) -> FaultSnapshot:
        """Activate a fault for a bounded duration."""
        if mode == "none":
            return self.clear()
        if not 1 <= duration_seconds <= MAX_FAULT_SECONDS:
            raise ValueError(f"duration_seconds must be between 1 and {MAX_FAULT_SECONDS}")
        with self._lock:
            self._mode = mode
            self._expires_at = datetime.now(UTC) + timedelta(seconds=duration_seconds)
            return FaultSnapshot(self._mode, self._expires_at)

    def current(self) -> FaultSnapshot:
        """Return the active fault, clearing it after expiry."""
        with self._lock:
            if self._expires_at is not None and datetime.now(UTC) >= self._expires_at:
                self._mode = "none"
                self._expires_at = None
            return FaultSnapshot(self._mode, self._expires_at)

    def clear(self) -> FaultSnapshot:
        """Disable any active fault."""
        with self._lock:
            self._mode = "none"
            self._expires_at = None
            return FaultSnapshot(self._mode, self._expires_at)


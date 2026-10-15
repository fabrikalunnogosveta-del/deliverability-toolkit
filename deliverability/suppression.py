"""Suppression list — hard bounce / complaint / opt-out → never send again."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Set

_HARD_REASONS = {"hard_bounce", "complaint", "opt_out", "unsubscribe", "trap"}


@dataclass
class SuppressionList:
    _entries: Dict[str, str] = field(default_factory=dict, init=False, repr=False)

    def suppress(self, email: str, reason: str = "hard_bounce") -> None:
        key = (email or "").strip().lower()
        if not key:
            raise ValueError("email required")
        self._entries[key] = reason

    def is_suppressed(self, email: str) -> bool:
        key = (email or "").strip().lower()
        return key in self._entries

    def reason(self, email: str) -> Optional[str]:
        return self._entries.get((email or "").strip().lower())

    def should_send(self, email: str) -> bool:
        return not self.is_suppressed(email)

    def __len__(self) -> int:
        return len(self._entries)

    def emails(self) -> Set[str]:
        return set(self._entries)

    @staticmethod
    def is_hard_reason(reason: str) -> bool:
        return (reason or "").lower() in _HARD_REASONS

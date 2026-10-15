"""Send report — what happened to each recipient."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class SendEvent:
    email: str
    status: str  # sent | delivered | bounced_hard | bounced_soft | complaint | opt_out
    domain: str = ""


@dataclass
class SendReport:
    events: List[SendEvent] = field(default_factory=list)

    def add(self, event: SendEvent) -> None:
        self.events.append(event)

    def count(self, status: str) -> int:
        return sum(1 for e in self.events if e.status == status)

    @property
    def delivered_rate(self) -> float:
        if not self.events:
            return 0.0
        return self.count("delivered") / len(self.events)

    def summary(self) -> dict:
        return {
            "total": len(self.events),
            "delivered": self.count("delivered"),
            "bounced_hard": self.count("bounced_hard"),
            "complaint": self.count("complaint"),
            "opt_out": self.count("opt_out"),
            "delivered_rate": round(self.delivered_rate, 4),
        }

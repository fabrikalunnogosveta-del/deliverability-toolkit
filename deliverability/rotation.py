"""IP/domain rotation under daily budgets and cooldowns."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SenderStats:
    domain: str
    sent_today: int = 0
    daily_cap: int = 100
    cooldown_until_day: int = 0
    healthy: bool = True


@dataclass
class RotationPool:
    """Round-robin with budget + health. Fail-closed if nothing available."""

    domains: List[str]
    daily_cap: int = 100
    _stats: Dict[str, SenderStats] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        for d in self.domains:
            self._stats[d] = SenderStats(domain=d, daily_cap=self.daily_cap)

    def next_domain(self, *, day: int = 0) -> Optional[str]:
        for domain in self.domains:
            st = self._stats[domain]
            if not st.healthy:
                continue
            if day < st.cooldown_until_day:
                continue
            if st.sent_today >= st.daily_cap:
                continue
            st.sent_today += 1
            return domain
        return None

    def mark_unhealthy(self, domain: str, cooldown_days: int = 1, *, day: int = 0) -> None:
        st = self._stats[domain]
        st.healthy = False
        st.cooldown_until_day = day + cooldown_days

    def mark_healthy(self, domain: str) -> None:
        self._stats[domain].healthy = True

    def reset_daily(self) -> None:
        for st in self._stats.values():
            st.sent_today = 0

    def stats(self) -> Dict[str, SenderStats]:
        return dict(self._stats)

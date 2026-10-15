"""Domain warm-up schedule — ramp volume, never blast from day one."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WarmupSchedule:
    """Exponential-ish ramp with a hard cap."""

    start: int = 20
    growth: float = 1.5
    cap: int = 2000
    min_volume: int = 1

    def volume_for_day(self, day: int) -> int:
        if day < 1:
            raise ValueError("day must be >= 1")
        raw = self.start * (self.growth ** (day - 1))
        vol = int(raw)
        return max(self.min_volume, min(self.cap, vol))

    def plan(self, days: int) -> list[int]:
        return [self.volume_for_day(d) for d in range(1, days + 1)]

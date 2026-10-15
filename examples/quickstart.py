"""Quickstart — warm-up, rotation, suppression (no mail is sent)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from deliverability import (
    RotationPool,
    SendEvent,
    SendReport,
    SuppressionList,
    WarmupSchedule,
    check_can_spam,
)


def main() -> None:
    warmup = WarmupSchedule(start=20, growth=1.5, cap=2000)
    print("warmup day1/day10:", warmup.volume_for_day(1), warmup.volume_for_day(10))

    pool = RotationPool(domains=["mail1.example", "mail2.example"], daily_cap=5)
    print("next domain:", pool.next_domain())

    sup = SuppressionList()
    sup.suppress("bad@example.com", reason="hard_bounce")
    print("should_send bad:", sup.should_send("bad@example.com"))

    issues = check_can_spam(
        has_physical_address=True, has_opt_out=True, opt_out_works=True, honest_subject=True
    )
    print("can_spam issues:", issues)

    report = SendReport()
    report.add(SendEvent("a@b.c", "delivered", "mail1.example"))
    report.add(SendEvent("x@y.z", "bounced_hard", "mail1.example"))
    print("report:", report.summary())


if __name__ == "__main__":
    main()

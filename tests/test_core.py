"""Behavioral contracts — warm-up, rotation, suppression, compliance, report."""

from deliverability import (
    RotationPool,
    SendEvent,
    SendReport,
    SuppressionList,
    WarmupSchedule,
    check_can_spam,
    check_gdpr,
)
import pytest


def test_warmup_monotonic_and_cap():
    w = WarmupSchedule(start=20, growth=1.5, cap=500)
    plan = w.plan(20)
    assert plan[0] == 20
    assert all(plan[i] <= plan[i + 1] for i in range(len(plan) - 1))
    assert max(plan) <= 500


def test_warmup_day_one_no_blast():
    w = WarmupSchedule(start=20, growth=2.0, cap=10000)
    assert w.volume_for_day(1) == 20


def test_warmup_rejects_day_zero():
    with pytest.raises(ValueError):
        WarmupSchedule().volume_for_day(0)


def test_rotation_respects_budget():
    pool = RotationPool(domains=["a.com", "b.com"], daily_cap=2)
    picks = [pool.next_domain() for _ in range(4)]
    assert all(p is not None for p in picks)
    assert pool.next_domain() is None  # budget exhausted


def test_rotation_skips_unhealthy():
    pool = RotationPool(domains=["a.com", "b.com"], daily_cap=10)
    pool.mark_unhealthy("a.com", cooldown_days=3, day=0)
    assert pool.next_domain(day=0) == "b.com"
    assert pool.next_domain(day=1) == "b.com"
    pool.mark_healthy("a.com")
    assert pool.next_domain(day=2) in {"a.com", "b.com"}


def test_suppression_blocks_send():
    sup = SuppressionList()
    assert sup.should_send("user@example.com")
    sup.suppress("Bad@Example.com", reason="hard_bounce")
    assert not sup.should_send("bad@example.com")
    assert sup.reason("BAD@EXAMPLE.COM") == "hard_bounce"
    assert len(sup) == 1


def test_suppression_idempotent():
    sup = SuppressionList()
    sup.suppress("x@y.z", reason="complaint")
    sup.suppress("x@y.z", reason="complaint")
    assert len(sup) == 1


def test_suppression_hard_reasons():
    assert SuppressionList.is_hard_reason("hard_bounce")
    assert SuppressionList.is_hard_reason("opt_out")
    assert not SuppressionList.is_hard_reason("soft_bounce")


def test_can_spam_flags():
    issues = check_can_spam(
        has_physical_address=False,
        has_opt_out=False,
        opt_out_works=False,
        honest_subject=False,
    )
    codes = {i.code for i in issues}
    assert "CANSPAM_ADDR" in codes
    assert "CANSPAM_OPTOUT" in codes
    assert "CANSPAM_SUBJECT" in codes


def test_can_spam_clean():
    assert check_can_spam(
        has_physical_address=True,
        has_opt_out=True,
        opt_out_works=True,
        honest_subject=True,
    ) == []


def test_gdpr_flags():
    issues = check_gdpr(has_lawful_basis=False, honors_deletion=False)
    codes = {i.code for i in issues}
    assert "GDPR_BASIS" in codes
    assert "GDPR_DELETE" in codes


def test_send_report_rates():
    r = SendReport()
    for status in ["delivered", "delivered", "bounced_hard", "complaint"]:
        r.add(SendEvent(email="x@y.z", status=status))
    s = r.summary()
    assert s["total"] == 4
    assert s["delivered"] == 2
    assert s["delivered_rate"] == 0.5

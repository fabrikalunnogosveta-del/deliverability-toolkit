# deliverability-toolkit

**Email deliverability infrastructure as code — domain warm-up, IP/domain rotation, suppression lists, compliance-first.**

**This is the solution, not the problem.** Production outbound systems need more than
“send mail”: they need schedules, rotation, bounce/complaint loops, and legal opt-out.

[![CI](https://github.com/fabrikalunnogosveta-del/deliverability-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/fabrikalunnogosveta-del/deliverability-toolkit/actions)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-12%20passed-brightgreen)

---

## The problem we solved

| Problem (before) | Solution (this library) |
|---|---|
| Blast from day one → spam folder | **Warm-up schedule** (volume ramps over weeks) |
| One burned domain kills all sending | **IP/domain rotation** + per-sender budgets |
| Hard bounces / complaints keep hitting | **Suppression list** (instant, persistent) |
| Legal risk on opt-out | **CAN-SPAM / GDPR** compliance helpers |
| No visibility into sender health | **Reputation checks** + send report |
| Ad-hoc scripts, no tests | Library + **pytest contracts** |

**Email deliverability is infrastructure, not spam.** This library is the mechanics
(schedules, lists, rotation) — no mailboxes, no data, no scraping.

---

## Architecture

```
warmup.py        # volume ramp: start small, grow by rules, never blast
rotation.py      # pick next domain/IP by budget + cooldown + health
suppression.py   # bounce/complaint/opt-out → never send again
compliance.py    # CAN-SPAM / GDPR checks (opt-out, identification)
report.py        # send report: delivered / bounced / suppressed
```

---

## How this maps to real jobs

| Job title | What this repo proves |
|---|---|
| **Email Deliverability Engineer** | warm-up, rotation, suppression loop |
| **Outbound / Growth Infrastructure** | sender budgets, reputation hygiene |
| **Backend / Python Engineer** | durable lists, rate limits, reports |

---

## Install

```bash
git clone https://github.com/fabrikalunnogosveta-del/deliverability-toolkit.git
cd deliverability-toolkit
pip install -r requirements.txt
```

## Quickstart

```python
from deliverability import WarmupSchedule, RotationPool, SuppressionList

# 1) Warm-up: day 1 = 20 sends, then grow
warmup = WarmupSchedule(start=20, growth=1.5, cap=2000)
assert warmup.volume_for_day(1) == 20
assert warmup.volume_for_day(10) > 20

# 2) Rotation: pick a healthy domain under budget
pool = RotationPool(domains=["a.example", "b.example"], daily_cap=100)
domain = pool.next_domain()

# 3) Suppression: hard bounce → never again
sup = SuppressionList()
sup.suppress("bad@example.com", reason="hard_bounce")
assert sup.is_suppressed("bad@example.com")
```

---

## Compliance first

- **CAN-SPAM**: physical address + working opt-out
- **GDPR**: honor deletion / suppression requests
- This library **does not send mail** — it manages the infrastructure layer
  (schedules, lists, rotation) used by a sending pipeline.

---

## Testing philosophy

- warm-up volume is monotonic and capped
- rotation respects daily caps and cooldowns
- suppression is durable and idempotent
- compliance flags missing opt-out / identification

```bash
python -m pytest tests/ -q
```

---

## Related

- [guards-and-laws](https://github.com/fabrikalunnogosveta-del/guards-and-laws) — LLM quality gates
- [structured-llm-output-guard](https://github.com/fabrikalunnogosveta-del/structured-llm-output-guard) — LLM → typed JSON
- [humanlike-browser-engine](https://github.com/fabrikalunnogosveta-del/humanlike-browser-engine) — human-like browser motion

---

## License

MIT

---

## Author

**Maxim Parshshin** — AI/LLM systems, quality gates, deliverability infrastructure.
Remote contracts.

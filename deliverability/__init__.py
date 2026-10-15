"""Email deliverability infrastructure: warm-up, rotation, suppression, compliance."""

from .warmup import WarmupSchedule
from .rotation import RotationPool, SenderStats
from .suppression import SuppressionList
from .compliance import ComplianceIssue, check_can_spam, check_gdpr
from .report import SendReport, SendEvent

__all__ = [
    "ComplianceIssue",
    "RotationPool",
    "SendEvent",
    "SendReport",
    "SenderStats",
    "SuppressionList",
    "WarmupSchedule",
    "check_can_spam",
    "check_gdpr",
]

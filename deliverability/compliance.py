"""Compliance helpers — CAN-SPAM / GDPR checks (does not send mail)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class ComplianceIssue:
    code: str
    message: str
    severity: str = "FLAG"  # FLAG | WARN


def check_can_spam(
    *,
    has_physical_address: bool,
    has_opt_out: bool,
    opt_out_works: bool = True,
    honest_subject: bool = True,
) -> List[ComplianceIssue]:
    issues: List[ComplianceIssue] = []
    if not has_physical_address:
        issues.append(ComplianceIssue("CANSPAM_ADDR", "Missing physical postal address"))
    if not has_opt_out:
        issues.append(ComplianceIssue("CANSPAM_OPTOUT", "Missing unsubscribe / opt-out"))
    elif not opt_out_works:
        issues.append(ComplianceIssue("CANSPAM_OPTOUT_BROKEN", "Opt-out must work"))
    if not honest_subject:
        issues.append(ComplianceIssue("CANSPAM_SUBJECT", "Subject must not be deceptive"))
    return issues


def check_gdpr(
    *,
    has_lawful_basis: bool,
    honors_deletion: bool,
    data_minimized: bool = True,
) -> List[ComplianceIssue]:
    issues: List[ComplianceIssue] = []
    if not has_lawful_basis:
        issues.append(ComplianceIssue("GDPR_BASIS", "No lawful basis recorded"))
    if not honors_deletion:
        issues.append(ComplianceIssue("GDPR_DELETE", "Must honor deletion / suppression"))
    if not data_minimized:
        issues.append(ComplianceIssue("GDPR_MINIMIZE", "Collect only necessary data", "WARN"))
    return issues

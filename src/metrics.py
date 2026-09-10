"""Governed vulnerability-remediation KPI calculations."""
from collections import Counter, defaultdict
from datetime import date
from statistics import median
from .models import Finding

WEIGHTS = {"critical": 4, "high": 3, "medium": 2, "low": 1}

def is_closed(f: Finding) -> bool:
    return f.status == "remediated" and f.validation_evidence

def calculate(findings: list[Finding], as_of: date) -> dict:
    open_items = [f for f in findings if not is_closed(f) and f.status != "risk_accepted"]
    overdue = [f for f in open_items if f.due < as_of]
    validated = [f for f in findings if is_closed(f)]
    durations = [(f.remediated - f.opened).days for f in validated if f.remediated]
    weighted_open = sum(WEIGHTS[f.severity] for f in open_items)
    weighted_overdue = sum(WEIGHTS[f.severity] for f in overdue)
    by_owner = defaultdict(lambda: {"open": 0, "overdue": 0})
    for f in open_items:
        by_owner[f.owner or "unassigned"]["open"] += 1
        if f in overdue: by_owner[f.owner or "unassigned"]["overdue"] += 1
    return {
        "total_findings": len(findings),
        "open_backlog": len(open_items),
        "overdue_backlog": len(overdue),
        "validated_closed": len(validated),
        "risk_accepted": sum(f.status == "risk_accepted" for f in findings),
        "sla_compliance_pct": round(100 * (1 - len(overdue) / len(open_items)), 1) if open_items else 100.0,
        "median_time_to_remediate_days": median(durations) if durations else None,
        "risk_weighted_overdue_pct": round(100 * weighted_overdue / weighted_open, 1) if weighted_open else 0.0,
        "open_by_severity": dict(Counter(f.severity for f in open_items)),
        "owner_metrics": dict(by_owner),
    }

def trend(current: dict, previous: dict) -> dict:
    """Positive backlog delta means deterioration; positive SLA delta means improvement."""
    return {
        "open_backlog_delta": current["open_backlog"] - previous["open_backlog"],
        "overdue_backlog_delta": current["overdue_backlog"] - previous["overdue_backlog"],
        "sla_compliance_delta_pp": round(current["sla_compliance_pct"] - previous["sla_compliance_pct"], 1),
    }

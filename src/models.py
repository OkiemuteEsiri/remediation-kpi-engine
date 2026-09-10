"""Validated models for synthetic vulnerability remediation metrics."""
from dataclasses import dataclass
from datetime import date, datetime

SEVERITIES = {"critical", "high", "medium", "low"}
STATUSES = {"open", "remediated", "risk_accepted"}

@dataclass(frozen=True)
class Finding:
    finding_id: str
    severity: str
    owner: str
    opened: date
    due: date
    status: str
    remediated: date | None = None
    validation_evidence: bool = False

    def __post_init__(self):
        if not self.finding_id.strip(): raise ValueError("finding_id required")
        if self.severity not in SEVERITIES: raise ValueError("invalid severity")
        if self.status not in STATUSES: raise ValueError("invalid status")
        if self.due < self.opened: raise ValueError("due cannot precede opened")
        if self.status == "remediated" and self.remediated is None: raise ValueError("remediated date required")
        if self.remediated and self.remediated < self.opened: raise ValueError("invalid remediation date")

def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()

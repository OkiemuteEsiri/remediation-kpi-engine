import unittest
from datetime import date
from src.models import Finding
from src.metrics import calculate, is_closed, trend

def f(**kw):
    base=dict(finding_id="X",severity="high",owner="Team",opened=date(2026,1,1),due=date(2026,1,31),status="open")
    base.update(kw); return Finding(**base)

class MetricsTests(unittest.TestCase):
    def test_invalid_severity_rejected(self):
        with self.assertRaises(ValueError): f(severity="urgent")
    def test_due_before_open_rejected(self):
        with self.assertRaises(ValueError): f(due=date(2025,12,1))
    def test_remediated_requires_date(self):
        with self.assertRaises(ValueError): f(status="remediated")
    def test_closure_requires_validation(self):
        item=f(status="remediated",remediated=date(2026,1,10),validation_evidence=False)
        self.assertFalse(is_closed(item))
    def test_validated_remediation_closes(self):
        item=f(status="remediated",remediated=date(2026,1,10),validation_evidence=True)
        self.assertTrue(is_closed(item))
    def test_risk_acceptance_separate_from_backlog(self):
        m=calculate([f(status="risk_accepted")],date(2026,2,1))
        self.assertEqual(m["risk_accepted"],1); self.assertEqual(m["open_backlog"],0)
    def test_overdue_and_sla(self):
        m=calculate([f(),f(finding_id="Y",due=date(2026,3,1))],date(2026,2,1))
        self.assertEqual(m["overdue_backlog"],1); self.assertEqual(m["sla_compliance_pct"],50.0)
    def test_mttr_uses_validated_closures(self):
        item=f(status="remediated",remediated=date(2026,1,11),validation_evidence=True)
        self.assertEqual(calculate([item],date(2026,2,1))["median_time_to_remediate_days"],10)
    def test_owner_metrics(self):
        m=calculate([f(owner="Platform")],date(2026,2,1))
        self.assertEqual(m["owner_metrics"]["Platform"]["overdue"],1)
    def test_trend_direction(self):
        t=trend({"open_backlog":3,"overdue_backlog":1,"sla_compliance_pct":80},{"open_backlog":5,"overdue_backlog":2,"sla_compliance_pct":60})
        self.assertEqual(t["open_backlog_delta"],-2); self.assertEqual(t["sla_compliance_delta_pp"],20)

if __name__ == "__main__": unittest.main()

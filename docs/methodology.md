# KPI Governance and Remediation Methodology

## Objective

Measure whether vulnerability risk is actually being reduced, not merely whether tickets are changing state. The engine separates operational backlog, SLA performance, risk-weighted overdue exposure, validated closure, risk acceptance and ownership.

## Metric definitions

- **Open backlog:** findings that are not validated closed and are not formally risk accepted.
- **Overdue backlog:** open findings whose remediation due date has passed.
- **SLA compliance:** `1 - overdue/open`; 100% when no open backlog exists.
- **Validated closed:** remediation is recorded and validation evidence exists.
- **Median time to remediate:** median elapsed days from opening to remediation for validated closures only.
- **Risk-weighted overdue %:** severity-weighted overdue exposure divided by severity-weighted open exposure.
- **Risk accepted:** governed exception state, reported separately rather than disguised as remediation.

## Governance controls

Metric definitions must be version-controlled. Dates are evaluated against an explicit reporting date. Owners should be mapped to accountable teams rather than inferred from scanner labels. A ticket marked remediated is not treated as closed until evidence demonstrates the vulnerable condition is no longer present.

## Remediation lifecycle

`identify -> prioritize -> assign -> remediate -> validate -> close -> monitor regression`

Validation evidence can include an authenticated rescan, configuration-state evidence, package/version verification, or another approved control-specific test. Exceptions require documented rationale, approver, compensating controls and expiry/review date in a production implementation.

## ATT&CK context

External exploitation and remote-service exposure can be contextualized with ATT&CK techniques such as T1190 and T1210. ATT&CK mapping informs prioritization and threat context; it is not evidence that exploitation occurred.

## Executive interpretation

Backlog volume alone is insufficient. Leadership should review overdue critical/high exposure, risk-weighted overdue percentage, SLA trend, validated closure throughput, aging, ownership concentration and exception volume together. A falling backlog with worsening risk-weighted overdue exposure can indicate that low-risk work is being closed while important exposure remains.

## Limitations

The public lab uses synthetic data and simplified severity weights. It does not claim production KPIs, scanner accuracy, client performance, exploitability, or business impact. Production use would require agreed SLA policy, asset criticality, threat intelligence, exception governance and data-quality controls.

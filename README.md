# Remediation KPI Engine

A defensive Vulnerability Management / Exposure Management engineering project for measuring whether remediation programs are reducing risk rather than merely closing tickets.

## Problem statement

Vulnerability programs can report large volumes of scanner findings while still struggling to answer basic governance questions: How much exposure is overdue? Are critical findings being reduced? Which owners are accumulating risk? Are findings really fixed, or merely marked remediated? This project turns synthetic finding lifecycle data into governed, explainable remediation KPIs.

## Architecture

```text
Synthetic finding lifecycle data
        |
        v
Validated data model
        |
        v
Closure + exception governance
        |
        v
KPI calculation engine
        |
        +--> backlog / overdue / SLA
        +--> validated closure / MTTR
        +--> risk-weighted overdue exposure
        +--> owner + severity metrics
        |
        v
Trend / executive decision support
```

## Implemented capabilities

- validated vulnerability lifecycle model
- explicit reporting-date calculations
- open and overdue backlog
- SLA compliance percentage
- validated-remediation closure rule
- median time to remediate
- severity-weighted overdue exposure
- risk-acceptance separation
- owner-level metrics
- severity distribution
- period-over-period trend deltas
- realistic synthetic portfolio data
- 10 unit tests
- executive reporting example
- least-privilege GitHub Actions workflow

## Why validated closure matters

A finding marked `remediated` is not counted as closed unless validation evidence is present. This models a core VM principle: remediation activity and verified risk reduction are different states. Risk acceptance is also reported separately so exceptions cannot silently inflate closure performance.

## Repository structure

```text
src/models.py                      validated lifecycle model
src/metrics.py                     governed KPI calculations
data/synthetic_findings.json       synthetic portfolio
 tests/test_metrics.py             unit tests
docs/methodology.md                definitions and governance
reports/example-executive-report.md decision-support example
.github/workflows/ci.yml           compile + unit-test gate
```

## KPI design

The project calculates open backlog, overdue backlog, SLA compliance, validated closures, risk acceptance, median remediation time, severity-weighted overdue percentage, severity distribution and owner metrics. Trend calculations distinguish backlog deterioration/improvement from percentage-point changes in SLA performance.

## Usage

Run the unit suite locally:

```bash
python -m unittest discover -s tests -v
```

The modules are intentionally dependency-light so the metric logic can be reviewed independently of a dashboard or scanner product.

## Remediation and validation workflow

`identify -> prioritize -> assign -> remediate -> validate -> close -> monitor regression`

Validation should use approved evidence appropriate to the control, such as authenticated rescans, configuration-state evidence or version/package verification. Production risk acceptance should include rationale, approver, compensating controls and an expiry/review date.

## MITRE ATT&CK context

Vulnerability exposure can be contextualized with techniques such as **T1190 – Exploit Public-Facing Application** and **T1210 – Exploitation of Remote Services**. ATT&CK context supports prioritization; it does not prove exploitation.

## Skills demonstrated

Risk-based Vulnerability Management, Exposure Management, KPI engineering, remediation governance, SLA measurement, data modeling, Python, unit testing, risk communication, exception governance, executive reporting and CI/CD quality controls.

## Limitations

All data is synthetic. Severity weights are deliberately simple and transparent. A production implementation would add asset criticality, KEV/EPSS-like threat context, business service mapping, approved SLA matrices, exception expiry, scanner reconciliation and data-quality monitoring.

## Roadmap

- configurable SLA policy matrix
- asset criticality and threat-context weighting
- aging-bucket metrics
- exception-expiry governance
- CSV/JSON ingestion CLI
- Markdown/JSON report generation
- regression and reopening metrics
- dashboard-ready export schema

## Safety and data handling

No employer/client data, credentials, production targets or fabricated operational metrics are included. The repository is a synthetic defensive engineering lab designed to demonstrate methodology and implementation quality.

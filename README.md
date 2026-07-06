# SJC_Intel

AI-assisted local intelligence/reporting for St. Johns County, Florida.

**During development, the primary entrypoint is `README_INTERNAL.md`.**
Start there for architecture, status, and next actions.

See `AGENTS.md` for agent roles, git policy, and logging rules.

## Setup

```bash
pip install -r requirements.txt
```

## Validation

Run offline (no network, no VPS, no credentials):

```bash
python3 -m pytest tests/ -v
python3 scripts/validate.py
```

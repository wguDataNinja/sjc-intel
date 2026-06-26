# SJC_Intel — Deep Research Intake

> Raw output from ChatGPT Deep Research and similar external research tools
> goes here. Nothing in this directory is canonical. Everything here is a
> **candidate** that must be reviewed before promotion.

## Purpose

A ChatGPT Deep Research report may return with homeowner-focused source
discovery for St. Johns County — candidate government sources, community/
developer sources, homeowner beats, search terms, blind spots, and
recommendations. This directory stores that output in its raw form so it
can be systematically reviewed and selectively promoted without
contaminating the canonical registries.

## Rules

1. **Raw reports are not canonical.** They go in this directory as-is.
2. **Candidates must be reviewed** before promotion to canonical sources,
   beats, search terms, or taxonomy.
3. **Sources should be assessed from a homeowner/resident perspective.**
   Not every interesting source is relevant to SJC_Intel's mission.
4. **Nothing here automatically feeds the monitoring pipeline.** Promotion
   requires explicit review and approval.

## Directory Structure

```
docs/deep_research/
├── README.md              # This file
├── reports/               # Raw Deep Research output files
│   └── YYYY-MM-DD_topic.md
└── review/                # Review notes, promotion decisions
    └── YYYY-MM-DD_review.md
```

## Workflow

See `docs/deep_research_ingestion.md` for the full intake workflow.

## Related Candidate Registries

- `registry/source_candidates.yaml` — Candidate sources extracted from research
- `registry/beat_candidates.yaml` — Candidate beats extracted from research
- `registry/search_terms.yaml` — Candidate search terms across categories

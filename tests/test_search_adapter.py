"""Tests for the provider-neutral search adapter (budgets, receipts, dedupe)."""
from pathlib import Path

import pytest

from scripts import search_adapter as sa


def stub_provider():
    rows = {
        '"magnolia oaks academy"': [
            sa.RawResult("Magnolia Oaks Academy opens", "https://news.example.com/a", "2026-07-22T07:00:00Z"),
            sa.RawResult("Magnolia Oaks Academy opens", "https://news.example.com/a", "2026-07-22T07:00:00Z"),  # dup
            sa.RawResult("Magnolia school", "https://other.example.org/b", "2026-07-01T07:00:00Z"),
        ],
        '"water shortage"': [
            sa.RawResult("Water shortage", "https://news.example.com/c", "2026-05-11T07:00:00Z"),
        ],
    }
    return sa.StubProvider(rows)


def run_one(query, spec_kwargs=None, budget=3):
    tracker = sa.BudgetTracker(run_budget=budget)
    spec = sa.SearchSpec(query=query, **(spec_kwargs or {}))
    return sa.execute_search(spec, "RUN-1", "RUN-1-Q01", tracker, stub_provider())


def test_budget_rejection():
    tracker = sa.BudgetTracker(run_budget=1)
    tracker.spend(sa.SearchSpec(query="a"))  # budget=1 default
    with pytest.raises(sa.BudgetError):
        tracker.check(sa.SearchSpec(query="b"))


def test_lane_profile_subject_budget_enforced():
    tracker = sa.BudgetTracker(run_budget=10, per_lane=1)
    spec = sa.SearchSpec(query="a", lane="schools")
    tracker.spend(spec)
    with pytest.raises(sa.BudgetError):
        tracker.check(sa.SearchSpec(query="b", lane="schools"))
    # Different lane still allowed.
    tracker.check(sa.SearchSpec(query="c", lane="roads"))


def test_receipt_fields_and_normalization():
    outcome = run_one('"magnolia oaks academy"')
    rec = outcome.receipt
    assert rec.run_id == "RUN-1" and rec.query_id == "RUN-1-Q01"
    assert rec.result_count == 3
    assert rec.accepted_result_count == 2  # one cross-query dup dropped
    assert rec.duplicate_count == 1
    assert rec.failure is None
    assert rec.cost_estimate == 0.0
    assert rec.budget_before == 3 and rec.budget_after == 2
    assert rec.result_hashes and len(rec.result_hashes) == 2
    assert rec.raw_sha256 and len(rec.raw_sha256) == 64
    assert not rec.simulated is False
    urls = [n.url for n in outcome.results]
    assert "https://news.example.com/a" in urls
    assert len(urls) == len(set(urls))


def test_duplicate_handling_across_queries():
    tracker = sa.BudgetTracker(run_budget=2)
    seen = set()
    spec1 = sa.SearchSpec(query='"magnolia oaks academy"')
    spec2 = sa.SearchSpec(query='"magnolia oaks academy"')
    o1 = sa.execute_search(spec1, "RUN", "Q1", tracker, stub_provider(), seen)
    o2 = sa.execute_search(spec2, "RUN", "Q2", tracker, stub_provider(), seen)
    assert len(o1.results) == 2
    assert len(o2.results) == 0
    assert o2.receipt.accepted_result_count == 0
    assert o2.receipt.duplicate_count == 3  # all three rows already seen


def test_no_match_recorded():
    outcome = run_one('"nothing matches"')
    assert outcome.receipt.accepted_result_count == 0
    assert outcome.receipt.result_count == 0
    assert outcome.results == []


def test_failure_and_retry(tmp_path):
    class FailingThenOk(sa.SearchProvider):
        name = "flaky"
        simulated = True

        def __init__(self):
            self.calls = 0

        def search(self, spec):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("boom")
            return "stub://ok", b"raw", [sa.RawResult("Ok", "https://x.example.com/1", None)]

    sa.register_provider(FailingThenOk)
    try:
        tracker = sa.BudgetTracker(run_budget=2)
        spec = sa.SearchSpec(query="q", provider="flaky", retry_limit=1)
        outcome = sa.execute_search(spec, "RUN", "Q", tracker, FailingThenOk())
        assert outcome.receipt.failure is None
        assert outcome.receipt.accepted_result_count == 1
    finally:
        sa._PROVIDERS.pop("flaky", None)


def test_domain_constraints():
    ok = run_one('"magnolia oaks academy"', spec_kwargs={"allowed_domains": ("news.example.com",)})
    assert all(n.domain == "news.example.com" for n in ok.results)
    blocked = run_one('"magnolia oaks academy"', spec_kwargs={"excluded_domains": ("news.example.com",)})
    assert all(n.domain != "news.example.com" for n in blocked.results)


def test_date_window():
    spec = sa.SearchSpec(query='"magnolia oaks academy"', date_after="2026-07-15")
    tracker = sa.BudgetTracker(run_budget=1)
    outcome = sa.execute_search(spec, "R", "Q", tracker, stub_provider())
    dates = [n.published_at for n in outcome.results]
    assert dates and all(d[:10] >= "2026-07-15" for d in dates)


def test_provider_isolation_unknown():
    with pytest.raises(sa.ProviderIsolationError):
        sa.create_provider("does-not-exist")


def test_provider_registry_has_live_and_stub():
    assert "google_news_rss" in sa.list_providers()
    assert "stub" in sa.list_providers()


def test_result_limit():
    spec = sa.SearchSpec(query='"magnolia oaks academy"', result_limit=1)
    tracker = sa.BudgetTracker(run_budget=1)
    outcome = sa.execute_search(spec, "R", "Q", tracker, stub_provider())
    assert len(outcome.results) == 1

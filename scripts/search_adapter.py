#!/usr/bin/env python3
"""Provider-neutral bounded public search adapter for supervised discovery.

Design goals:
  * no repository code depends on a single commercial provider;
  * every query emits a machine-readable receipt;
  * budgets are enforced by run / lane / profile / subject / domain;
  * results are normalized and deduplicated before the strategist sees them;
  * no-match and failure are first-class outcomes;
  * a deterministic stub provider keeps simulation and tests offline.

Providers are registered by name. ``google_news_rss`` is the approved
credential-free live discovery provider in the current environment; it returns
leads for human review, never primary authority. ``stub`` is deterministic and
used for simulation and tests. Adding a commercial provider only requires a new
subclass plus registration; nothing else changes.
"""
from __future__ import annotations

import abc
import dataclasses
import datetime as dt
import email.utils
import hashlib
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any, Callable

DEFAULT_USER_AGENT = "SJC-Intel/1.0 public research"
DEFAULT_TIMEOUT = 15
DEFAULT_RETRY_LIMIT = 2


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _parse_pubdate(value: str) -> str | None:
    """Parse RFC-822 (RSS) pubDate to ISO UTC; return None when unparsable."""
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return None


def domain_of(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


@dataclasses.dataclass(frozen=True)
class SearchSpec:
    """One bounded search request."""

    query: str
    provider: str = "google_news_rss"
    result_limit: int = 5
    allowed_domains: tuple[str, ...] = ()
    excluded_domains: tuple[str, ...] = ()
    date_after: str | None = None  # ISO date or datetime
    date_before: str | None = None
    timeout: int = DEFAULT_TIMEOUT
    retry_limit: int = DEFAULT_RETRY_LIMIT
    user_agent: str = DEFAULT_USER_AGENT
    budget: int = 1
    lane: str | None = None
    subject: str | None = None
    source_profile: str = "live_pilot"
    labels: tuple[str, ...] = ()

    def allowed(self, domain: str) -> bool:
        if self.allowed_domains and domain not in self.allowed_domains:
            return False
        if domain in self.excluded_domains:
            return False
        return True

    def in_date_window(self, published_at: str | None) -> bool:
        if not published_at:
            return True
        value = dt.date.fromisoformat(published_at[:10])
        if self.date_after and value < dt.date.fromisoformat(self.date_after[:10]):
            return False
        if self.date_before and value > dt.date.fromisoformat(self.date_before[:10]):
            return False
        return True


@dataclasses.dataclass
class RawResult:
    title: str
    url: str
    published_at: str | None
    source_type: str = "news_rss"


@dataclasses.dataclass
class NormalizedResult:
    url: str
    title: str
    domain: str
    published_at: str | None
    source_type: str
    hash: str
    run_id: str
    query_id: str
    provider: str


@dataclasses.dataclass
class SearchReceipt:
    run_id: str
    query_id: str
    provider: str
    query: str
    source_profile: str
    lanes: list[str]
    subjects: list[str]
    allowed_domains: list[str]
    excluded_domains: list[str]
    started_at: str
    completed_at: str | None
    simulated: bool
    result_count: int
    accepted_result_count: int
    duplicate_count: int
    failure: str | None
    cost_estimate: float
    budget_before: int
    budget_after: int
    result_urls: list[str]
    result_hashes: list[str]
    raw_sha256: str | None

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SearchOutcome:
    receipt: SearchReceipt
    results: list[NormalizedResult]
    raw_rows: list[dict[str, Any]]


class BudgetError(Exception):
    pass


class ProviderIsolationError(Exception):
    pass


class BudgetTracker:
    """Enforce search budgets at run, lane, profile, subject, and domain scope."""

    def __init__(self, run_budget: int, per_lane: int | None = None,
                 per_profile: int | None = None, per_subject: int | None = None,
                 per_domain: int | None = None):
        self.limits = {
            "run": run_budget,
            "lane": per_lane,
            "profile": per_profile,
            "subject": per_subject,
            "domain": per_domain,
        }
        self.spent = {"run": 0, "lane": {}, "profile": {}, "subject": {}, "domain": {}}

    def remaining(self, spec: SearchSpec) -> int:
        allowed = self.limits["run"] - self.spent["run"]
        if spec.lane and self.limits["lane"] is not None:
            allowed = min(allowed, self.limits["lane"] - self.spent["lane"].get(spec.lane, 0))
        if spec.source_profile and self.limits["profile"] is not None:
            allowed = min(allowed, self.limits["profile"] - self.spent["profile"].get(spec.source_profile, 0))
        if spec.subject and self.limits["subject"] is not None:
            allowed = min(allowed, self.limits["subject"] - self.spent["subject"].get(spec.subject, 0))
        for domain in spec.allowed_domains:
            if domain and self.limits["domain"] is not None:
                allowed = min(allowed, self.limits["domain"] - self.spent["domain"].get(domain, 0))
        return allowed

    def check(self, spec: SearchSpec) -> None:
        if self.remaining(spec) < spec.budget:
            raise BudgetError(
                f"budget exhausted for {spec.query!r} (lane={spec.lane}, "
                f"profile={spec.source_profile}, subject={spec.subject})"
            )

    def spend(self, spec: SearchSpec) -> None:
        self.spent["run"] += spec.budget
        if spec.lane:
            self.spent["lane"][spec.lane] = self.spent["lane"].get(spec.lane, 0) + spec.budget
        if spec.source_profile:
            self.spent["profile"][spec.source_profile] = self.spent["profile"].get(spec.source_profile, 0) + spec.budget
        if spec.subject:
            self.spent["subject"][spec.subject] = self.spent["subject"].get(spec.subject, 0) + spec.budget
        for domain in spec.allowed_domains:
            if domain:
                self.spent["domain"][domain] = self.spent["domain"].get(domain, 0) + spec.budget

    def to_dict(self) -> dict[str, Any]:
        return {"limits": self.limits, "spent": self.spent}


class SearchProvider(abc.ABC):
    name: str
    simulated = False

    @abc.abstractmethod
    def search(self, spec: SearchSpec) -> tuple[str, bytes, list[RawResult]]:
        """Return (endpoint, raw_bytes, rows). Raise on unrecoverable failure."""


class GoogleNewsRSSProvider(SearchProvider):
    name = "google_news_rss"
    simulated = False

    def search(self, spec: SearchSpec) -> tuple[str, bytes, list[RawResult]]:
        q = spec.query
        if spec.date_after:
            q += f" after:{spec.date_after[:10]}"
        if spec.date_before:
            q += f" before:{spec.date_before[:10]}"
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
            {"q": q, "hl": "en-US", "gl": "US", "ceid": "US:en"}
        )
        last_error: Exception | None = None
        for attempt in range(spec.retry_limit + 1):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": spec.user_agent})
                with urllib.request.urlopen(req, timeout=spec.timeout) as res:
                    raw = res.read()
                root = ET.fromstring(raw)
                rows: list[RawResult] = []
                for item in root.findall(".//item"):
                    title = (item.findtext("title") or "").strip()
                    link = (item.findtext("link") or "").strip()
                    if not title or not link:
                        continue
                    rows.append(RawResult(title=title, url=link,
                                          published_at=_parse_pubdate(item.findtext("pubDate") or "")))
                    if len(rows) >= spec.result_limit:
                        break
                return url, raw, rows
            except Exception as exc:  # noqa: BLE001 - retry boundary
                last_error = exc
                if attempt < spec.retry_limit:
                    time.sleep(min(2 ** attempt, 4))
        raise last_error or RuntimeError("search failed")


class StubProvider(SearchProvider):
    """Deterministic offline provider used by simulation and tests."""

    name = "stub"
    simulated = True

    def __init__(self, rows: dict[str, list[RawResult]] | None = None):
        self._rows = rows or {}

    def search(self, spec: SearchSpec) -> tuple[str, bytes, list[RawResult]]:
        endpoint = f"stub://search?q={urllib.parse.quote(spec.query)}"
        raw = f"stub-{spec.query}".encode("utf-8")
        rows = self._rows.get(spec.query.lower(), [])
        rows = [r for r in rows if spec.allowed(domain_of(r.url))]
        return endpoint, raw, rows[: spec.result_limit]


_PROVIDERS: dict[str, type[SearchProvider]] = {
    GoogleNewsRSSProvider.name: GoogleNewsRSSProvider,
    StubProvider.name: StubProvider,
}


def register_provider(provider: type[SearchProvider]) -> None:
    _PROVIDERS[provider.name] = provider


def list_providers() -> list[str]:
    return sorted(_PROVIDERS)


def create_provider(name: str, **kwargs: Any) -> SearchProvider:
    if name not in _PROVIDERS:
        raise ProviderIsolationError(f"unknown search provider: {name!r}")
    return _PROVIDERS[name](**kwargs)


def execute_search(spec: SearchSpec, run_id: str, query_id: str,
                   tracker: BudgetTracker, provider: SearchProvider,
                   known_hashes: set[str] | None = None) -> SearchOutcome:
    """Run one bounded query, record a receipt, and normalize + dedupe results."""
    tracker.check(spec)
    budget_before = tracker.remaining(spec)
    seen = known_hashes if known_hashes is not None else set()
    started = now_utc()
    endpoint = ""
    raw = b""
    rows: list[RawResult] = []
    failure: str | None = None
    simulated = provider.simulated
    for attempt in range(spec.retry_limit + 1):
        try:
            endpoint, raw, rows = provider.search(spec)
            failure = None
            break
        except Exception as exc:  # noqa: BLE001 - receipt must be produced
            failure = str(exc)[:300]
            if attempt < spec.retry_limit:
                time.sleep(0.2)
    completed = now_utc()
    tracker.spend(spec)

    normalized: list[NormalizedResult] = []
    raw_rows: list[dict[str, Any]] = []
    dupes = 0
    for row in rows:
        domain = domain_of(row.url)
        raw_rows.append({"title": row.title, "url": row.url, "domain": domain,
                         "published_at": row.published_at, "source_type": row.source_type})
        if not spec.allowed(domain):
            continue
        if not spec.in_date_window(row.published_at):
            continue
        h = _url_hash(row.url)
        if h in seen:
            dupes += 1
            continue
        seen.add(h)
        normalized.append(NormalizedResult(url=row.url, title=row.title, domain=domain,
                                           published_at=row.published_at, source_type=row.source_type,
                                           hash=h, run_id=run_id, query_id=query_id, provider=provider.name))
    receipt = SearchReceipt(
        run_id=run_id, query_id=query_id, provider=provider.name, query=spec.query,
        source_profile=spec.source_profile,
        lanes=[spec.lane] if spec.lane else [],
        subjects=[spec.subject] if spec.subject else [],
        allowed_domains=list(spec.allowed_domains), excluded_domains=list(spec.excluded_domains),
        started_at=started, completed_at=completed, simulated=simulated,
        result_count=len(rows), accepted_result_count=len(normalized), duplicate_count=dupes,
        failure=failure, cost_estimate=0.0, budget_before=budget_before,
        budget_after=tracker.remaining(spec),
        result_urls=[n.url for n in normalized], result_hashes=[n.hash for n in normalized],
        raw_sha256=hashlib.sha256(raw).hexdigest() if raw else None,
    )
    return SearchOutcome(receipt=receipt, results=normalized, raw_rows=raw_rows)


def default_subject_rules() -> list[tuple[str, str, str]]:
    """Return (needle, canonical subject, lane) matching rules for resident leads."""
    return [
        ("magnolia oaks", "Magnolia Oaks Academy", "schools and families"),
        # School QQ is the former planning placeholder for Magnolia Oaks.
        ("school qq", "Magnolia Oaks Academy", "schools and families"),
        ("cr 2209", "CR 2209 connector", "roads and mobility"),
        ("first coast expressway", "First Coast Expressway access", "roads and mobility"),
        ("publix", "Publix at Silverleaf Market", "retail and amenities"),
        ("harris teeter", "SilverLeaf grocery center — possible Harris Teeter", "retail and amenities"),
        ("baptist", "Baptist SilverLeaf campus", "healthcare and services"),
        ("water", "utilities and water", "utilities and household operations"),
    ]

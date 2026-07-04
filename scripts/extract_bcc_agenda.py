#!/usr/bin/env python3
"""
BCC Agenda extractor for SJC_Intel — Phase 2 with PDF text extraction.

Fetches Clerk Board Records, resolves agenda PDFs, extracts text via pypdf,
parses individual agenda items, classifies by resident impact, and produces
normalized intel_item records.

Primary source: https://stjohnsclerk.com/board-records/agendas/
PDF dependency: pypdf
"""
import re
import os
import sys
import yaml
import hashlib
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

CLERK_URL = "https://stjohnsclerk.com/board-records/agendas/"
USER_AGENT = "Mozilla/5.0 (SJC_Intel BCC Extractor/1.0)"
BASE_INTEL_DIR = "data/intel_items"
BASE_SOURCE_EVENTS_DIR = "data/source_events"
PDF_FIXTURE_DIR = "tests/fixtures"
TEXT_FIXTURE_DIR = "tests/fixtures"
SOURCE_EVENT_PREFIX = "EVT-BCC"


# ── Deterministic PDF URLs ──────────────────────────────────────────────

def expected_pdf_url(date_str, suffix):
    parts = date_str.split("/")
    if len(parts) != 3:
        return None
    m, d, y = parts
    y2 = y[2:4]
    return f"https://stjohnsclerk.com/wp-content/uploads/2026/{m.zfill(2)}/{m}{d}{y2}{suffix}.pdf"


def expected_agenda_url(date_str):
    return expected_pdf_url(date_str, "arbcc")


def expected_minutes_url(date_str):
    return expected_pdf_url(date_str, "mrbcc")


# ── Clerk HTML Parser ───────────────────────────────────────────────────

class ClerkTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_cell = ""
        self.current_row = []
        self.rows = []
        self.cell_links = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cls = d.get("class", "")
        if tag == "table" and "eael-data-table" in cls:
            self.in_table = True
        if not self.in_table:
            return
        if tag == "tr":
            self.in_row = True
            self.current_row = []
        if tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = ""
            self.cell_links = []

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        if tag == "tr" and self.in_row:
            if self.current_row:
                self.rows.append(self.current_row)
            self.in_row = False
        if tag in ("td", "th") and self.in_cell:
            self.current_row.append({
                "text": self.current_cell.strip(),
                "links": list(self.cell_links),
            })
            self.in_cell = False

    def handle_data(self, data):
        if not self.in_table or not self.in_cell:
            return
        self.current_cell += data

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self.current_cell += "\n"


def fetch_page(url=None):
    u = url or CLERK_URL
    req = urllib.request.Request(u, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def check_url(url):
    if not url:
        return False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def download_file(url, filepath):
    if not url:
        return False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(filepath, "wb") as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"  Download failed: {e}", file=sys.stderr)
        return False


def parse_meetings(html):
    """Parse Clerk HTML into meeting records."""
    parser = ClerkTableParser()
    parser.feed(html)
    meetings = []
    for row in parser.rows:
        if len(row) < 4:
            continue
        date_cell = row[0]
        agenda_cell = row[1] if len(row) > 1 else {"text": "", "links": []}
        minutes_cell = row[2] if len(row) > 2 else {"text": "", "links": []}

        date_str = date_cell["text"].strip()
        if not date_str or not re.match(r"\d{1,2}/\d{1,2}/\d{4}", date_str):
            continue

        agenda_links = agenda_cell.get("links", [])
        minutes_links = minutes_cell.get("links", [])

        agenda_url = agenda_links[0] if agenda_links else ""
        minutes_url = minutes_links[0] if minutes_links else ""

        link_is_broken = False
        if agenda_url and "mrbcc" in agenda_url:
            link_is_broken = True
            expected = expected_agenda_url(date_str)
            if expected:
                agenda_url = expected

        meetings.append({
            "date": date_str,
            "agenda_url": agenda_url,
            "minutes_url": minutes_url,
            "agenda_link_broken": link_is_broken,
            "expected_agenda_url": expected_agenda_url(date_str),
        })
    return meetings


# ── PDF Text Extraction ─────────────────────────────────────────────────

def extract_pdf_text(filepath):
    """Extract text from a PDF file using pypdf."""
    if not HAS_PYPDF:
        print("  WARNING: pypdf not available. Cannot extract PDF text.", file=sys.stderr)
        return ""
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def parse_agenda_items(text, meeting_date):
    """Split agenda PDF text into individual agenda items.
    
    Handles multiple numbering sections (Regular Agenda items 1-N,
    then Consent Agenda items starting again at 1). Filters out
    non-item numbered references (e.g., statutory citations like "403.").
    """
    lines = text.split("\n")
    items = []
    current_item = None
    item_num = 0
    section = "preamble"
    found_public_hearing = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Detect section transitions
        if "consent agenda" in stripped.lower() and "approval" not in stripped.lower():
            section = "consent"
        elif "regular meeting" in stripped.upper():
            section = "regular"

        # Skip very long numbers that are statutory references (e.g., "403.")
        skip_long = re.match(r'^(\d{3,})\.\s', stripped)
        if skip_long and int(skip_long.group(1)) > 100:
            continue

        # Detect agenda item: starts with number period
        item_match = re.match(r'^(\d{1,2})\.\s+(.*)', stripped)

        if item_match:
            # Save previous item
            if current_item and current_item["text"].strip():
                items.append(current_item)

            item_num += 1
            num = item_match.group(1)
            title = item_match.group(2)[:200]
            
            # Determine section context
            if "public hearing" in stripped.lower():
                section = "public_hearing"
                found_public_hearing = True
            elif found_public_hearing and "motion" in stripped.lower():
                section = "consent"

            current_item = {
                "number": f"{section}.{num}",
                "title": title,
                "text": stripped,
                "lines": [stripped],
                "section": section,
                "action_type": classify_action_type(stripped),
            }
        elif current_item:
            current_item["text"] += "\n" + stripped
            current_item["lines"].append(stripped)
            if len(current_item["lines"]) <= 3 and len(current_item["title"]) < 80:
                current_item["title"] += " " + stripped[:80]

    # Last item
    if current_item and current_item["text"].strip():
        items.append(current_item)

    if not items:
        items = fallback_split(text)

    return items


def fallback_split(text):
    """Fallback: split by common BCC agenda section headers."""
    sections = []
    current = {"title": "Preamble", "text": "", "number": "0", "action_type": "other", "lines": []}
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            continue
        # Detect section headers
        if re.match(r'^(CONSENT AGENDA|REGULAR AGENDA|PUBLIC HEARING|REPORTS| ordinances| resolutions|contracts)', s, re.IGNORECASE):
            if current["text"].strip():
                sections.append(current)
            current = {"title": s, "text": s, "number": str(len(sections) + 1), "action_type": "other", "lines": [s]}
        else:
            current["text"] += "\n" + s
            current["lines"].append(s)
    if current["text"].strip():
        sections.append(current)
    return sections


def classify_action_type(text):
    """Classify an agenda item into an action type."""
    t = text.lower()
    if "public hearing" in t or "public hearing" in text[:50].lower():
        return "public_hearing"
    if "ordinance" in t:
        return "ordinance"
    if "resolution" in t:
        return "resolution"
    if "contract" in t or "agreement" in t or "award" in t:
        return "contract"
    if "budget" in t or "millage" in t or "appropriation" in t:
        return "budget"
    if "rezoning" in t or "rez" in t or "comp plan" in t or "comprehensive plan" in t or "pud" in t:
        return "land_use"
    if "procurement" in t or "bid" in t or "rfb" in t or "rfq" in t or "rfi" in t:
        return "procurement"
    if "proclamat" in t:
        return "proclamation"
    if "consent" in t or "minutes" in t:
        return "consent"
    return "regular_agenda"


def classify_resident_impact(item_text, item_title):
    """Classify an agenda item as high/medium/low signal."""
    t = (item_text + " " + item_title).lower()

    # High signal — directly affects residents
    high_keywords = [
        "rezoning", "rezone", "comp plan", "comprehensive plan", "pud", "dri",
        "road", "traffic", "infrastructure", "closure",
        "utility", "water", "sewer", "reclaimed", "boil", "reuse",
        "budget", "millage", "fee", "assessment", "tax",
        "capital project", "procurement", "construction",
        "park", "library", "beach", "facility",
        "public safety", "emergency", "fire", "sheriff",
        "cdd", "special district", "school",
        "ordinance", "public hearing",
    ]
    # Medium signal — notable but less direct
    medium_keywords = [
        "contract", "agreement", "award", "grant",
        "appointment", "board", "committee",
        "plan", "study", "report",
        "amendment", "modification",
    ]
    # Low/routine
    low_keywords = [
        "proclamation", "minutes", "consent", "ceremonial",
        "recognize", "commend", "congratulate",
    ]

    for kw in high_keywords:
        if kw in t:
            return "high_signal"
    for kw in medium_keywords:
        if kw in t:
            return "medium_signal"
    for kw in low_keywords:
        if kw in t:
            return "low_signal"
    return "routine_noise"


def map_beat(action_type, signal, text, title):
    """Map agenda item to resident-interest beat."""
    t = (text + " " + title).lower()
    if "rezoning" in t or "rezone" in t or "comp plan" in t or "comprehensive plan" in t or "pud" in t or "dri" in t:
        return "rezoning_comp_plan_dri"
    if "road" in t or "traffic" in t or "infrastructure" in t or "closure" in t or "transportation" in t:
        return "transportation"
    if "water" in t or "sewer" in t or "utility" in t or "reclaimed" in t or "reuse" in t:
        return "utilities_water"
    if "budget" in t or "millage" in t or "fee" in t or "tax" in t or "appropriation" in t:
        return "taxes_exemptions_trim_vab"
    if "park" in t or "library" in t or "beach" in t or "recreation" in t:
        return "parks_amenities"
    if "public safety" in t or "emergency" in t or "fire" in t or "sheriff" in t:
        return "public_safety_livability"
    if "contract" in t or "procurement" in t or "bid" in t or "award" in t:
        return "local_government_budget_procurement"
    if "proclamat" in t or "recognize" in t or "commend" in t:
        return "parks_amenities"
    if "ordinance" in t or "resolution" in t or "public hearing" in t:
        return "local_government_budget_procurement"
    if "consent" in t:
        return "local_government_budget_procurement"
    return "local_government_budget_procurement"


def map_topics(beat):
    mapping = {
        "rezoning_comp_plan_dri": ["development", "county_government", "public_notices"],
        "transportation": ["transportation", "infrastructure"],
        "utilities_water": ["infrastructure", "environment"],
        "taxes_exemptions_trim_vab": ["taxes", "county_government"],
        "parks_amenities": ["parks_recreation", "community_events"],
        "public_safety_livability": ["public_safety"],
        "local_government_budget_procurement": ["county_government"],
    }
    return mapping.get(beat, ["county_government"])


# ── Source Event Generation ──────────────────────────────────────────────

def write_source_events(meeting_events, output_date, fetched_at):
    """Write source_event records for processed BCC meetings."""
    se_dir = os.path.join(BASE_SOURCE_EVENTS_DIR, output_date)
    os.makedirs(se_dir, exist_ok=True)

    se_path = os.path.join(se_dir, "sjc_bcc_calendar.yaml")
    source_event_data = {
        "source_id": "sjc_bcc_calendar",
        "generated_at": fetched_at,
        "total_events": len(meeting_events),
        "events": meeting_events,
    }
    with open(se_path, "w") as f:
        yaml.dump(source_event_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Wrote {len(meeting_events)} source events to {se_path}")


def build_meeting_event(meeting_date, meeting_info, item_ids, status, extraction_status, source_health, notes=""):
    """Build a source event record for a single BCC meeting."""
    parts = meeting_date.split("/")
    yr, m, d = parts[2], parts[0].zfill(2), parts[1].zfill(2)
    if len(yr) == 2:
        yr = "20" + yr
    iso_date = f"{yr}-{m}-{d}"
    compact = iso_date.replace("-", "")

    return {
        "event_id": f"EVT-BCC-{compact}-0001",
        "source_id": "sjc_bcc_calendar",
        "event_type": "meeting",
        "title": f"BCC Regular Meeting — {iso_date}",
        "event_date": iso_date,
        "discovered_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_url": CLERK_URL,
        "document_urls": {
            "agenda": meeting_info.get("agenda_url", ""),
            "minutes": meeting_info.get("minutes_url", ""),
        },
        "status": status,
        "extraction_status": extraction_status,
        "source_health": source_health,
        "extracted_item_ids": sorted(item_ids),
        "related_source_event_ids": [],
        "notes": notes,
        "raw_source_file": "tests/fixtures/clerk_agendas.html",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print("BCC Agenda Extractor — Phase 2 (PDF Text Extraction)")
    print("=" * 60)

    if not HAS_PYPDF:
        print("ERROR: pypdf is required. Install: pip install pypdf")
        sys.exit(1)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1. Fetch Clerk page
    print("\n1. Fetching Clerk Board Records page...")
    html = fetch_page()
    print(f"   Fetched {len(html)} bytes")

    os.makedirs(PDF_FIXTURE_DIR, exist_ok=True)
    with open(f"{PDF_FIXTURE_DIR}/clerk_agendas.html", "w") as f:
        f.write(html)

    # 2. Parse meetings
    meetings = parse_meetings(html)
    print(f"   Found {len(meetings)} meetings")

    # 3. Find accessible agenda PDFs
    print("\n2. Checking agenda PDF accessibility...")
    accessible = []
    for m in meetings:
        if m["agenda_link_broken"]:
            if check_url(m["expected_agenda_url"]):
                m["agenda_url"] = m["expected_agenda_url"]
                m["agenda_link_broken"] = False
                print(f"   {m['date']}: fixed via expected URL")
            else:
                print(f"   {m['date']}: broken (404)")
        elif m["agenda_url"]:
            if check_url(m["agenda_url"]):
                accessible.append(m)
                print(f"   {m['date']}: agenda accessible")
            else:
                print(f"   {m['date']}: agenda URL reported but 404")

    # 4. Process the latest accessible agenda + fixture (Jan 20)
    print("\n3. Processing agenda PDFs...")
    all_items = []
    meeting_events = []

    pdfs_to_process = [
        ("tests/fixtures/1202026_agenda.pdf", "1/20/2026", "fixture"),
    ]

    if accessible:
        latest = accessible[0]
        live_path = f"{PDF_FIXTURE_DIR}/{latest['date'].replace('/', '')}_agenda.pdf"
        if download_file(latest["agenda_url"], live_path):
            pdfs_to_process.append((live_path, latest["date"], "live"))
            print(f"   Downloaded live agenda: {latest['date']}")
        else:
            print(f"   Could not download {latest['date']} agenda")

    for pdf_path, meeting_date_str, source_type in pdfs_to_process:
        print(f"\n   Processing {source_type} PDF: {meeting_date_str}")
        if not os.path.exists(pdf_path):
            print(f"     File not found: {pdf_path}")
            continue

        text = extract_pdf_text(pdf_path)
        print(f"     Extracted {len(text)} chars from PDF")

        # Save text fixture
        txt_path = pdf_path.replace(".pdf", ".txt")
        with open(txt_path, "w") as f:
            f.write(text)
        print(f"     Saved text fixture: {txt_path}")

        # Parse agenda items
        items = parse_agenda_items(text, meeting_date_str)
        print(f"     Parsed {len(items)} agenda items")

        # Build source event for this meeting
        try:
            parts = meeting_date_str.split("/")
            yr = parts[2]
            if len(yr) == 2:
                yr = "20" + yr
            iso_date = f"{yr}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
        except:
            iso_date = meeting_date_str

        compact = iso_date.replace("-", "")
        if source_type == "fixture":
            event_id = f"EVT-BCC-{compact}-0001"
        else:
            event_id = f"EVT-BCC-{today_iso.replace('-', '')}-0001"

        # Build meeting info dict for source event
        meeting_info = {}
        for m in meetings:
            try:
                m_parts = m["date"].split("/")
                m_yr = m_parts[2] if len(m_parts[2]) == 4 else "20" + m_parts[2]
                m_iso = f"{m_yr}-{m_parts[0].zfill(2)}-{m_parts[1].zfill(2)}"
                if m_iso == iso_date:
                    meeting_info = m
                    break
            except:
                pass

        # Classify and normalize
        for i, item in enumerate(items):
            signal = classify_resident_impact(item["text"], item["title"])
            beat = map_beat(item["action_type"], signal, item["text"], item["title"])
            topics = map_topics(beat)

            item_id = f"SJC-BCC-{compact}-{i+1:04d}"
            dedupe_key = hashlib.sha256(
                f"sjc_bcc_calendar||{iso_date}||{item['number']}||{item['title'][:60]}".encode()
            ).hexdigest()[:16]

            interest_tags = ["community_trust"]
            if "development" in topics or "rezoning" in beat:
                interest_tags = ["development_watch", "property_values"]
            if "transportation" in beat:
                interest_tags = ["traffic_impact", "quality_of_life"]
            if "utilities" in beat:
                interest_tags = ["utility_impact", "cost_impact"]
            if "taxes" in beat:
                interest_tags = ["cost_impact", "community_trust"]

            excerpt = item["text"][:300]
            summary = f"Agenda item {item['number']}: {item['title'][:150]}"

            record = {
                "item_id": item_id,
                "title": item["title"][:200],
                "summary": summary,
                "source_id": "sjc_bcc_calendar",
                "source_url": CLERK_URL,
                "source_event_id": event_id,
                "source_published_at": iso_date,
                "discovered_at": now,
                "discovered_by": "hermes-sjc_bcc_calendar",
                "topics": topics,
                "communities": [],
                "geographic_scope": "county_wide",
                "urgency": "archival",
                "verification_status": "source_confirmed",
                "sensitivity": "low",
                "recommended_channels": ["website_review_queue", "weekly_brief_candidate"],
                "raw_excerpt": excerpt,
                "citation": {
                    "source_name": "St. Johns County Clerk of Court — Board Records",
                    "source_type": "government_website",
                    "accessed_at": now,
                    "url": CLERK_URL,
                },
                "review_status": "pending_review",
                "primary_topic": topics[0] if topics else "county_government",
                "interest_tags": interest_tags,
                "resident_relevance": {
                    "summary": f"BCC agenda item from {iso_date} meeting.",
                    "affected_audiences": ["residents", "homeowners"],
                    "why_it_matters": excerpt[:200],
                    "confidence": "high",
                    "inference_notes": "Directly from BCC agenda PDF published by Clerk of Court.",
                },
                "taxonomy_gap": None,
                "human_review_required": False,
                "created_at": now,
                "_dedupe_key": dedupe_key,
                "_meeting_date": iso_date,
                "_agenda_item_number": item["number"],
                "_action_type": item["action_type"],
                "_signal": signal,
                "_beat": beat,
                "_source_type": source_type,
            }
            all_items.append(record)

        # Build source event for this meeting
        item_ids = [r["item_id"] for r in all_items if r["_meeting_date"] == iso_date]
        if meeting_info:
            status = "extracted"
            extraction_status = f"{len(item_ids)} agenda items extracted from PDF."
            source_health = "accessible"
            if meeting_info.get("agenda_link_broken"):
                status = "extracted"
                extraction_status = f"{len(item_ids)} items extracted via expected URL (Clerk link was broken)."
                source_health = "accessible"
            event = build_meeting_event(
                meeting_date=meeting_date_str,
                meeting_info=meeting_info,
                item_ids=item_ids,
                status=status,
                extraction_status=extraction_status,
                source_health=source_health,
                notes="",
            )
            meeting_events.append(event)

    # 5. Write output
    intel_dir = os.path.join(BASE_INTEL_DIR, today_iso)
    os.makedirs(intel_dir, exist_ok=True)

    # Agenda items
    items_path = os.path.join(intel_dir, "sjc_bcc_agenda_items.yaml")
    output = {
        "source_id": "sjc_bcc_calendar",
        "fetched_at": now,
        "source_url": CLERK_URL,
        "total_items": len(all_items),
        "items": all_items,
    }
    with open(items_path, "w") as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"   Wrote {len(all_items)} agenda items to {items_path}")

    # Source events
    if meeting_events:
        write_source_events(meeting_events, today_iso, now)

    # Summary
    signals = {}
    beats = {}
    action_types = {}
    for item in all_items:
        signals[item["_signal"]] = signals.get(item["_signal"], 0) + 1
        beats[item["_beat"]] = beats.get(item["_beat"], 0) + 1
        action_types[item["_action_type"]] = action_types.get(item["_action_type"], 0) + 1

    print(f"\n  === Summary ===")
    print(f"  Total agenda items extracted: {len(all_items)}")
    print(f"  Source events created: {len(meeting_events)}")
    print(f"  By signal: {signals}")
    print(f"  By beat: {beats}")
    print(f"  By action type: {action_types}")

    # Show notable items
    print(f"\n  Notable resident-impact items:")
    for item in all_items:
        if item["_signal"] == "high_signal":
            print(f"    [{item['_beat']}] {item['title'][:100]}")

    print("\nDone.")


if __name__ == "__main__":
    main()

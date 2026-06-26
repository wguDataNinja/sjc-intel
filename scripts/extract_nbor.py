#!/usr/bin/env python3
"""
NBOR (Neighborhood Bill of Rights) structured extractor for SJC_Intel.

Fetches the public NBOR application page, parses structured HTML tables,
and outputs normalized records matching the intel_item schema and
resident-interest taxonomy.

Source: https://webapp.sjcfl.us/webnews/NBRscreend.aspx
"""
import re
import sys
import json
import yaml
import hashlib
import urllib.request
from html.parser import HTMLParser
from datetime import datetime, timezone

NBOR_URL = "https://webapp.sjcfl.us/webnews/NBRscreend.aspx"
USER_AGENT = "Mozilla/5.0 (SJC_Intel NBOR Extractor/1.0)"
OUTPUT_DIR = "data/intel_items/2026-06-08"
RAW_FIXTURE = "tests/fixtures/nbor_raw.html"


# ── Category classification ──────────────────────────────────────────────

def classify_category(title, description, section_raw):
    """Map NBOR items to resident-interest beat categories."""
    t = (title + " " + description).lower()

    # Application IDs — check these first since they're definitive
    # Rezonings
    if re.search(r'\bREZ\s+\d+', title) or "rezone" in t:
        return "rezoning_comp_plan_dri"

    # Comp plan amendments
    if re.search(r'\bCPA\b', title) or "comp plan" in t or "future land use" in t:
        return "rezoning_comp_plan_dri"

    # Zoning variances
    if re.search(r'\bZVAR\b', title) or re.search(r'\bPVZVAR\b', title) or "variance" in t:
        return "rezoning_comp_plan_dri"

    # PUD modifications
    if re.search(r'\bMAJMOD\b', title) or re.search(r'\bMINMOD\b', title) or "pud" in t:
        return "rezoning_comp_plan_dri"

    # Appeals
    if re.search(r'\bPLNAPPL\b', title) or "appeal" in t:
        return "rezoning_comp_plan_dri"

    # Special use permits
    if re.search(r'\bSUPMIN\b', title) or "special use" in t:
        return "site_plans_permits_construction"

    # Road closures / drainage (actual road work, not addresses)
    road_work_keywords = ["lane closure", "road closure", "drainage improvement",
                          "traffic", "right-of-way", "lane closures"]
    if any(w in t for w in road_work_keywords):
        return "roadwork_traffic"

    # Utility ROW permits — companies doing utility work
    utility_companies = ["comcast", "att", "jea", "iq fiber", "beaches energy", "fpl"]
    if any(c in t for c in utility_companies):
        return "utilities_water"

    # General construction / site work
    construction_keywords = ["bulkhead", "temp power", "geo tech", "pole replacement",
                             "new service", "cable", "fiber", "conduit", "span replacement"]
    if any(w in t for w in construction_keywords):
        return "site_plans_permits_construction"

    return "site_plans_permits_construction"


def classify_topic(beat):
    mapping = {
        "roadwork_traffic": ["transportation", "infrastructure"],
        "utilities_water": ["infrastructure", "environment"],
        "rezoning_comp_plan_dri": ["development", "county_government", "public_notices"],
        "site_plans_permits_construction": ["development", "infrastructure"],
    }
    return mapping.get(beat, ["development"])


def classify_urgency(category):
    if category == "ROW":
        return "ongoing"
    return "timely"  # meetings have specific dates


def classify_sensitivity(beat):
    if beat in ("rezoning_comp_plan_dri",):
        return "medium"
    return "low"


# ── HTML Parser ──────────────────────────────────────────────────────────

def fetch_page(url=None):
    """Fetch NBOR page via HTTP GET. Returns HTML string."""
    u = url or NBOR_URL
    req = urllib.request.Request(u, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_rows(html):
    """Parse NBOR HTML into list of raw record dicts."""
    # Locate data section
    start = html.find('<!--end Header row-->')
    end = html.find('Records per page')
    if start < 0 or end < 0:
        print("WARNING: Could not locate data section in HTML", file=sys.stderr)
        return []

    data_section = html[start:end]
    raw_rows = data_section.split('<hr class="mt-0">')

    records = []
    for raw in raw_rows:
        raw = raw.strip()
        if not raw or "col-sm-12 col-md-6" not in raw:
            continue

        # Extract title from <strong>
        titles = re.findall(r'<strong>(.*?)</strong>', raw)
        title = titles[0].strip() if titles else ""

        # Extract description (everything after <br /> following title)
        desc_match = re.search(r'</strong>\s*<br\s*/?>\s*(.*?)(?:<ul|<br\s*/?>\s*<br|<div)', raw, re.DOTALL)
        description = ""
        if desc_match:
            description = re.sub(r'<[^>]+>', ' ', desc_match.group(1)).strip()
            description = re.sub(r'\s+', ' ', description)

        # Extract PDF links
        pdfs = re.findall(r'href="([^"]+\.pdf[^"]*)"', raw)
        # Make PDF URLs absolute
        pdf_urls = []
        for p in pdfs:
            if p.startswith("http"):
                pdf_urls.append(p)
            elif p.startswith("vu.aspx"):
                pdf_urls.append(f"https://webapp.sjcfl.us/webnews/{p}")
            else:
                pdf_urls.append(f"https://webapp.sjcfl.us/webnews/{p}")

        # Map link
        map_url = ""
        map_match = re.search(r'href="([^"]*ViewMap[^"]*)"', raw)
        if map_match:
            map_url = map_match.group(1)

        # Extract columns from float-md-right elements
        cols = re.findall(r'class="float-md-right">\s*(.*?)\s*</p>', raw, re.DOTALL)
        cols = [re.sub(r'<[^>]+>', '', c).strip() for c in cols]

        district = cols[0] if len(cols) > 0 else ""
        category = cols[1] if len(cols) > 1 else ""
        date_str = cols[2] if len(cols) > 2 else ""

        # Extract application/permit number from title
        app_id = ""
        id_match = re.search(r'([A-Z]+\s*\d{10,})', title)
        if id_match:
            app_id = id_match.group(1)

        record = {
            "title": title,
            "description": description,
            "district": district,
            "category": category,
            "date": date_str,
            "pdf_urls": pdf_urls,
            "map_url": map_url,
            "app_id": app_id,
            "raw_text": re.sub(r'<[^>]+>', ' ', raw).strip(),
        }
        records.append(record)

    return records


def normalize_records(records, source="sjc_nbor_public_notices"):
    """Convert raw NBOR records to intel_item schema."""
    items = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now(timezone.utc).strftime("%Y%m%d")

    for i, rec in enumerate(records):
        if not rec["title"]:
            continue

        beat = classify_category(rec["title"], rec["description"], "")
        topics = classify_topic(beat)
        urgency = classify_urgency(rec["category"])
        sensitivity = classify_sensitivity(beat)
        is_row = rec["category"] == "ROW"
        is_hearing = "Meeting" in rec["category"]

        # Build summary
        if is_row:
            summary = f"ROW permit: {rec['title']} — {rec['description'][:150]}"
        elif is_hearing:
            summary = f"Public hearing: {rec['title']} — {rec['description'][:150]}"
        else:
            summary = f"{rec['title']} — {rec['description'][:150]}"

        # Build dedupe key
        dedupe_raw = f"{source}||{rec['category']}||{rec['app_id'] or rec['title']}||{rec['date']}"
        dedupe_key = hashlib.sha256(dedupe_raw.encode()).hexdigest()[:16]

        # Affected audience
        audiences = ["residents", "homeowners"]
        if is_row:
            audiences.append("commuters")
            audiences.append("nearby_residents")
        if beat == "rezoning_comp_plan_dri":
            audiences.extend(["homeowners", "prospective_movers"])

        # Interest tags
        tags = ["development_watch"]
        if beat == "roadwork_traffic":
            tags = ["traffic_impact", "quality_of_life"]
        elif beat == "utilities_water":
            tags = ["utility_impact", "quality_of_life"]

        item = {
            "item_id": f"SJC-NBOR-{today}-{i+1:04d}",
            "title": rec["title"],
            "summary": summary,
            "source_id": source,
            "source_url": NBOR_URL,
            "source_published_at": rec["date"] if rec["date"] else None,
            "discovered_at": now,
            "discovered_by": f"hermes-{source}",
            "topics": topics,
            "communities": [],
            "geographic_scope": "county_wide",
            "urgency": urgency,
            "verification_status": "source_confirmed",
            "sensitivity": sensitivity,
            "recommended_channels": ["website_review_queue", "weekly_brief_candidate"],
            "raw_excerpt": rec["description"][:300] if rec["description"] else rec["title"],
            "citation": {
                "source_name": "St. Johns County Neighborhood Bill of Rights",
                "source_type": "government_website",
                "accessed_at": now,
                "url": NBOR_URL,
            },
            "review_status": "pending_review",
            "primary_topic": topics[0] if topics else "development",
            "interest_tags": tags,
            "resident_relevance": {
                "summary": f"{'ROW permit' if is_row else 'Public hearing'} affecting St. Johns County residents.",
                "affected_audiences": audiences,
                "why_it_matters": rec["description"][:200] if rec["description"] else rec["title"],
                "confidence": "high",
                "inference_notes": "Directly from NBOR public notices application.",
            },
            "taxonomy_gap": None,
            "human_review_required": False,
            "created_at": now,
            "_dedupe_key": dedupe_key,
            "_category": rec["category"],
            "_beat": beat,
            "_app_id": rec["app_id"],
            "_pdf_urls": rec["pdf_urls"],
            "_map_url": rec["map_url"],
            "_district": rec["district"],
            "_raw_text": rec["raw_text"],
        }
        items.append(item)

    return items


# ── Output ───────────────────────────────────────────────────────────────

def write_output(items, html, records):
    """Write output files: intel_items YAML, raw fixture, and a summary."""
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Intel items YAML
    output = {
        "source_id": "sjc_nbor_public_notices",
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_url": NBOR_URL,
        "total_items": len(items),
        "items": items,
    }
    items_path = f"{OUTPUT_DIR}/sjc_nbor_public_notices.yaml"
    with open(items_path, "w") as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Wrote {len(items)} items to {items_path}")

    # Raw HTML fixture (already saved, update if live)
    if html:
        with open(RAW_FIXTURE, "w") as f:
            f.write(html)
        print(f"Updated raw fixture: {RAW_FIXTURE}")

    # Summary
    by_category = {}
    for r in records:
        cat = r["category"] or "unknown"
        by_category[cat] = by_category.get(cat, 0) + 1

    by_beat = {}
    for item in items:
        beat = item["_beat"]
        by_beat[beat] = by_beat.get(beat, 0) + 1

    print(f"\nRecords by NBOR category: {by_category}")
    print(f"Items by resident-interest beat: {by_beat}")
    print(f"Total normalized items: {len(items)}")


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    print("NBOR Extractor for SJC_Intel")
    print("=" * 50)

    # Fetch
    print("\n1. Fetching NBOR page...")
    html = fetch_page()
    print(f"   Fetched {len(html)} bytes")

    # Parse
    print("\n2. Parsing HTML rows...")
    records = parse_rows(html)
    print(f"   Found {len(records)} records")

    # Show some raw records
    for i, rec in enumerate(records[:3]):
        print(f"\n   Record {i+1}: {rec['title']}")
        print(f"     Category: {rec['category']}, Date: {rec['date']}, District: {rec['district']}")
        print(f"     Description: {rec['description'][:100]}...")
        if rec['pdf_urls']:
            print(f"     PDFs: {rec['pdf_urls']}")
        if rec['app_id']:
            print(f"     App ID: {rec['app_id']}")

    # Normalize
    print("\n3. Normalizing to intel_item schema...")
    items = normalize_records(records)
    print(f"   Generated {len(items)} normalized items")

    # Show sample
    if items:
        print(f"\n   Sample item 1:")
        print(f"     ID: {items[0]['item_id']}")
        print(f"     Title: {items[0]['title']}")
        print(f"     Beat: {items[0]['_beat']}")
        print(f"     Topics: {items[0]['topics']}")
        print(f"     Urgency: {items[0]['urgency']}")
        print(f"     Dedupe key: {items[0]['_dedupe_key']}")

    # Write
    print("\n4. Writing output files...")
    write_output(items, html, records)

    # Dedupe strategy
    print("\n5. Dedupe key strategy:")
    print("   Primary: source_id + category + app_id + date")
    print("   Fallback: source_id + category + normalized_title + date")
    print("   Final: SHA256 hash of raw row text")

    print("\nDone.")
    return items, records


if __name__ == "__main__":
    items, records = main()

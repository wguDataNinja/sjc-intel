"""Tests for the GitHub Pages deployment workflow (subpath + public-only guard)."""
from pathlib import Path

import yaml


def test_pages_workflow_exists():
    wf = Path("scripts").parent / ".github" / "workflows" / "pages.yml"
    assert wf.exists(), "pages.yml workflow must exist"


def test_pages_workflow_uses_official_actions_and_min_permissions():
    text = (Path("scripts").parent / ".github" / "workflows" / "pages.yml").read_text()
    for action in ("actions/checkout@", "actions/setup-python@",
                   "actions/upload-pages-artifact@", "actions/deploy-pages@"):
        assert action in text, f"expected official action {action}"
    # Minimum permissions: no broad `write-all`.
    assert "contents: read" in text
    assert "pages: write" in text
    assert "id-token: write" in text
    assert "workflow_dispatch" in text


def test_pages_uploads_only_site():
    text = (Path("scripts").parent / ".github" / "workflows" / "pages.yml").read_text()
    assert "path: site" in text
    # No internal/private material in the artifact.
    for forbidden in ("runtime", "reports", "registry", "adaptive_discovery",
                      "pending_proposals", "decisions.yaml", "accepted_state"):
        assert forbidden not in text.split("Upload Pages artifact")[1].split("Deploy to GitHub Pages")[0], (
            f"artifact should not reference {forbidden}")


def test_site_uses_relative_subpath_safe_links():
    """Under GitHub Pages project pages (https://user.github.io/sjc-intel/), the
    site must use relative links so the subpath prefix does not break routes."""
    import glob
    index = Path("scripts").parent / "site" / "index.html"
    if not index.exists():
        return  # site not built in this environment
    text = index.read_text()
    assert 'href="/' not in text, "absolute root href would break under a subpath"
    assert 'src="/' not in text, "absolute root src would break under a subpath"


def test_pages_guard_rejects_internal_artifacts():
    """The workflow's in-run guard (grep for internal paths under site/) mirrors
    the repository rule that site/ contains public output only."""
    site = Path("scripts").parent / "site"
    if not site.exists():
        return
    internal = []
    for root, _dirs, files in site.walk():
        for name in files:
            rel = (root / name).relative_to(site).as_posix()
            if any(tok in rel for tok in ("runtime/", "reports/", "registry/",
                                          "adaptive_discovery", "pending_proposals",
                                          "decisions.yaml", "accepted_state")):
                internal.append(rel)
    assert internal == [], f"internal artifacts found under site/: {internal}"

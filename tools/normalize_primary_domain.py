#!/usr/bin/env python3
"""Normalize West Coast Capital Mortgage to its canonical production domain.

Deploy mode updates the Netlify publish directory in-place.
Source mode also updates WCCM generators/workflows so future rebuilds do not
re-introduce the legacy long domain.
"""
from __future__ import annotations

import argparse
from pathlib import Path

OLD = "westcoastcapitalmortgage.com"
NEW = "westccmortgage.com"
CANONICAL = f"https://{NEW}"

DOMAIN_RULES = [
    f"https://{OLD}/* {CANONICAL}/:splat 301!",
    f"https://www.{OLD}/* {CANONICAL}/:splat 301!",
    f"https://www.{NEW}/* {CANONICAL}/:splat 301!",
    f"https://westccmtg.com/* {CANONICAL}/:splat 301!",
    f"https://www.westccmtg.com/* {CANONICAL}/:splat 301!",
    f"https://cawccmortgage.com/* {CANONICAL}/:splat 301!",
    f"https://www.cawccmortgage.com/* {CANONICAL}/:splat 301!",
    f"https://westccmortgage.netlify.app/* {CANONICAL}/:splat 301!",
]


def replace_domain(path: Path) -> int:
    if not path.is_file() or path.name == "_redirects":
        return 0
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0
    count = text.count(OLD)
    if count:
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")
    return count


def clean_redirects(path: Path) -> tuple[int, int]:
    """Keep first-match semantics, remove unreachable duplicates, and put host rules first."""
    if not path.exists():
        raise FileNotFoundError(path)

    original = path.read_text(encoding="utf-8").splitlines()
    unique_rules: list[str] = []
    seen_sources: set[str] = set()
    duplicate_count = 0

    alternate_hosts = {
        OLD,
        f"www.{OLD}",
        f"www.{NEW}",
        "westccmtg.com",
        "www.westccmtg.com",
        "cawccmortgage.com",
        "www.cawccmortgage.com",
        "westccmortgage.netlify.app",
    }

    for raw in original:
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split()
        if len(parts) < 3:
            continue
        source, target, status = parts[0], parts[1], parts[2]

        # Catch-all is rebuilt once, at the bottom.
        if status == "404" or source == "/*" and target == "/404.html":
            continue

        # Host-level rules are rebuilt once, at the top.
        if source.startswith("http://") or source.startswith("https://"):
            host = source.split("://", 1)[1].split("/", 1)[0].lower()
            if host in alternate_hosts:
                continue

        if source in seen_sources:
            duplicate_count += 1
            continue
        seen_sources.add(source)
        unique_rules.append(" ".join(parts[:3]))

    out = [
        "# West Coast Capital Mortgage — Netlify redirects",
        f"# Canonical host: {CANONICAL}",
        "",
        "# Alternate hosts -> canonical host",
        *DOMAIN_RULES,
        "",
        "# Retired URLs -> current consolidated pages (first-match order preserved)",
        *unique_rules,
        "",
        "# Catch-all must remain last",
        "/* /404.html 404",
        "",
    ]
    path.write_text("\n".join(out), encoding="utf-8")
    return len(unique_rules), duplicate_count


def text_files_under(root: Path):
    if not root.exists():
        return
    for p in root.rglob("*"):
        if p.is_file():
            yield p


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        action="store_true",
        help="also normalize WCCM generator/workflow sources in the repository",
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="normalize only the Netlify publish directory (default behavior)",
    )
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    publish = repo / "wccm-corporate"
    if not publish.exists():
        raise SystemExit(f"Publish directory not found: {publish}")

    replacement_count = 0
    changed_files = 0

    for p in text_files_under(publish):
        n = replace_domain(p)
        if n:
            replacement_count += n
            changed_files += 1

    if args.source:
        candidates = [
            repo / "gen_city_pages.py",
            repo / "gen_geo_pages.py",
            repo / "flagship_detail.py",
            repo / "flagship_data.json",
            repo / "ping_indexnow.py",
        ]
        candidates.extend((repo / "tools").glob("*.py"))
        candidates.extend((repo / ".github" / "workflows").glob("*.yml"))
        candidates.extend((repo / ".github" / "workflows").glob("*.yaml"))
        for p in candidates:
            if p.resolve() == Path(__file__).resolve():
                continue
            n = replace_domain(p)
            if n:
                replacement_count += n
                changed_files += 1

    rule_count, duplicate_count = clean_redirects(publish / "_redirects")

    # Hard guard: no legacy long-domain SEO references may remain in the
    # published site except the intentional source host in _redirects.
    leftovers = []
    for p in text_files_under(publish):
        if p.name == "_redirects":
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if OLD in text:
            leftovers.append(str(p.relative_to(repo)))
    if leftovers:
        raise SystemExit("Old canonical domain remains in: " + ", ".join(leftovers))

    print(
        f"Canonical domain normalized: {replacement_count} replacements in "
        f"{changed_files} files; redirects={rule_count}; duplicates_removed={duplicate_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""One-shot: extract assets from docs/16-facilitator-toolkit-k7p2nx.html into
toolkit/ifp/<NN>-<slug>.md. Each asset becomes one markdown file with:

    # Title
    > Description

    <copyable body text from the <textarea readonly>>

Idempotent — re-running overwrites files.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "docs" / "16-facilitator-toolkit-k7p2nx.html"
OUT = REPO_ROOT / "toolkit" / "ifp"


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return re.sub(r"-+", "-", s).strip("-")[:60] or "asset"


def main() -> int:
    if not SRC.is_file():
        print(f"missing source: {SRC}", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")
    assets = soup.find_all("div", class_="asset")
    written = skipped = 0
    for i, asset in enumerate(assets, 1):
        h3 = asset.find("h3")
        if not h3:
            skipped += 1
            continue
        title = h3.get_text(" ", strip=True)
        meta_el = asset.find("p", class_="asset-meta")
        description = meta_el.get_text(" ", strip=True) if meta_el else ""
        ta = asset.find("textarea")
        if not ta:
            print(f"  [{i:02d}] {title!r}: no textarea (skipped)", file=sys.stderr)
            skipped += 1
            continue
        body = html.unescape(ta.decode_contents()).strip("\n").rstrip()
        filename = f"{i:02d}-{slugify(title)}.md"
        target = OUT / filename
        content = f"# {title}\n"
        if description:
            content += f"> {description}\n"
        content += f"\n{body}\n"
        target.write_text(content, encoding="utf-8")
        written += 1
        print(f"  [{i:02d}] {filename}  ({len(body)} chars)")
    print(f"wrote {written}, skipped {skipped} of {len(assets)} blocks")
    return 0


if __name__ == "__main__":
    sys.exit(main())

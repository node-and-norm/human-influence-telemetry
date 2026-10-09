#!/usr/bin/env python3
"""Retrieve a bounded OGL source packet; never call a model or infer HIT findings.

Extraction normalizes HTML whitespace and decodes character references. All
selected paragraphs retain their words, punctuation and order. Live retrieval
can change; hashes identify retrieved bytes, not historical publication copies.
"""

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research/strengthening/jev-review-001/sources.json"
LICENCE_URL = "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
SOURCES = (
    ("OFQ-01", "Ofqual", "https://www.gov.uk/government/news/statement-from-roger-taylor-chair-ofqual"),
    ("OFQ-02", "Ofqual", "https://www.gov.uk/government/publications/ofqual-annual-report-for-the-period-1-april-2020-to-31-march-2021/annual-report-and-accounts-2020-to-2021"),
    ("OFQ-03", "Ofqual", "https://www.gov.uk/government/publications/ofquals-regulatory-burden-statement/regulatory-burden-statement-april-2021"),
    ("DFE-01", "Department for Education", "https://www.gov.uk/government/publications/coronavirus-covid-19-cancellation-of-gcses-as-and-a-levels-in-2020/coronavirus-covid-19-cancellation-of-gcses-as-and-a-levels-in-2020"),
)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
BLOCKS = {"p", "h2", "h3", "h4", "h5", "li"}


class Element:
    def __init__(self, tag, attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Element):
                yield from child.walk()

    def text(self):
        def chunks(node):
            if isinstance(node, str):
                return node
            if node.tag == "br":
                return " "
            return "".join(chunks(child) for child in node.children)
        return re.sub(r"\s+", " ", chunks(self)).strip()


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Element("document")
        self.stack = [self.root]
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        element = Element(tag, attrs)
        self.stack[-1].children.append(element)
        if tag not in VOID:
            self.stack.append(element)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def retrieve(url):
    request = urllib.request.Request(url, headers={"User-Agent": "HIT-source-retrieval/0.1 (public-document research; no authentication)", "Accept-Encoding": "identity"})
    with urllib.request.urlopen(request, timeout=45) as response:
        raw = response.read()
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
    return raw, final_url, content_type, datetime.now(timezone.utc).isoformat(timespec="seconds")


def govspeak_blocks(document):
    containers = [node for node in document.root.walk() if "gem-c-govspeak" in node.attrs.get("class", "").split()]
    if not containers:
        raise ValueError("missing GOV.UK prose container")
    container = max(containers, key=lambda node: len(node.text()))
    output = []
    def visit(node):
        if node.tag in BLOCKS:
            if node.text():
                output.append({"tag": node.tag, "anchor": node.attrs.get("id"), "text": node.text()})
            return
        for child in node.children:
            if isinstance(child, Element):
                visit(child)
    visit(container)
    return output


def section(blocks, start, end):
    starts = [i for i, block in enumerate(blocks) if block["text"] == start]
    if len(starts) != 1:
        raise ValueError(f"section start must occur once: {start}")
    start_index = starts[0]
    ends = [i for i, block in enumerate(blocks) if i > start_index and block["text"] == end]
    if not ends:
        raise ValueError(f"missing section end: {end}")
    return list(range(start_index + 1, ends[0]))


def selections(source_id, blocks):
    if source_id == "OFQ-01":
        if len(blocks) != 6 or any(block["tag"] != "p" for block in blocks):
            raise ValueError("Chair statement no longer consists of six paragraphs")
        return [("OFQ-01-statement", "Complete statement body, paragraphs 1–6 after the image", list(range(6)))]
    if source_id == "OFQ-02":
        board = [i for i, block in enumerate(blocks) if block["text"].startswith("The Ofqual Board is the legal authority")]
        if len(board) != 1:
            raise ValueError("Board authority paragraph must occur once")
        directions = section(blocks, "Secretary of State Directions", "Board and executive team response")
        return [
            ("OFQ-02-advice", "Regulating GCSE, AS and A levels in response to Covid-19 > External Advisory Group and quality assurance; complete subsection before Communications and engagement", section(blocks, "External Advisory Group and quality assurance", "Communications and engagement")),
            ("OFQ-02-board", "Governance statement > Overview, first paragraph; then Secretary of State Directions, complete subsection before Board and executive team response. These are two non-contiguous excerpts; intervening overview text and figure are omitted.", board + [directions[0] - 1] + directions),
            ("OFQ-02-results", "Regulating GCSE, AS and A levels in response to Covid-19 > Public confidence and results days; complete subsection before Outcomes", section(blocks, "Public confidence and results days", "Outcomes")),
        ]
    if source_id == "OFQ-03":
        return [("OFQ-03-direction", "2.3 Monitoring awarding and results in 2020; complete subsection before 2.4 Engagement with awarding organisations", section(blocks, "2.3 Monitoring awarding and results in 2020", "2.4 Engagement with awarding organisations"))]
    return [
        ("DFE-01-results", "Results and university entry in 2020 > Results days; complete subsection before Universities, colleges and sixth forms and grade acceptance", section(blocks, "Results days", "Universities, colleges and sixth forms and grade acceptance")),
        ("DFE-01-external", "External candidates in 2020 > Arrangements for home-educated students and other external candidates; complete subsection before Vocational and technical qualifications (VTQs) in 2020", section(blocks, "Arrangements for home-educated students and other external candidates", "Vocational and technical qualifications (VTQs) in 2020")),
        ("DFE-01-admissions", "Results and university entry in 2020 > Universities, colleges and sixth forms and grade acceptance; complete subsection before Students participating in the autumn series of exams", section(blocks, "Universities, colleges and sixth forms and grade acceptance", "Students participating in the autumn series of exams")),
        ("DFE-01-appeals", "Arrangements for summer 2020 appeals plus the complete following Bias and discrimination subsection; ends before Arrangements for autumn series of GCSE, A and AS level exams in 2020", section(blocks, "Arrangements for summer 2020 appeals", "Arrangements for autumn series of GCSE, A and AS level exams in 2020")),
    ]


def source_record(source_id, publisher, url):
    raw, final_url, content_type, retrieved_at = retrieve(url)
    if final_url != url or "text/html" not in content_type:
        raise ValueError(f"source moved or changed content type: {source_id}")
    document = Document(raw.decode("utf-8"))
    nodes = list(document.root.walk())
    metadata = {node.attrs.get("name"): node.attrs.get("content") for node in nodes if node.tag == "meta" and node.attrs.get("name") in {"govuk:first-published-at", "govuk:public-updated-at", "govuk:updated-at", "govuk:primary-publishing-organisation", "govuk:withdrawn"}}
    if metadata.get("govuk:primary-publishing-organisation") != publisher:
        raise ValueError(f"publisher changed: {source_id}")
    licence_links = [node.attrs["href"] for node in nodes if node.tag == "a" and "open-government-licence/version/3" in node.attrs.get("href", "")]
    if not licence_links:
        raise ValueError(f"no OGL v3 link: {source_id}")
    notices = [node for node in nodes if "gem-c-notice" in node.attrs.get("class", "").split()]
    withdrawn = metadata.get("govuk:withdrawn") == "withdrawn"
    notice_text = "\n\n".join(node.text() for node in notices) or None
    withdrawn_at = next((node.attrs.get("datetime") for notice in notices for node in notice.walk() if node.tag == "time"), None)
    if withdrawn != (source_id == "DFE-01") or withdrawn and not (notice_text and withdrawn_at):
        raise ValueError(f"withdrawal status changed or notice missing: {source_id}")
    blocks = govspeak_blocks(document)
    passages = []
    for passage_id, locator, indices in selections(source_id, blocks):
        text = "\n\n".join(blocks[i]["text"] for i in indices)
        passages.append({"id": passage_id, "locator": locator, "text": text, "text_sha256": digest(text.encode("utf-8")), "govspeak_block_indices_zero_based": indices, "blocks": [{"index_zero_based": i, **blocks[i]} for i in indices]})
    first_published = metadata["govuk:first-published-at"]
    public_updated = metadata["govuk:public-updated-at"]
    return {
        "id": source_id,
        "url": url,
        "title": next(node.text() for node in nodes if node.tag == "h1"),
        "publisher": publisher,
        "publication_date": first_published[:10],
        "updated_date": public_updated[:10],
        "retrieved_at": retrieved_at,
        "retrieved_local": datetime.fromisoformat(retrieved_at).astimezone(ZoneInfo("America/New_York")).isoformat(),
        "govuk_metadata": metadata,
        "date_basis": "publication_date uses govuk:first-published-at; updated_date uses govuk:public-updated-at. govuk:updated-at is separate technical metadata, not an authenticated date of substantive wording change.",
        "withdrawn": withdrawn,
        "withdrawn_at": withdrawn_at,
        "withdrawal_notice": notice_text,
        "license": {"name": "Open Government Licence v3.0", "url": LICENCE_URL, "observed_page_links": sorted(set(licence_links)), "attribution": f"Source: {publisher}, GOV.UK. Contains public sector information licensed under the Open Government Licence v3.0.", "scope": "Selected government-authored prose only. Logos, images, third-party linked documents and third-party rights are excluded. No endorsement is implied."},
        "retrieval": {"method": "HTTPS GET without authentication; UTF-8 HTML; no browser script execution", "final_url": final_url, "content_type": content_type, "raw_body_bytes": len(raw), "raw_body_sha256": digest(raw), "raw_html_retained": False, "hash_limit": "Raw response hashes include page markup and may change without prose changes. They identify this retrieval, not a publication-day copy."},
        "source_independence": "Institutional primary self-report. Ofqual sources share one publisher; DfE is a separate publisher involved in the same response. Neither establishes independently verified institutional outcomes.",
        "passages": passages,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--inspect", action="store_true", help="print selected source passages without writing")
    mode.add_argument("--write", action="store_true", help="create a fresh derived JSON packet; never overwrite an existing file")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.write and args.output.exists():
        raise SystemExit("Refusing to overwrite a retained packet. Use a new --output path and review any change.")
    licence_raw, licence_final_url, _, licence_retrieved_at = retrieve(LICENCE_URL)
    licence_text = Document(licence_raw.decode("utf-8")).root.text()
    for phrase in ("copy, publish, distribute and transmit", "Contains public sector information licensed under the Open Government Licence v3.0.", "Non-endorsement", "third party rights"):
        if phrase not in licence_text:
            raise ValueError(f"licence verification phrase missing: {phrase}")
    packet = {
        "packet_id": "HIT-JEV-REVIEW-001-SOURCES",
        "scope": "Nine selected primary-source passages from four GOV.UK HTML documents. This advisory-model rehearsal excludes OCR-01 and OFQ-04 and is not the full six-document HIT-SOLO-002 packet.",
        "selection_author": "OpenAI Codex, assistant-prepared under maintainer authorization; source selection is not independent human review",
        "extraction": "Python standard-library HTMLParser; decode HTML character references; collapse each HTML paragraph/list-item/heading's whitespace; retain original words, punctuation and order; separate retained blocks with two newlines. No paraphrasing, OCR, linked-document extraction or scoring.",
        "license_verification": {"url": licence_final_url, "retrieved_at": licence_retrieved_at, "raw_body_sha256": digest(licence_raw), "observed_reuse_permission": "OGL v3.0 permits copying and distribution with attribution, subject to stated exemptions and non-endorsement.", "attribution": "Contains public sector information licensed under the Open Government Licence v3.0."},
        "sources": [source_record(*source) for source in SOURCES],
    }
    if args.inspect:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(packet, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        print(json.dumps({"output": str(args.output), "sources": len(packet["sources"]), "passages": [passage["id"] for source in packet["sources"] for passage in source["passages"]]}))


if __name__ == "__main__":
    main()

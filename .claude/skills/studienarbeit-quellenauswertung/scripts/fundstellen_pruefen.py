"""Prüft jede Fundstelle wörtlich am umgewandelten Quelltext und korrigiert belegte Seiten.

Aufruf:
  uv run fundstellen_pruefen.py 02-quellen/fundstellen/Fundstellen_<kurzname>.md 02-quellen/markdown/<kurzname>.md

Schreibt pro Stelle die Zeilen „Seite:" und „Check:" zurück. Exit 1, wenn mindestens
ein Zitat nicht gefunden wurde.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from seiten import parse_pages  # noqa: E402

QUOTE_CHARS = "„“”\"‚‘’'«»"
STELLE_RE = re.compile(r"^### Stelle\b", re.MULTILINE)
SEITE_RE = re.compile(r"^(\s*)(?:S\.\s*)?(\d+|\?)\s*\(PDF\s*(\d+)\)")
MIN_WORDS, MIN_CHARS = 5, 30  # kürzere Zitate passen fast überall und beweisen nichts
FOOTNOTE_RE = re.compile(r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+|\[\^\d+\]|\^\d+|(?<=[^\W\d_])\d{1,3}\b")
ELLIPSIS_RE = re.compile(r"…|\.\.\.")
CHECK_TEXT = {
    "belegt": "✅ belegt",
    "nicht-gefunden": "❌ nicht gefunden [ZITAT PRÜFEN]",
    "mehrdeutig": "⚠️ steht auf mehreren Seiten, keine davon passt zur Angabe [SEITE PRÜFEN]",
    "zu-kurz": "❌ zu kurz zum Prüfen (mindestens 5 Wörter) [ZITAT PRÜFEN]",
    "auslassung": "❌ Auslassung […] nicht prüfbar, als zwei Stellen anlegen [ZITAT PRÜFEN]",
    "format": "❌ Zitat nicht in einer Zeile oder ohne schließendes Anführungszeichen [ZITAT PRÜFEN]",
}
FAILED = {"nicht-gefunden", "zu-kurz", "auslassung", "format"}
OPEN_QUOTES, CLOSE_QUOTES = "„\"“«‚", "“”\"»‘’"


def normalize(text: str, strip_markers: bool = False) -> str:
    """Vergleichsform: Ligaturen auflösen, Trennungen, Zeichen, Leerraum glätten.

    strip_markers nur für den Quelltext: entfernt Fußnotenzeichen, damit ein Zitat
    ohne Fußnotenzeichen passt. Das Zitat selbst wird nie so beschnitten, sonst
    passte „Stufe4" auf „Stufe3".
    """
    if strip_markers:
        text = FOOTNOTE_RE.sub("", text)
    text = unicodedata.normalize("NFKC", text)
    # Bindestrich zwischen Wortzeichen fällt auf beiden Seiten weg: Trennungen („representa- tion",
    # auch am Zeilenende) und echte Bindestriche („pre-train") vergleichen sich so gleich
    text = re.sub(r"(?<=\w)-\s*(?=\w)", "", text)
    text = text.translate(str.maketrans("", "", QUOTE_CHARS + "*_#>"))
    return re.sub(r"\s+", " ", text).strip().lower()


def locate_all(quote: str, pages: list[tuple[int, str, str]]) -> list[tuple[int, str]]:
    """Alle Seiten (PDF, gedruckt) mit dem Zitat; erst einzeln, sonst über Seitengrenzen."""
    hits = [(pdf, printed) for pdf, printed, text in pages if _contains(text, quote)]
    if hits:
        return hits
    return [
        (pdf, printed)
        for (pdf, printed, text), (_, _, following) in zip(pages, pages[1:])
        if _contains(text + "\n" + following, quote)
    ]


def _contains(source: str, quote: str) -> bool:
    """Zitat steht wörtlich im Quelltext, mit oder ohne dessen Fußnotenzeichen."""
    needle = normalize(quote)
    return needle in normalize(source) or needle in normalize(source, strip_markers=True)


def locate(quote: str, pages: list[tuple[int, str, str]]) -> tuple[int, str] | None:
    """Erste Seite mit dem Zitat (für einfache Abfragen)."""
    hits = locate_all(quote, pages)
    return hits[0] if hits else None


def _field_re(name: str) -> re.Pattern[str]:
    # Wert = Rest der Zeile plus eingerückte Folgezeilen; alles danach (Notizen, ---) bleibt unberührt
    return re.compile(rf"^- {name}:[ \t]*(.*(?:\n[ \t]+\S.*)*)", re.MULTILINE)


def _field(block: str, name: str) -> str | None:
    """Feldwert, auch wenn er über eingerückte Folgezeilen umbrochen ist."""
    match = _field_re(name).search(block)
    return " ".join(match.group(1).split()) if match else None


def _set_field(block: str, name: str, value: str) -> str:
    return _field_re(name).sub(lambda _: f"- {name}: {value}", block, count=1)


def _judge(zitat: str, seite_alt: str, pages: list[tuple[int, str, str]], full_text: str) -> tuple[str, str]:
    """Status und neue Seitenangabe für eine Stelle."""
    if ELLIPSIS_RE.search(zitat):
        return "auslassung", seite_alt
    if len(normalize(zitat).split()) < MIN_WORDS or len(normalize(zitat)) < MIN_CHARS:
        return "zu-kurz", seite_alt
    if not pages:  # ohne Seitenmarken (Word, EPUB, OCR): nur Wortlaut, Seitenzahl nie bestätigen
        if not _contains(full_text, zitat):
            return "nicht-gefunden", seite_alt
        has_page = re.search(r"(?:^|\bS\.|\bp\.|\bSeite)\s*\d", seite_alt.strip())
        return "belegt", ("[SEITE PRÜFEN]" if has_page else seite_alt)
    hits = locate_all(zitat, pages)
    if not hits:
        return "nicht-gefunden", seite_alt
    claimed = SEITE_RE.match(seite_alt)
    for pdf, printed in hits:  # Angabe passt zu einem Fundort: behalten
        if claimed and ((printed != "?" and claimed.group(2) == printed) or
                        (printed == "?" and claimed.group(3) == str(pdf))):
            return "belegt", (f"{printed} (PDF {pdf})" if printed != "?" else f"[SEITE PRÜFEN] (PDF {pdf})")
    if len(hits) > 1:
        return "mehrdeutig", "[SEITE PRÜFEN] (PDF " + ", ".join(str(pdf) for pdf, _ in hits) + ")"
    pdf, printed = hits[0]
    if printed == "?":
        return "belegt", f"[SEITE PRÜFEN] (PDF {pdf})"
    return "andere-seite", f"{printed} (PDF {pdf})"


TAIL_RE = re.compile(r"(?<=[“”\"»‘’])\s*(?:\([^)]*\))?\s*[.,;:]?\s*$")


def _clean_quote(value: str) -> str:
    """Satzzeichen oder Klammerzusatz nach dem schließenden Anführungszeichen entfernen."""
    return TAIL_RE.sub("", value.strip())


def _bad_quote_format(block: str) -> bool:
    """Zitat-Zeile, die nicht sauber endet: lieber ablehnen als nur die erste Zeile prüfen."""
    lines = block.splitlines()
    idx = next((i for i, line in enumerate(lines) if line.startswith("- Zitat:")), None)
    if idx is None:
        return False
    value = _clean_quote(lines[idx][len("- Zitat:"):])
    nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
    continues = nxt.strip() and not nxt.startswith(("- ", "#", "---"))
    unclosed = value[:1] in OPEN_QUOTES and value[-1:] not in CLOSE_QUOTES
    return bool(continues or unclosed)


def _check_block(block: str, pages: list[tuple[int, str, str]], full_text: str) -> tuple[str, dict]:
    nr = re.match(r"### Stelle\s*(\S*)", block)
    zitat = _clean_quote(_field(block, "Zitat") or "").strip(QUOTE_CHARS + " ")
    seite_alt = _field(block, "Seite") or ""
    if _bad_quote_format(block):
        status, seite_neu = "format", seite_alt
    else:
        status, seite_neu = _judge(zitat, seite_alt, pages, full_text) if zitat else ("nicht-gefunden", seite_alt)
    if status == "andere-seite":
        old = SEITE_RE.match(seite_alt)
        check = f"⚠️ korrigiert von S. {old.group(2) if old else seite_alt}"
    else:
        check = CHECK_TEXT[status]
    block = _set_field(block, "Seite", seite_neu)
    block = _set_field(block, "Check", check)
    result = {"nr": nr.group(1) if nr else "?", "status": status, "seite_alt": seite_alt, "seite_neu": seite_neu}
    return block, result


def check_file(fundstellen: Path, markdown: Path) -> list[dict]:
    """Alle Stellen einer Fundstellen-Datei prüfen und das Ergebnis zurückschreiben."""
    full_text = markdown.read_text(encoding="utf-8")
    pages = parse_pages(full_text)
    text = fundstellen.read_text(encoding="utf-8")
    starts = [m.start() for m in STELLE_RE.finditer(text)]
    if not starts:
        return []
    head, blocks = text[: starts[0]], [text[a:b] for a, b in zip(starts, starts[1:] + [len(text)])]
    results, new_blocks = [], []
    for block in blocks:
        new_block, result = _check_block(block, pages, full_text)
        new_blocks.append(new_block)
        results.append(result)
    fundstellen.write_text(head + "".join(new_blocks), encoding="utf-8")
    return results


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print(__doc__)
        return 2
    results = check_file(Path(args[0]), Path(args[1]))
    belegt = sum(r["status"] == "belegt" for r in results)
    print(f"{len(results)} Stellen: {belegt} belegt, {len(results) - belegt} mit Hinweis")
    for r in results:
        if r["status"] != "belegt":
            print(f"  Stelle {r['nr']}: {r['status']} ({r['seite_alt']} -> {r['seite_neu']})")
    return 1 if any(r["status"] in FAILED for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())

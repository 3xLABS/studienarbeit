"""Wandelt alle Quellen in 02-quellen/dateien/ lokal in Markdown um.

PDFs werden Seite für Seite umgewandelt, damit jede Stelle ihre Seite behält. Die
gedruckte Seitenzahl kommt aus Kopf-/Fußzeilen (Rohtext via pypdf, weil anydoc
diese entfernt) oder aus dem Seitenbereich im Recherche-Protokoll.

Aufruf:
  uv run --with firecrawl-anydoc --with pypdf quellen_umwandeln.py 02-quellen [--ocr Datei.pdf ...]
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from seiten import _parse_range as _range_bounds  # noqa: E402
from seiten import assign_printed, offset_from_range, render_marked, render_pages  # noqa: E402

UMLAUTE = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "ae", "Ö": "oe", "Ü": "ue"})
INDEX_KEYS = ["datei", "kurzname", "format", "seiten", "versatz_quelle", "bereich", "status"]
SUPPORTED = {
    ".pdf", ".doc", ".docx", ".docm", ".odt", ".rtf", ".epub", ".ppt", ".pptx",
    ".odp", ".xls", ".xlsx", ".ods", ".csv",
}


def _slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.translate(UMLAUTE)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def kurzname(filename: str, taken: set[str]) -> str:
    """Stabiler, eindeutiger Dateiname ohne Endung, z. B. 'mueller-2021-risiko'."""
    base = _slug(Path(filename).stem) or "quelle"
    name, n = base, 2
    while name in taken:
        name, n = f"{base}-{n}", n + 1
    return name


def _first_author(autor: str) -> str:
    """Nachname des Erstautors aus 'Schmidt, A.', 'A. Schmidt' oder 'Weber & Lee'."""
    first = re.split(r"\s*(?:&|;| und | and | et al\.?)\s*", autor.strip())[0]
    if "," in first:
        return first.split(",")[0].strip()
    words = first.split()
    return words[-1] if words else ""


def load_recherche(quellen_dir: Path) -> list[dict]:
    """Quellenzeilen aus allen Recherche-Protokollen (Tabellen mit Spalte 'Autor')."""
    rows: list[dict] = []
    for path in sorted(quellen_dir.glob("Recherche_*.md")):
        header: list[str] | None = None
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip().startswith("|"):
                header = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if header is None:
                header = [c.lower() for c in cells]
                continue
            if set(line) <= set("|-: "):
                continue
            row = dict(zip(header, cells))
            if row.get("autor") and row.get("jahr"):
                row["schluessel"] = f"{_slug(_first_author(row['autor']))}-{_slug(row['jahr'])}"
                rows.append(row)
    return rows


def _candidates(name: str, rows: list[dict]) -> list[dict]:
    """Protokollzeilen, deren Schlüssel 'nachname-jahr' am Anfang des Kurznamens steht."""
    return [r for r in rows if name == r["schluessel"] or name.startswith(r["schluessel"] + "-")]


def _pdf_pages(path: Path) -> tuple[list[str], list[str]]:
    """Pro Seite: anydoc-Markdown (Inhalt) und pypdf-Rohtext (für Seitenzahlen)."""
    import anydoc
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(path))
    contents, raws = [], []
    for page in reader.pages:
        raws.append(page.extract_text() or "")
        writer = PdfWriter()
        writer.add_page(page)
        buf = io.BytesIO()
        writer.write(buf)
        try:
            contents.append(anydoc.to_markdown_bytes(buf.getvalue(), "pdf"))
        except anydoc.ConvertError:
            contents.append("")  # leere Seite (z. B. Vakatseite): Seite bleibt mit Marke stehen
    return contents, raws


def convert_file(path: Path, page_range: str | None, ocr: bool) -> tuple[str, dict]:
    """Eine Quelle umwandeln. Liefert Markdown und Infos für den Index."""
    import anydoc

    info = {"format": path.suffix.lower().lstrip("."), "seiten": "-", "versatz_quelle": "ohne-seiten", "status": "ok"}
    try:
        if path.suffix.lower() != ".pdf":
            return anydoc.to_markdown(str(path)), info
        try:
            anydoc.to_markdown(str(path))  # erkennt Scans für das ganze Dokument
        except anydoc.NeedsOcrError:
            if not ocr:
                info["status"] = "braucht-ocr"
                return "", info
            info["versatz_quelle"] = "unbekannt"
            return anydoc.to_markdown(str(path), ocr="hosted"), info
        contents, raws = _pdf_pages(path)
        info["seiten"] = str(len(contents))
        offset = offset_from_range(len(contents), page_range)
        if offset is not None:  # Länge passt exakt zum Seitenbereich: der ist der stärkere Beleg …
            header = assign_printed(len(contents), None, raws)
            conflict = any(p != "?" and int(p) not in (i + 1, i + 1 + offset) for i, p in enumerate(header))
            if conflict:  # … außer die Kopfzeilen sagen klar etwas anderes (Tippfehler im Protokoll?)
                info["versatz_quelle"] = "konflikt"
                return render_pages(contents, None), info
            info["versatz_quelle"] = "crossref"
            return render_pages(contents, offset, raws, page_range), info
        printed = assign_printed(len(contents), None, raws)  # Kopfzeilen, abschnittsweise
        rng = _range_bounds(page_range)
        if rng:  # z. B. Datenbank-Ausdruck "Page 3 of 12" bei Zeitschriftenseiten 320-331
            printed = [p if p == "?" or rng[0] <= int(p) <= rng[1] else "?" for p in printed]
        if any(n != "?" for n in printed):
            info["versatz_quelle"] = "kopfzeile"
            return render_marked(contents, printed), info
        info["versatz_quelle"] = "unbekannt"
        return render_pages(contents, None), info
    except (anydoc.ConvertError, OSError) as err:
        info["status"] = f"fehler: {err}"
        return "", info


def _write_index(out_dir: Path, entries: list[dict], missing: list[dict]) -> None:
    lines = [
        "# Quellen-Index", "",
        "| Datei | Kurzname | Format | Seiten | Versatz | Bereich | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    lines += ["| " + " | ".join(str(e[k]) for k in INDEX_KEYS) + " |" for e in entries]
    if missing:
        lines += ["", "## Ohne Datei", "", "| Autor | Jahr | Titel | Status |", "|---|---|---|---|"]
        lines += [f"| {r['autor']} | {r['jahr']} | {r.get('titel', '')} | fehlt |" for r in missing]
    (out_dir / "_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quellen_dir", type=Path)
    parser.add_argument("--ocr", nargs="*", default=[], help="Dateinamen, die per Firecrawl-OCR umgewandelt werden dürfen")
    args = parser.parse_args(argv)

    src_dir, out_dir = args.quellen_dir / "dateien", args.quellen_dir / "markdown"
    if not src_dir.is_dir():
        print(f"Ordner fehlt: {src_dir}")
        return 1
    out_dir.mkdir(exist_ok=True)
    rows = load_recherche(args.quellen_dir)
    previous = _previous_index(out_dir)
    files = sorted(p for p in src_dir.iterdir() if p.suffix.lower() in SUPPORTED)
    # Bekannte Dateien behalten ihren Kurznamen, sonst klaut eine neue Datei ihn (und ihre Fundstellen)
    names = {p.name: previous[p.name]["kurzname"] for p in files if p.name in previous}
    taken = set(names.values())
    for path in files:
        if path.name not in names:
            names[path.name] = kurzname(path.name, taken)
            taken.add(names[path.name])

    matched: set[int] = set()
    entries: list[dict] = []
    for path in files:
        name = names[path.name]
        candidates = _candidates(name, rows)
        matched.update(id(r) for r in candidates)
        # Seitenbereich nur bei eindeutiger Zuordnung, sonst lieber keine Seitenzahl als eine falsche
        page_range = candidates[0].get("seiten") if len(candidates) == 1 else None
        bereich = page_range or "-"
        target = out_dir / f"{name}.md"
        old = previous.get(path.name)
        if (target.exists() and target.stat().st_mtime >= path.stat().st_mtime and old
                and old["bereich"] == bereich and old["status"] == "ok"):
            entries.append(old)
            continue
        markdown, info = convert_file(path, page_range, path.name in args.ocr)
        if markdown:
            target.write_text(markdown, encoding="utf-8")
        entries.append({"datei": path.name, "kurzname": name, "bereich": bereich, **info})

    missing = [r for r in rows if id(r) not in matched]
    _write_index(out_dir, entries, missing)

    print(f"{len(entries)} Dateien verarbeitet, Index: {out_dir / '_index.md'}")
    for e in entries:
        if e["versatz_quelle"] == "konflikt":
            print(f"  {e['datei']}: Seitenbereich im Recherche-Protokoll widerspricht den Kopfzeilen, bitte prüfen")
        elif e["status"] != "ok" or e["versatz_quelle"] == "unbekannt":
            print(f"  {e['datei']}: {e['status']}, Versatz {e['versatz_quelle']}")
    for r in missing:
        print(f"  fehlt: {r['autor']} ({r['jahr']}) {r.get('titel', '')}")
    return 0


def _previous_index(out_dir: Path) -> dict[str, dict]:
    """Zeilen des letzten Index, nach Dateiname."""
    index = out_dir / "_index.md"
    if not index.exists():
        return {}
    result = {}
    for line in index.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == len(INDEX_KEYS) and cells[0] not in ("Datei", "---"):
            result[cells[0]] = dict(zip(INDEX_KEYS, cells))
    return result


if __name__ == "__main__":
    sys.exit(main())

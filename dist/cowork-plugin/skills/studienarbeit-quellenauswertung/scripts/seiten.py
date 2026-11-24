"""Seitenlogik für die lokale Quellenauswertung.

Ermittelt aus dem Text einzelner PDF-Seiten die gedruckte Seitenzahl (Kopf-/Fußzeile
oder Seitenbereich aus Crossref) und schreibt bzw. liest die Seitenmarken
`<!-- seite pdf=N gedruckt=M -->`. Nur Standardbibliothek.
"""
from __future__ import annotations

import re
from collections import Counter

MIN_PAGES = 3  # so viele Seiten müssen denselben Versatz zeigen, damit er als Abschnitt gilt
EDGE_LINES = 2  # Zeilen oben und unten, in denen Seitenzahlen stehen
MAX_HEADER_LEN = 80  # Kopfzeilen sind kurz; lange Zeilen sind Fließtext
MARK_RE = re.compile(r"^<!-- seite pdf=(\d+) gedruckt=(\d+|\?) -->$", re.MULTILINE)
# Kopfzeile: Zahl am Anfang oder Ende einer kurzen Zeile ("320 A. Schmidt", "Journal 12 (2023) 319")
TOP_RE = re.compile(r"^\s*(\d{1,4})(?![\d.,])|(?<![\d.,])(\d{1,4})\s*$")
# Fußzeile: nur die nackte Zahl ("12", "- 12 -") oder mit Wort Seite/Page; "1 Vgl. …" ist eine Fußnote
BOTTOM_RE = re.compile(r"^\W{0,3}(\d{1,4})\W{0,3}$|(?:Seite|Page)\s+(\d{1,4})\s*$", re.IGNORECASE)
# „2 of 20" / „Seite 2 von 20" / „2/20": nur die erste Zahl ist die Seite
N_OF_M_RE = re.compile(r"(\d{1,4})\s*(?:of|von|/)\s*(\d{1,4})\s*$", re.IGNORECASE)
RANGE_RE = re.compile(r"(?<!\d)\d{1,4}\s*[-–]\s*\d{1,4}(?!\d)")


def page_numbers(text: str) -> set[int]:
    """Kandidaten für die gedruckte Seitenzahl aus Kopf- und Fußzeilen einer Seite."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    found: list[str] = []
    # „n / m" auf der ganzen Seite: pypdf liefert Fußzeilen manchmal mitten im Text (PLOS-Seitenleiste);
    # n <= m trennt Seitenangaben von Brüchen, Streutreffer fängt die Abschnittslogik ab
    for line in lines:
        n_of_m = N_OF_M_RE.search(line)
        if n_of_m and int(n_of_m.group(1)) <= int(n_of_m.group(2)):
            found.append(n_of_m.group(1))
    for line in lines[:EDGE_LINES]:
        # „pages 4171–4186" oder „(2014) 1929-1958" ist der Seitenbereich des Artikels, keine Seitenzahl
        if len(line) <= MAX_HEADER_LEN and not N_OF_M_RE.search(line) and not RANGE_RE.search(line):
            found += [n for pair in TOP_RE.findall(line) for n in pair if n]
    for line in lines[-EDGE_LINES:]:
        found += [n for pair in BOTTOM_RE.findall(line) for n in pair if n]
    return {int(n) for n in found if int(n) > 0}


def offset_from_range(page_count: int, page_range: str | None) -> int | None:
    """Versatz aus dem Crossref-Seitenbereich, nur wenn die PDF-Länge exakt passt."""
    if not page_range:
        return None
    match = re.fullmatch(r"\s*(\d+)\s*[-–]\s*(\d+)\s*", page_range)
    if not match:
        return None
    start, end = int(match.group(1)), int(match.group(2))
    return start - 1 if page_count == end - start + 1 else None


NEAR = 5  # eine Zahl so nah an der erwarteten Seite ist eine echte Seitenzahl, die widerspricht


def _parse_range(page_range: str | None) -> tuple[int, int] | None:
    match = re.fullmatch(r"\s*(\d+)\s*[-–]\s*(\d+)\s*", page_range or "")
    return (int(match.group(1)), int(match.group(2))) if match else None


def assign_printed(count: int, offset: int | None, raws: list[str] | None = None,
                   page_range: str | None = None) -> list[str]:
    """Gedruckte Seite je PDF-Seite, abschnittsweise belegt; '?' wo kein Beleg.

    - Kopfzeilen-Modus: Jeder Versatz, den mindestens MIN_PAGES Seiten zeigen, gilt
      für die Seiten, die ihn tragen (nach einer eingeschobenen Bildseite beginnt
      ein neuer Abschnitt mit eigenem Versatz).
    - Crossref-Modus (page_range gesetzt): Der Versatz aus dem Seitenbereich gilt,
      solange keine Seite eine andere Zahl innerhalb des Bereichs trägt.
    - Seiten ohne eigene Zahl: nur, wenn die nummerierten Nachbarn auf beiden
      Seiten denselben Versatz haben, oder (Artikelanfang) die direkt folgende Seite.
    """
    nums = [page_numbers(r) for r in raws] if raws else None
    if nums is None or not any(nums):
        return ["?" if offset is None or i + 1 + offset < 1 else str(i + 1 + offset) for i in range(count)]

    cands = [{n - (i + 1) for n in nums[i]} for i in range(count)]
    valid = _section_pages(cands)  # Versatz -> Seiten, die in einem echten Abschnitt liegen
    rng = _parse_range(page_range) if offset is not None else None

    assigned: list[int | None] = [None] * count
    for i in range(count):
        if rng:  # Crossref-Modus: nur Zahlen innerhalb des Bereichs zählen, sonst gilt der Versatz
            expected = i + 1 + offset
            in_range = {n for n in nums[i] if rng[0] <= n <= rng[1] and n != i + 1}  # i+1: "Page n of m"
            if not in_range or expected in in_range:
                assigned[i] = offset
            continue
        hits = {o for o in cands[i] if i in valid.get(o, ())}
        if len(hits) == 1:
            assigned[i] = hits.pop()

    result = []
    for i in range(count):
        o = assigned[i]
        if o is None and not rng:
            o = _from_neighbours(i, assigned, nums)
        printed = None if o is None else i + 1 + o
        result.append("?" if printed is None or printed < 1 else str(printed))
    return result


def _section_pages(cands: list[set[int]]) -> dict[int, set[int]]:
    """Pro Versatz die Seiten, die in einem Lauf von mind. MIN_PAGES Seiten liegen.

    Ein Lauf darf je eine Seite ohne diesen Versatz überspringen (Zahlen nur auf
    jeder zweiten Seite), verstreute Treffer (Tabellenzahlen) bilden keinen Abschnitt.
    """
    pages_by_offset: dict[int, list[int]] = {}
    for i, offsets in enumerate(cands):
        for o in offsets:
            pages_by_offset.setdefault(o, []).append(i)
    valid: dict[int, set[int]] = {}
    for o, idx in pages_by_offset.items():
        run = [idx[0]]
        for i in idx[1:] + [None]:
            if i is not None and i - run[-1] <= 2:
                run.append(i)
                continue
            if len(run) >= MIN_PAGES:
                valid.setdefault(o, set()).update(run)
            if i is not None:
                run = [i]
    return valid


def _from_neighbours(i: int, assigned: list[int | None], nums: list[set[int]]) -> int | None:
    """Versatz für eine Seite ohne belegte Zahl aus den nächsten belegten Nachbarn."""
    before = next((j for j in range(i - 1, -1, -1) if assigned[j] is not None), None)
    after = next((j for j in range(i + 1, len(assigned)) if assigned[j] is not None), None)
    if before is not None and after is not None and assigned[before] == assigned[after]:
        o = assigned[before]
    elif before is None and after == i + 1:  # erste Seite eines Artikels ohne Kopfzeile
        o = assigned[after]
    else:
        return None
    expected = i + 1 + o
    if any(abs(n - expected) <= NEAR and n != expected for n in nums[i]):
        return None  # Seite trägt eine nahe, aber andere Zahl: Widerspruch
    return o


def render_pages(pages: list[str], offset: int | None, raws: list[str] | None = None,
                 page_range: str | None = None) -> str:
    """Seiten mit Seitenmarke zusammensetzen (Seitenzahlen über assign_printed)."""
    return render_marked(pages, assign_printed(len(pages), offset, raws, page_range))


def render_marked(pages: list[str], printed: list[str]) -> str:
    """Seiten mit bereits bestimmten gedruckten Seitenzahlen zusammensetzen."""
    return "\n".join(
        f"<!-- seite pdf={i + 1} gedruckt={printed[i]} -->\n{text.strip()}\n" for i, text in enumerate(pages)
    )


def parse_pages(markdown: str) -> list[tuple[int, str, str]]:
    """Umkehrung von render_pages: Liste aus (PDF-Seite, gedruckte Seite, Text)."""
    marks = list(MARK_RE.finditer(markdown))
    result = []
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(markdown)
        result.append((int(mark.group(1)), mark.group(2), markdown[mark.end():end].strip()))
    return result

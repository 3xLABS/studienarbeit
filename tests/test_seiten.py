"""Tests für die Seitenlogik: Versatz-Erkennung, Crossref-Fallback, Seitenmarken."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / ".claude/skills/studienarbeit-quellenauswertung/scripts"))

from seiten import assign_printed, offset_from_range, parse_pages, render_pages  # noqa: E402


def detect_offset(pages: list[str]) -> int | None:
    """Testhilfe: der eine Versatz, den assign_printed aus den Kopf-/Fußzeilen belegt."""
    printed = assign_printed(len(pages), None, pages)
    offsets = {int(n) - (i + 1) for i, n in enumerate(printed) if n != "?"}
    return offsets.pop() if len(offsets) == 1 else None


def test_offset_from_footer():
    assert detect_offset([f"Text\n\n{319 + i}" for i in range(5)]) == 318


def test_offset_ignores_year_and_titlepage():
    pages = ["Titel\nJournal 2023"] + [f"Kopf 2023\nText\n{320 + i}" for i in range(4)]
    assert detect_offset(pages) == 318


def test_offset_ignores_numbers_inside_sentences():
    pages = [f"Kopf\nIn Abschnitt {i + 1} zeigt sich mehr.\n{319 + i}" for i in range(4)]
    assert detect_offset(pages) == 318
    assert detect_offset([f"Kopf\nIn Abschnitt {i + 1} zeigt sich mehr." for i in range(4)]) is None


def test_offset_from_n_of_m_footer():
    assert detect_offset([f"Sustainability 2023, 15, 1234\nText\n{i + 1} of 20" for i in range(4)]) == 0
    assert detect_offset([f"Text\nSeite {i + 3} von 40" for i in range(4)]) == 2


def test_offset_none_when_too_few():
    assert detect_offset(["a\n5", "b"]) is None


def test_offset_from_range():
    assert offset_from_range(22, "319-340") == 318
    assert offset_from_range(22, "319–340") == 318
    assert offset_from_range(23, "319-340") is None
    assert offset_from_range(10, None) is None


def test_render_and_parse_roundtrip():
    md = render_pages(["eins", "zwei"], 318)
    assert "<!-- seite pdf=1 gedruckt=319 -->" in md
    assert parse_pages(md) == [(1, "319", "eins"), (2, "320", "zwei")]
    assert "gedruckt=?" in render_pages(["x"], None)


# --- Review-Befunde ---

def test_footnotes_are_not_page_numbers():
    # C4: Fußnoten am Seitenende ("1 Vgl. …") dürfen keinen Versatz erzeugen
    pages = [f"Kopf\nText der Seite.\n{i + 3} Vgl. Müller 2020, S. 12." for i in range(5)]
    assert detect_offset(pages) is None


def test_running_header_number_counts():
    pages = [f"{320 + i} A. Schmidt\nText\nmehr Text\nnoch mehr" for i in range(4)]
    assert detect_offset(pages) == 319


def test_inserted_unnumbered_page_breaks_offset():
    # C3: nach einer eingeschobenen Bildseite stimmt der Versatz nicht mehr
    raws = [f"Text\n{101 + i}" for i in range(5)] + ["Abbildung"] + [f"Text\n{106 + i}" for i in range(4)]
    md = render_pages([f"s{i}" for i in range(10)], 100, raws)
    assert "pdf=5 gedruckt=105" in md
    assert "pdf=6 gedruckt=?" in md          # Bildseite selbst: keine Zahl
    assert "pdf=10 gedruckt=109" in md       # Abschnitt danach behält seine echten Zahlen


def test_crossref_offset_without_any_page_numbers():
    md = render_pages(["a", "b"], 318, ["Text ohne Zahl", "auch ohne"])
    assert "pdf=1 gedruckt=319" in md and "pdf=2 gedruckt=320" in md


def test_roman_front_matter_never_negative():
    # H1: Seiten vor der ersten belegten Seite bekommen ?, nie 0 oder negativ
    raws = ["i", "ii", "iii"] + [f"Text\n{i + 1}" for i in range(5)]
    md = render_pages([f"s{i}" for i in range(8)], -3, raws)
    assert "pdf=1 gedruckt=?" in md and "pdf=4 gedruckt=1" in md
    assert len(parse_pages(md)) == 8


def test_trailing_unnumbered_pages_unknown():
    # Re-Review 3: Anhang ohne Zahlen hinter dem Artikel bekommt keine erfundenen Seiten
    raws = [f"Text\n{101 + i}" for i in range(6)] + ["Anhang ohne Zahl"] * 6
    md = render_pages([f"s{i}" for i in range(12)], 100, raws)
    assert "pdf=6 gedruckt=106" in md and "pdf=7 gedruckt=?" in md and "pdf=12 gedruckt=?" in md


def test_first_page_without_header_gets_number():
    raws = ["Titel des Artikels"] + [f"Text\n{320 + i}" for i in range(4)]
    assert "pdf=1 gedruckt=319" in render_pages([f"s{i}" for i in range(5)], 318, raws)


def test_unnumbered_page_between_agreeing_neighbours():
    raws = [f"Text\n{101 + i}" for i in range(3)] + ["Abbildung"] + [f"Text\n{105 + i}" for i in range(3)]
    assert "pdf=4 gedruckt=104" in render_pages([f"s{i}" for i in range(7)], 100, raws)


def test_crossref_mode_ignores_header_noise():
    # Re-Review 4: Kopfzeile mit Jahreszahl widerspricht dem Crossref-Bereich nicht
    raws = ["Journal of Risk 2023\nText ohne Seitenzahl"] * 5
    md = render_pages([f"s{i}" for i in range(5)], 318, raws, page_range="319-323")
    assert "pdf=1 gedruckt=319" in md and "pdf=5 gedruckt=323" in md


def test_crossref_mode_contradiction_in_range():
    raws = ["Text\nnichts"] * 2 + ["Text\n330"] + ["Text\nnichts"] * 2  # 330 liegt im Bereich, erwartet 321
    md = render_pages([f"s{i}" for i in range(5)], 318, raws, page_range="319-340")
    assert "pdf=3 gedruckt=?" in md and "pdf=2 gedruckt=320" in md


def test_scattered_table_numbers_no_section():
    # Re-Review 2, N2: drei verstreute Tabellenzahlen bilden keinen Abschnitt
    raws = []
    for i in range(20):
        raws.append(f"Tabelle\nZeile\n{i + 1 + 40}" if i in (4, 9, 14) else f"Kopf {101 + i}\nText\nmehr\nnoch mehr")
    printed = assign_printed(20, None, raws)
    assert printed[4] in ("105", "?") and printed[9] in ("110", "?") and printed[14] in ("115", "?")


def test_odd_pages_only_still_section():
    raws = [f"Text\n{101 + i}" if i % 2 == 0 else "Text ohne Zahl" for i in range(8)]
    printed = assign_printed(8, None, raws)
    assert printed[0] == "101" and printed[1] == "102" and printed[6] == "107"


def test_n_of_m_footer_in_middle_of_extracted_text():
    # Echte PLOS-PDF: pypdf liefert die Fußzeile vor dem Seitenleisten-Text
    pages = [f"RESEARCH ARTICLE\nTitel\nPLOS ONE | https://doi.org/10.1371/x April 22, 2020 {i + 1} / 18\n"
             f"Seitenleiste mit Förderhinweis\nEP/ N510129/1 and by Macmillan" for i in range(4)]
    assert assign_printed(4, None, pages) == ["1", "2", "3", "4"]
    # Bruch im Fließtext mit n > m ist keine Seitenzahl
    assert detect_offset([f"Kopf\nVerhältnis 9/{i + 1}\nText\nmehr" for i in range(4)]) is None


def test_page_range_in_header_is_not_a_page_number():
    # Echte ACL-PDF: Seite 1 trägt "pages 4171–4186" im Kopf, danach die Seitenzahl oben
    raws = ["Proceedings of NAACL-HLT 2019, pages 4171–4186\nText\nmehr\nnoch mehr"]
    raws += [f"{4172 + i}\nText\nmehr\nnoch mehr" for i in range(4)]
    md = render_pages([f"s{i}" for i in range(5)], 4170, raws, page_range="4171-4186")
    assert "pdf=1 gedruckt=4171" in md

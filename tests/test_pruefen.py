"""Tests für fundstellen_pruefen.py: Wortlaut-Normalisierung, Seitensuche, Rückschreiben."""
from pathlib import Path

from fundstellen_pruefen import check_file, locate, normalize
from seiten import parse_pages, render_pages

PAGES = [
    "Einleitung zum Thema der vorliegenden Untersuchung über Risiken.",
    "Cyberrisiken nehmen seit Jahren deutlich zu. Das integrierte",
    "Risikomanagement bündelt alle Domänen. Weitere Ausführungen folgen.",
]


def stelle(nr: int, zitat: str, seite: str) -> str:
    return (
        f"### Stelle {nr}\n- Zitat: „{zitat}“\n- Seite: {seite}\n- Bezug: FF1\n"
        f"- Funktion: Beleg\n- Kapitel: 2\n- Check: offen\n"
    )


def test_normalize_hyphen_ligature_quotes():
    assert normalize("Risiko-\nmanagement ist „eﬃzient“") == normalize("Risikomanagement ist effizient")


def test_locate_exact_page():
    pages = parse_pages(render_pages(PAGES, 318))
    assert locate("Cyberrisiken nehmen seit Jahren deutlich zu.", pages) == (2, "320")


def test_quote_across_page_break():
    pages = parse_pages(render_pages(PAGES, 318))
    assert locate("Das integrierte Risikomanagement bündelt alle Domänen.", pages) == (2, "320")


def test_check_file_marks(tmp_path: Path):
    md = tmp_path / "quelle.md"
    md.write_text(render_pages(PAGES, 318), encoding="utf-8")
    f = tmp_path / "Fundstellen_quelle.md"
    f.write_text(
        "# Fundstellen\n\n"
        + stelle(1, "Cyberrisiken nehmen seit Jahren deutlich zu.", "320 (PDF 2)")
        + "\n" + stelle(2, "Einleitung zum Thema der vorliegenden Untersuchung über Risiken.", "321 (PDF 3)")
        + "\n" + stelle(3, "Das steht so nirgends in dieser Quelle drin.", "319 (PDF 1)"),
        encoding="utf-8",
    )
    res = check_file(f, md)
    assert [r["status"] for r in res] == ["belegt", "andere-seite", "nicht-gefunden"]
    text = f.read_text(encoding="utf-8")
    assert "Check: ✅ belegt" in text
    assert "Seite: 319 (PDF 1)" in text and "korrigiert von S. 321" in text
    assert "[ZITAT PRÜFEN]" in text


def test_unknown_printed_page(tmp_path: Path):
    md = tmp_path / "q.md"
    md.write_text(render_pages(PAGES, None), encoding="utf-8")
    f = tmp_path / "F.md"
    f.write_text(stelle(1, "Einleitung zum Thema der vorliegenden Untersuchung über Risiken.", "5 (PDF 1)"), encoding="utf-8")
    check_file(f, md)
    assert "Seite: [SEITE PRÜFEN] (PDF 1)" in f.read_text(encoding="utf-8")


def test_docx_wording_only(tmp_path: Path):
    md = tmp_path / "bericht.md"
    md.write_text("# Bericht\n\nUnternehmen steuern Risiken zunehmend integriert.\n", encoding="utf-8")
    f = tmp_path / "F.md"
    f.write_text(stelle(1, "Unternehmen steuern Risiken zunehmend integriert.", "Abschnitt Bericht"), encoding="utf-8")
    res = check_file(f, md)
    assert res[0]["status"] == "belegt"
    assert "Seite: Abschnitt Bericht" in f.read_text(encoding="utf-8")


# --- Review-Befunde ---
LONG = "Das integrierte Risikomanagement bündelt alle Domänen."


def _run(tmp_path, pages_md: str, block: str):
    md = tmp_path / "q.md"; md.write_text(pages_md, encoding="utf-8")
    f = tmp_path / "F.md"; f.write_text(block, encoding="utf-8")
    return check_file(f, md)[0], f.read_text(encoding="utf-8")


def test_multiline_quote_fully_checked(tmp_path):
    # C1: zweite Zeile eines umbrochenen Zitats wird mitgeprüft
    block = ("### Stelle 1\n- Zitat: „Das integrierte Risikomanagement bündelt\n  völlig erfundene Dinge in großer Menge.“\n"
             "- Seite: 320 (PDF 2)\n- Check: offen\n")
    res, _ = _run(tmp_path, render_pages(PAGES, 318), block)
    assert res["status"] in ("nicht-gefunden", "format")  # beides: abgelehnt, nie belegt


def test_stated_page_kept_when_quote_repeats(tmp_path):
    # C2: Satz steht auf S. 101 und 103, Angabe 103 bleibt
    pages = [LONG, "Anderes.", LONG]
    res, text = _run(tmp_path, render_pages(pages, 100), stelle(1, LONG, "103 (PDF 3)"))
    assert res["status"] == "belegt" and "Seite: 103 (PDF 3)" in text


def test_ambiguous_page_not_autocorrected(tmp_path):
    pages = [LONG, "Anderes.", LONG]
    res, text = _run(tmp_path, render_pages(pages, 100), stelle(1, LONG, "102 (PDF 2)"))
    assert res["status"] == "mehrdeutig" and "[SEITE PRÜFEN]" in text


def test_short_quote_rejected(tmp_path):
    res, text = _run(tmp_path, render_pages(PAGES, 318), stelle(1, "Einleitung zum Thema.", "319 (PDF 1)"))
    assert res["status"] == "zu-kurz" and "[ZITAT PRÜFEN]" in text


def test_no_pages_number_replaced(tmp_path):
    # C5: ohne Seitenmarken wird eine behauptete Seitenzahl nicht bestätigt
    res, text = _run(tmp_path, f"# OCR\n\n{LONG}\n", stelle(1, LONG, "47 (PDF 3)"))
    assert res["status"] == "belegt" and "Seite: [SEITE PRÜFEN]" in text


def test_footnote_marker_ignored(tmp_path):
    # H4: Fußnotenzeichen im Quelltext stört den Abgleich nicht
    src = render_pages(["Das integrierte Risikomanagement³ bündelt alle Domänen[^4] effizient."], 0)
    q = "Das integrierte Risikomanagement bündelt alle Domänen effizient."
    res, _ = _run(tmp_path, src, stelle(1, q, "1 (PDF 1)"))
    assert res["status"] == "belegt"


def test_ellipsis_rejected(tmp_path):
    res, text = _run(tmp_path, render_pages(PAGES, 318),
                     stelle(1, "Cyberrisiken nehmen […] deutlich zu und das ist sehr lang.", "320 (PDF 2)"))
    assert res["status"] == "auslassung" and "[ZITAT PRÜFEN]" in text


def test_trailing_content_after_last_field_kept(tmp_path):
    # Re-Review 2: Notizen nach dem letzten Feld bleiben erhalten
    block = stelle(1, LONG, "1 (PDF 1)") + "\n---\n\n## Fazit\nWichtige Notizen.\n"
    _, text = _run(tmp_path, render_pages([LONG], 0), block)
    assert "## Fazit\nWichtige Notizen." in text and "Check: ✅ belegt" in text


def test_glued_digit_not_ignored_in_quote(tmp_path):
    # Re-Review 6: „Stufe4" darf nicht zu „Stufe3" im Quelltext passen
    src = render_pages(["Die Stufe3 des Modells verbindet alle Bereiche der Steuerung."], 0)
    res, _ = _run(tmp_path, src, stelle(1, "Die Stufe4 des Modells verbindet alle Bereiche der Steuerung.", "1 (PDF 1)"))
    assert res["status"] == "nicht-gefunden"
    res, _ = _run(tmp_path, src, stelle(1, "Die Stufe3 des Modells verbindet alle Bereiche der Steuerung.", "1 (PDF 1)"))
    assert res["status"] == "belegt"


def test_no_pages_page_inside_text_replaced(tmp_path):
    # Re-Review 7
    _, text = _run(tmp_path, f"# OCR\n\n{LONG}\n", stelle(1, LONG, "Kapitel 3, S. 45"))
    assert "Seite: [SEITE PRÜFEN]" in text


def test_unindented_wrapped_quote_rejected(tmp_path):
    # Re-Review 2, R1: umbrochenes Zitat ohne Einrückung wird nicht halb geprüft
    block = ("### Stelle 1\n- Zitat: „Das integrierte Risikomanagement bündelt alle Domänen.\n"
             "und wurde von allen Experten als gescheitert bewertet.“\n- Seite: 1 (PDF 1)\n- Check: offen\n")
    res, text = _run(tmp_path, render_pages([LONG], 0), block)
    assert res["status"] == "format" and "[ZITAT PRÜFEN]" in text


def test_unclosed_quote_rejected(tmp_path):
    block = "### Stelle 1\n- Zitat: „Das integrierte Risikomanagement bündelt alle Domänen.\n- Seite: 1 (PDF 1)\n- Check: offen\n"
    res, _ = _run(tmp_path, render_pages([LONG], 0), block)
    assert res["status"] == "format"


def test_german_punctuation_after_quote_ok(tmp_path):
    # Re-Review 3: „…“. und „…“ (Hervorhebung im Original) sind korrekt
    for tail in ["“.", "“ (Hervorhebung im Original)"]:
        block = f"### Stelle 1\n- Zitat: „{LONG[:-1]}{tail}\n- Seite: 1 (PDF 1)\n- Check: offen\n"
        res, _ = _run(tmp_path, render_pages([LONG], 0), block)
        assert res["status"] == "belegt", tail


def test_inline_hyphenation_from_anydoc():
    # Echte ACL-PDF: anydoc liefert Trennungen als "representa- tion" mitten in der Zeile
    from fundstellen_pruefen import normalize
    source = "We introduce a new language representa- tion model called **BERT**, designed to pre- train"
    assert normalize("We introduce a new language representation model called BERT") in normalize(source)
    assert normalize("designed to pre-train") in normalize(source)
    assert normalize("Daten- und KI-Risiken") in normalize("die Daten- und KI- Risiken")

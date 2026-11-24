"""Tests für quellen_umwandeln.py: Seitenmarken, Versatz, Formate, Index, Wiederholungslauf."""
import os
import time
from pathlib import Path

from quellen_umwandeln import kurzname, main


def run_cli(quellen: Path, *extra: str) -> int:
    return main([str(quellen), *extra])


def read_md(quellen: Path, name: str) -> str:
    return (quellen / "markdown" / f"{name}.md").read_text(encoding="utf-8")


def index(quellen: Path) -> str:
    return (quellen / "markdown" / "_index.md").read_text(encoding="utf-8")


def test_pdf_pages_and_offset(tmp_quellen, footer_pdf):
    run_cli(tmp_quellen)
    md = read_md(tmp_quellen, "mueller-2021")
    assert "<!-- seite pdf=3 gedruckt=321 -->" in md
    assert "kopfzeile" in index(tmp_quellen)


def test_range_fallback(tmp_quellen, plain_pdf_22_pages, recherche_with_range):
    run_cli(tmp_quellen)
    assert "<!-- seite pdf=1 gedruckt=319 -->" in read_md(tmp_quellen, "schmidt-2020")
    assert "crossref" in index(tmp_quellen)


def test_docx_without_pages(tmp_quellen, docx_file):
    run_cli(tmp_quellen)
    md = read_md(tmp_quellen, "bericht")
    assert "<!-- seite" not in md
    assert "integriert" in md


def test_scan_reported(tmp_quellen, image_pdf):
    run_cli(tmp_quellen)
    assert "braucht-ocr" in index(tmp_quellen)


def test_missing_file_reported(tmp_quellen, plain_pdf_22_pages, recherche_with_range):
    run_cli(tmp_quellen)
    idx = index(tmp_quellen)
    assert "Weber" in idx and "fehlt" in idx


def test_kurzname_umlaut_spaces_collision():
    taken: set[str] = set()
    assert kurzname("Müller 2021 Risiko.pdf", taken) == "mueller-2021-risiko"
    taken.add("mueller-2021-risiko")
    assert kurzname("Müller 2021 Risiko.docx", taken) == "mueller-2021-risiko-2"


def test_skip_unchanged_reconvert_changed(tmp_quellen, footer_pdf):
    run_cli(tmp_quellen)
    out = tmp_quellen / "markdown" / "mueller-2021.md"
    first = out.stat().st_mtime
    time.sleep(0.05)
    run_cli(tmp_quellen)
    assert out.stat().st_mtime == first
    future = time.time() + 10
    os.utime(footer_pdf, (future, future))
    run_cli(tmp_quellen)
    assert out.stat().st_mtime > first


# --- Review-Befunde ---

def test_range_only_for_unique_match(tmp_quellen, plain_pdf_22_pages):
    # H2: zwei Zeilen Schmidt 2020 → Bereich nicht raten
    (tmp_quellen / "Recherche_Kapitel_1_X.md").write_text(
        "| Autor | Jahr | Seiten |\n|---|---|---|\n| Schmidt, A. | 2020 | 319-340 |\n| Schmidt, B. | 2020 | 1-22 |\n",
        encoding="utf-8")
    run_cli(tmp_quellen)
    assert "gedruckt=?" in read_md(tmp_quellen, "schmidt-2020")


def test_key_needs_word_boundary(tmp_quellen, plain_pdf_22_pages):
    (tmp_quellen / "Recherche_Kapitel_1_X.md").write_text(
        "| Autor | Jahr | Seiten |\n|---|---|---|\n| Midt, C. | 2020 | 319-340 |\n", encoding="utf-8")
    run_cli(tmp_quellen)
    assert "gedruckt=?" in read_md(tmp_quellen, "schmidt-2020")


def test_added_range_triggers_reconvert(tmp_quellen, plain_pdf_22_pages):
    # H3: Seitenbereich nachgetragen → neue Umwandlung trotz unveränderter PDF
    run_cli(tmp_quellen)
    assert "gedruckt=?" in read_md(tmp_quellen, "schmidt-2020")
    (tmp_quellen / "Recherche_Kapitel_1_X.md").write_text(
        "| Autor | Jahr | Seiten |\n|---|---|---|\n| Schmidt, A. | 2020 | 319-340 |\n", encoding="utf-8")
    run_cli(tmp_quellen)
    assert "gedruckt=319" in read_md(tmp_quellen, "schmidt-2020")


def test_names_stable_when_new_file_sorts_first(tmp_quellen, footer_pdf):
    # M3: "Mueller 2021!.pdf" sortiert vor "Mueller 2021.pdf" und hat denselben Stamm
    import shutil
    run_cli(tmp_quellen)
    shutil.copy2(footer_pdf, tmp_quellen / "dateien" / "Mueller 2021!.pdf")
    run_cli(tmp_quellen)
    idx = index(tmp_quellen)
    assert "| Mueller 2021.pdf | mueller-2021 |" in idx
    assert "| Mueller 2021!.pdf | mueller-2021-2 |" in idx


def test_inserted_page_end_to_end(tmp_quellen):
    # Re-Review 1: Seitenprüfung läuft im echten Umwandeln-Pfad
    import conftest
    conftest._pdf(tmp_quellen / "dateien" / "Weber 2019.pdf", 10, 101, skip_footer={5})
    run_cli(tmp_quellen)
    md = read_md(tmp_quellen, "weber-2019")
    assert "pdf=5 gedruckt=105" in md and "pdf=6 gedruckt=?" in md and "pdf=10 gedruckt=109" in md


def test_page_n_of_m_loses_to_journal_range(tmp_quellen):
    # Re-Review 2, N1: Datenbank-Ausdruck "Page 3 of 12" vs. Zeitschriftenbereich 320-331
    from reportlab.pdfgen import canvas
    path = tmp_quellen / "dateien" / "Kim 2022.pdf"
    c = canvas.Canvas(str(path))
    for i in range(12):
        c.setFont("Helvetica", 11)
        c.drawString(72, 740, "Das integrierte Risikomanagement verbindet alle Bereiche.")
        c.drawString(250, 40, f"Page {i + 1} of 12")
        c.showPage()
    c.save()
    (tmp_quellen / "Recherche_Kapitel_1_K.md").write_text(
        "| Autor | Jahr | Seiten |\n|---|---|---|\n| Kim, J. | 2022 | 320-331 |\n", encoding="utf-8")
    run_cli(tmp_quellen)
    md = read_md(tmp_quellen, "kim-2022")
    assert "pdf=1 gedruckt=320" in md and "pdf=12 gedruckt=331" in md


def test_printout_numbering_overlapping_range(tmp_quellen):
    # Re-Review 3: "Page n of 12" bei Artikel S. 5-16 überschneidet sich mit dem Bereich
    from reportlab.pdfgen import canvas
    path = tmp_quellen / "dateien" / "Lee 2021.pdf"
    c = canvas.Canvas(str(path))
    for i in range(12):
        c.setFont("Helvetica", 11)
        c.drawString(72, 740, "Das integrierte Risikomanagement verbindet alle Bereiche.")
        c.drawString(250, 40, f"Page {i + 1} of 12")
        c.showPage()
    c.save()
    (tmp_quellen / "Recherche_Kapitel_1_L.md").write_text(
        "| Autor | Jahr | Seiten |\n|---|---|---|\n| Lee, S. | 2021 | 5-16 |\n", encoding="utf-8")
    run_cli(tmp_quellen)
    md = read_md(tmp_quellen, "lee-2021")
    assert "pdf=1 gedruckt=5" in md and "pdf=5 gedruckt=9" in md and "pdf=12 gedruckt=16" in md


def test_range_conflicting_with_headers(tmp_quellen, recherche_with_range):
    # Re-Review 4: Kopfzeilen 320..331, Protokoll sagt 1-12 (Tippfehler) → Konflikt, keine Seitenzahl
    import conftest
    conftest._pdf(tmp_quellen / "dateien" / "Park 2020.pdf", 12, 320)
    (tmp_quellen / "Recherche_Kapitel_1_P.md").write_text(
        "| Autor | Jahr | Seiten |\n|---|---|---|\n| Park, H. | 2020 | 1-12 |\n", encoding="utf-8")
    run_cli(tmp_quellen)
    md = read_md(tmp_quellen, "park-2020")
    assert "gedruckt=1 " not in md and "pdf=5 gedruckt=?" in md
    assert "konflikt" in index(tmp_quellen)

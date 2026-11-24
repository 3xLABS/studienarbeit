"""Gemeinsame Fixtures: synthetische Quellen (PDF, DOCX, Scan) und Recherche-Protokoll."""
import io
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parent.parent / ".claude/skills/studienarbeit-quellenauswertung/scripts"
sys.path.insert(0, str(SCRIPTS))

LOREM = (
    "Das integrierte Risikomanagement verbindet Cyberrisiken, Datenschutzrisiken und "
    "KI-Risiken in einem gemeinsamen Steuerungsmodell. Seite {n} beschreibt dabei einen "
    "eigenen Aspekt der Untersuchung."
)


def _pdf(path: Path, pages: int, footer_start: int | None, skip_footer: set[int] = frozenset()) -> Path:
    """Text-PDF mit optionaler gedruckter Seitenzahl in der Fußzeile."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(str(path), pagesize=A4)
    for i in range(pages):
        c.setFont("Helvetica", 11)
        c.drawString(72, 780, "Journal of Risk Studies 2023")
        text = c.beginText(72, 740)
        for line in LOREM.format(n=i + 1).split(". "):
            text.textLine(line)
        c.drawText(text)
        if footer_start is not None and i not in skip_footer:
            c.drawString(300, 40, str(footer_start + i - sum(1 for s in skip_footer if s < i)))
        c.showPage()
    c.save()
    return path


@pytest.fixture
def tmp_quellen(tmp_path: Path) -> Path:
    quellen = tmp_path / "02-quellen"
    (quellen / "dateien").mkdir(parents=True)
    return quellen


@pytest.fixture
def footer_pdf(tmp_quellen: Path) -> Path:
    return _pdf(tmp_quellen / "dateien" / "Mueller 2021.pdf", 5, 319)


@pytest.fixture
def plain_pdf_22_pages(tmp_quellen: Path) -> Path:
    return _pdf(tmp_quellen / "dateien" / "Schmidt 2020.pdf", 22, None)


@pytest.fixture
def docx_file(tmp_quellen: Path) -> Path:
    from docx import Document

    doc = Document()
    doc.add_heading("Bericht zur Lage", level=1)
    doc.add_paragraph("Unternehmen steuern Risiken zunehmend integriert.")
    path = tmp_quellen / "dateien" / "Bericht.docx"
    doc.save(str(path))
    return path


@pytest.fixture
def image_pdf(tmp_quellen: Path) -> Path:
    """PDF, das nur ein Bild enthält (wie ein Scan)."""
    from PIL import Image
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas

    img = Image.new("RGB", (400, 600), "white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    path = tmp_quellen / "dateien" / "Scan.pdf"
    c = canvas.Canvas(str(path), pagesize=A4)
    c.drawImage(ImageReader(buf), 72, 72, width=400, height=600)
    c.showPage()
    c.save()
    return path


@pytest.fixture
def recherche_with_range(tmp_quellen: Path) -> Path:
    path = tmp_quellen / "Recherche_Kapitel_1_Test.md"
    path.write_text(
        "# Recherche Kapitel 1\n\n## Gesammelte Quellen\n\n"
        "| # | Titel | Autor | Jahr | Typ | Relevanz | Check | DOI | Seiten |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| 1 | Risiko integriert | Schmidt, A. | 2020 | Paper | ★★★★☆ | ✅ verifiziert | 10.1/x | 319-340 |\n"
        "| 2 | Ohne Datei | Weber & Lee | 2019 | Paper | ★★★☆☆ | ✅ verifiziert | 10.1/y | 12-30 |\n",
        encoding="utf-8",
    )
    return path

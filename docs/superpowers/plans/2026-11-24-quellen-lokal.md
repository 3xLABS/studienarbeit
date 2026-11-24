# Lokale Quellenauswertung mit anydoc: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Phase 3 der Pipeline läuft lokal: Quellen werden mit anydoc seitengenau umgewandelt, Claude wählt pro Quelle die wichtigsten Stellen, ein Skript prüft jedes Zitat wörtlich samt Seite.

**Architecture:** Drei Python-Dateien im Skill `studienarbeit-quellenauswertung/scripts/` (Seitenlogik, Umwandeln, Prüfen), aufgerufen über `uv run --with …`, ohne Projekt-venv. Die Skill-Texte steuern Claude durch Umwandeln → Suchen → Prüfen → Kapitel-Auswertung. Die drei Auslieferungen (`.claude/skills`, `dist/cowork-plugin`, `dist/master-skill`) werden am Ende synchronisiert.

**Tech Stack:** Python ≥ 3.10, firecrawl-anydoc 0.2.5, pypdf, pytest, reportlab und python-docx (nur Tests), uv.

**Spec:** `docs/superpowers/specs/2026-11-24-quellen-lokal-design.md`

## Global Constraints

- Python ≥ 3.10; Aufruf immer über `uv run --with firecrawl-anydoc --with pypdf <script>`.
- Seitenmarke exakt: `<!-- seite pdf=<n> gedruckt=<m|?> -->`, eine Zeile vor jedem Seiteninhalt.
- Keine Seitenzahl ohne Beleg; unbelegt → `gedruckt=?` bzw. Marker `[SEITE PRÜFEN]`.
- Nicht gefundenes Zitat → Marker `[ZITAT PRÜFEN]`, nie still behalten.
- Keine Netzwerkaufrufe in den Skripten; hosted OCR nur über Flag `--ocr <datei>`, das der Skill erst nach Ja des Users setzt.
- Ordner: `02-quellen/dateien/`, `02-quellen/markdown/`, `02-quellen/fundstellen/`, alle drei in `.gitignore`.
- Laufzeit Code-Tab der Desktop-App; ohne Shell stoppt Phase 3 mit Verweis darauf.
- Skill-Texte deutsch, echte Umlaute, kein Em-Dash.
- Version 1.4.0 in `marketplace.json` und `plugin.json`.
- Kein Commit/Push ohne Chris' Go. Arbeit auf Branch `feat/quellen-lokal`.

## Review Focus

1. Zitat über eine Seitengrenze → belegt mit erster Seite (Task 3, `test_quote_across_page_break`).
2. Titelseite ohne Nummer, Kopfzeile mit Jahreszahl „2023" → Versatz trotzdem aus der Mehrheit (Task 1, `test_offset_ignores_year_and_titlepage`).
3. Silbentrennung am Zeilenende und Ligaturen (`ﬁ`) → Zitat ohne Trennung wird gefunden (Task 3, `test_normalize_hyphen_ligature_quotes`).
4. Dateinamen mit Umlauten und Leerzeichen → stabiler, eindeutiger Kurzname (Task 2, `test_kurzname_umlaut_spaces_collision`).
5. Datei nach Umwandlung ersetzt → wird neu umgewandelt, unveränderte nicht (Task 2, `test_skip_unchanged_reconvert_changed`).

---

### Task 1: Seitenlogik (reine Funktionen)

**Files:**
- Create: `.claude/skills/studienarbeit-quellenauswertung/scripts/seiten.py`
- Test: `tests/test_seiten.py`

**Interfaces:**
- Produces:
  - `detect_offset(page_texts: list[str]) -> int | None` — Zahl (arabisch) in den ersten/letzten 2 nichtleeren Zeilen je Seite; Kandidat = Zahl − PDF-Seite (1-basiert). Ergebnis nur, wenn ≥ 3 Seiten denselben Versatz liefern und dieser die Mehrheit aller Kandidaten ist; sonst `None`.
  - `offset_from_range(page_count: int, page_range: str | None) -> int | None` — `"319-340"` oder `"319–340"`: wenn `page_count == ende - anfang + 1`, dann `anfang - 1`; sonst `None`.
  - `render_pages(pages: list[str], offset: int | None) -> str` — Seiten mit Marke, `gedruckt=?` bei `None`.
  - `parse_pages(markdown: str) -> list[tuple[int, str, str]]` — `(pdf, gedruckt, text)`, Umkehrung von `render_pages`.

- [ ] **Step 1: Write the failing tests**

```python
def test_offset_from_footer():
    assert detect_offset([f"Text\n\n{319 + i}" for i in range(5)]) == 318

def test_offset_ignores_year_and_titlepage():
    pages = ["Titel\nJournal 2023"] + [f"Kopf 2023\nText\n{320 + i}" for i in range(4)]
    assert detect_offset(pages) == 318

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
```

- [ ] **Step 2: Run, expect FAIL** — `uv run --with pytest pytest tests/test_seiten.py -q` → ImportError.
- [ ] **Step 3: Implement** die vier Funktionen in `seiten.py` (nur Standardbibliothek).
- [ ] **Step 4: Run, expect PASS** — 5 passed.

### Task 2: Umwandeln (`quellen_umwandeln.py`)

**Files:**
- Create: `.claude/skills/studienarbeit-quellenauswertung/scripts/quellen_umwandeln.py`
- Test: `tests/test_umwandeln.py`, `tests/conftest.py` (Fixtures: PDF mit Fußzeilen-Seitenzahlen per reportlab, PDF ohne Seitenzahlen mit 22 Seiten, .docx per python-docx, Bild-PDF ohne Text, `Recherche_Kapitel_1_Test.md` mit Seiten-Spalte)

**Interfaces:**
- Consumes: `detect_offset`, `offset_from_range`, `render_pages` aus Task 1 (Import über `sys.path.insert(0, str(Path(__file__).parent))`).
- Produces:
  - `kurzname(filename: str, taken: set[str]) -> str` — ä→ae, ö→oe, ü→ue, ß→ss, Rest ASCII, kebab-case, ohne Endung, Kollision → `-2`, `-3`.
  - `load_recherche(quellen_dir: Path) -> list[dict]` — Zeilen der Quellentabellen aus `Recherche_*.md` (`titel`, `autor`, `jahr`, `seiten`); Schlüssel für Zuordnung: Nachname Erstautor + Jahr, kleingeschrieben, im Kurznamen enthalten.
  - `convert_file(path: Path, page_range: str | None, ocr: bool) -> tuple[str, dict]` — Markdown + `{format, seiten, versatz_quelle: "kopfzeile"|"crossref"|"unbekannt"|"ohne-seiten", status: "ok"|"braucht-ocr"|"fehler"}`. PDF: pypdf schreibt jede Seite als eigenes PDF in Bytes, `anydoc.to_markdown_bytes(b)` je Seite; Versatz erst `detect_offset`, dann `offset_from_range`. Andere Formate: `anydoc.to_markdown(str(path))`. NeedsOcr-Ausnahme → `braucht-ocr`; mit `ocr=True` `anydoc.to_markdown(str(path), ocr="hosted")` (dann ohne Seitenmarken, `versatz_quelle="unbekannt"`). Exakte Ausnahme-Klasse aus `anydoc/_anydoc.pyi` übernehmen.
  - CLI: `quellen_umwandeln.py <quellen_dir> [--ocr <dateiname> ...]` — schreibt `markdown/<kurzname>.md` und `markdown/_index.md` (Tabelle `Datei | Kurzname | Format | Seiten | Versatz | Status`, darunter Abschnitt „Ohne Datei" mit Recherche-Einträgen ohne zugeordnete Datei, Status `fehlt`); überspringt Dateien, deren Markdown neuer ist als die Quelle; druckt Zusammenfassung inkl. `braucht-ocr` und `fehlt`.

- [ ] **Step 1: Write the failing tests**

```python
def test_pdf_pages_and_offset(tmp_quellen, footer_pdf):          # "Mueller 2021.pdf", Fußzeilen 319..323
    run_cli(tmp_quellen)
    assert "<!-- seite pdf=3 gedruckt=321 -->" in read_md(tmp_quellen, "mueller-2021")

def test_range_fallback(tmp_quellen, plain_pdf_22_pages, recherche_with_range):  # Schmidt 2020, 319-340
    run_cli(tmp_quellen)
    assert "gedruckt=319" in read_md(tmp_quellen, "schmidt-2020")

def test_docx_without_pages(tmp_quellen, docx_file):
    run_cli(tmp_quellen)
    assert "<!-- seite" not in read_md(tmp_quellen, "bericht")

def test_scan_reported(tmp_quellen, image_pdf):
    run_cli(tmp_quellen)
    assert "braucht-ocr" in index(tmp_quellen)

def test_missing_file_reported(tmp_quellen, recherche_with_range):  # Eintrag ohne Datei
    run_cli(tmp_quellen)
    assert "fehlt" in index(tmp_quellen)

def test_kurzname_umlaut_spaces_collision():
    taken = set()
    assert kurzname("Müller 2021 Risiko.pdf", taken) == "mueller-2021-risiko"
    taken.add("mueller-2021-risiko")
    assert kurzname("Müller 2021 Risiko.docx", taken) == "mueller-2021-risiko-2"

def test_skip_unchanged_reconvert_changed(tmp_quellen, footer_pdf):
    # 2. Lauf: mtime des Markdowns unverändert; nach os.utime der Quelle in die Zukunft: neu geschrieben
```

- [ ] **Step 2: Run, expect FAIL** — `uv run --with pytest --with firecrawl-anydoc --with pypdf --with reportlab --with python-docx pytest tests/test_umwandeln.py -q`.
- [ ] **Step 3: Implement** nach Interfaces.
- [ ] **Step 4: Run, expect PASS** — 7 passed. Meldet anydoc das reportlab-PDF als OCR-bedürftig: Fixture mit Standardschrift (Helvetica) prüfen, nicht den Code aufweichen.

### Task 3: Prüfen (`fundstellen_pruefen.py`)

**Files:**
- Create: `.claude/skills/studienarbeit-quellenauswertung/scripts/fundstellen_pruefen.py`
- Test: `tests/test_pruefen.py`

**Interfaces:**
- Consumes: `parse_pages` aus Task 1.
- Fundstellen-Format (fest; Claude schreibt es, Skript liest und schreibt zurück):

```markdown
### Stelle 1
- Zitat: „Wörtlicher Text der Quelle."
- Seite: 325 (PDF 7)
- Bezug: FF1
- Funktion: Beleg
- Kapitel: 2
- Check: offen
```

- Produces:
  - `normalize(text: str) -> str` — NFKC (Ligaturen), `-\n` vor Kleinbuchstabe entfernen, Anführungszeichen „“”"‚‘’'« » entfernen, `*_#>` entfernen, Leerraum zu einem Leerzeichen, lowercase.
  - `locate(quote: str, pages: list[tuple[int, str, str]]) -> tuple[int, str] | None` — erste Seite, auf der das normalisierte Zitat steht; zusätzlich Seitenpaare (n, n+1) zusammen durchsuchen, Treffer zählt für n.
  - `check_file(fundstellen: Path, markdown: Path) -> list[dict]` — je Stelle `{nr, status: "belegt"|"andere-seite"|"nicht-gefunden", seite_alt, seite_neu}`; schreibt zurück: `Check: ✅ belegt` / neue `Seite:`-Zeile + `Check: ⚠️ korrigiert von S. <alt>` / `Check: ❌ nicht gefunden [ZITAT PRÜFEN]`. Bei `gedruckt=?`: `Seite: [SEITE PRÜFEN] (PDF n)`. Markdown ohne Seitenmarken (docx): nur Wortlaut prüfen, Seite bleibt Abschnittsangabe.
  - CLI: `fundstellen_pruefen.py <fundstellen.md> <markdown.md>`; druckt Zusammenfassung; Exit 1, wenn mindestens eine Stelle nicht gefunden.

- [ ] **Step 1: Write the failing tests**

```python
def test_normalize_hyphen_ligature_quotes():
    assert normalize("Risiko-\nmanagement ist „eﬃzient“") == normalize("Risikomanagement ist effizient")

def test_locate_exact_page():        # Zitat steht auf pdf=2 → (2, "320")
def test_quote_across_page_break():  # erster Halbsatz pdf=2, Rest pdf=3 → (2, "320")

def test_check_file_marks(tmp_path):  # 3 Stellen: richtig, falsche Seite, erfunden
    res = check_file(f, md)
    assert [r["status"] for r in res] == ["belegt", "andere-seite", "nicht-gefunden"]
    text = f.read_text()
    assert "Seite: 320 (PDF 2)" in text and "[ZITAT PRÜFEN]" in text

def test_unknown_printed_page():     # gedruckt=? → "Seite: [SEITE PRÜFEN] (PDF 4)"
def test_docx_wording_only():        # Markdown ohne Marken, Zitat vorhanden → belegt, Seite unverändert
```

- [ ] **Step 2: Run, expect FAIL** — `uv run --with pytest pytest tests/test_pruefen.py -q`.
- [ ] **Step 3: Implement** nach Interfaces.
- [ ] **Step 4: Run, expect PASS**; dann ganze Suite mit allen `--with` aus Task 2.

### Task 4: Skill-Texte und Projektdateien

**Files:**
- Modify: `.claude/skills/studienarbeit-quellenauswertung/SKILL.md` — Literatur-Strang (Übersicht, Schritte 2–5, Seiten-Check) neu; Empirik-Strang unverändert; Frontmatter-Description anpassen (< 1024 Zeichen).
- Delete: `.claude/skills/studienarbeit-quellenauswertung/references/gem-systemprompt.md`, falls `grep -rn gem-systemprompt .claude` danach keinen Verweis mehr zeigt.
- Modify: `studienarbeit-onboarding/SKILL.md` — Shell-Check (sonst Stopp mit Hinweis Code-Tab der Desktop-App); `uv --version`, sonst Installation macOS/Linux `curl -LsSf https://astral.sh/uv/install.sh | sh`, Windows `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`; Smoke-Test: Umwandeln-Skript auf leerem Ordner läuft fehlerfrei.
- Modify: `studienarbeit-planung/SKILL.md` — optionaler Abschnitt „Hypothesen" im Template von `Forschungsfrage.md`.
- Modify: `studienarbeit-recherche/SKILL.md` — Abschluss: Volltexte nach `02-quellen/dateien/`, Webseiten per „Drucken → Als PDF".
- Modify: `studienarbeit-writer/SKILL.md` — nur Stellen mit `✅` oder `⚠️ korrigiert`; `[ZITAT PRÜFEN]`/`[SEITE PRÜFEN]` nie still auflösen.
- Modify: `studienarbeit-finalisierung/SKILL.md` — Seiten-Check: offene Marker aus Kapiteln und Fundstellen in den Prüfbericht; Rechenregel entfällt.
- Modify: `.claude/CLAUDE.md`, `README.md` — Phase 3, Tool-Tabelle (Gemini nur noch Empirik-Strang, falls dort genutzt), Voraussetzungen (Desktop-App Code-Tab, uv), Ordnerstruktur, Changelog 1.4.0.
- Modify: `.gitignore` — `02-quellen/dateien/*`, `!02-quellen/dateien/.gitkeep`, `02-quellen/markdown/`, `02-quellen/fundstellen/`.
- Create: `02-quellen/dateien/.gitkeep`

Neuer Literatur-Ablauf im Skill (Claude formuliert die Prosa):
1. Voraussetzungen: Shell verfügbar, Forschungsfrage, Gliederung, Dateien in `02-quellen/dateien/`.
2. Umwandeln: `uv run --with firecrawl-anydoc --with pypdf "<Skill-Basisordner>/scripts/quellen_umwandeln.py" 02-quellen`; `_index.md` zusammenfassen; `braucht-ocr` pro Datei nachfragen (ganzes Dokument geht an Firecrawl), nur bei Ja `--ocr <datei>`; `fehlt` → um PDF bitten.
3. Suchplan aus Hauptfrage, Unterfragen, Hypothesen, Belegpflicht des Kapitels: 8–15 Suchbegriffe inkl. Synonyme DE/EN.
4. Pro Quelle `grep -n -i` über `markdown/<kurzname>.md`, nur Trefferseiten ± 1 lesen, nie ganze Datei.
5. 3–8 Stellen pro Quelle im festen Format nach `02-quellen/fundstellen/Fundstellen_<kurzname>.md`, Zitat wörtlich aus dem Markdown kopiert.
6. Prüfen: `uv run "<Skill-Basisordner>/scripts/fundstellen_pruefen.py" <fundstellen> <markdown>` pro Quelle; Ergebnis zusammenfassen.
7. Kapitel-Auswertung im bisherigen Template, nur geprüfte Stellen, Zitierstil aus Meta-Block.
8. Fortschritt.md, Handoff an Phase 4 (unverändert).

- [ ] **Step 1:** Änderungen vornehmen.
- [ ] **Step 2: Verify** — `grep -n "Gem\b\|Gemini" .claude/skills/studienarbeit-quellenauswertung/SKILL.md` nur noch im Empirik-Strang; `grep -c "—"` in geänderten Dateien nicht höher als vorher; Description-Länge je Skill < 1024 (`python3` Zählung).

### Task 5: Auslieferung synchronisieren und Pakete bauen

**Files:**
- Copy: geänderte `.claude/skills/**` inkl. `scripts/` → `dist/cowork-plugin/skills/**`
- Modify: `dist/master-skill/studienarbeit/references/phase-0-onboarding.md`, `phase-1-planung.md`, `phase-2-recherche.md`, `phase-3-quellenauswertung.md`, `phase-4-writer.md`, `phase-7-finalisierung.md`; `dist/master-skill/studienarbeit/SKILL.md` (Phase-3-Beschreibung); Create `dist/master-skill/studienarbeit/scripts/` (Kopie der drei Skripte); `gem-systemprompt.md`-Kopien wie in Task 4 behandeln.
- Modify: `.claude-plugin/marketplace.json`, `dist/cowork-plugin/.claude-plugin/plugin.json` — 1.4.0; Keywords `gemini` raus, `anydoc` rein.
- Rebuild: `dist/studienarbeit-pipeline.plugin`, `dist/studienarbeit.skill` (Befehle aus `dist/README.md`, alte Datei vorher löschen).

- [ ] **Step 1:** Baseline notieren: `diff -rq .claude/skills dist/cowork-plugin/skills -x .DS_Store -x 'Icon*'` vor den Änderungen.
- [ ] **Step 2:** kopieren und anpassen.
- [ ] **Step 3: Verify** — derselbe diff zeigt nicht mehr als die Baseline; `unzip -l dist/studienarbeit-pipeline.plugin | grep scripts/` und `unzip -l dist/studienarbeit.skill | grep scripts/` listen je 3 Skripte; `python3 -m json.tool` auf beide JSON-Dateien ok.

### Task 6: Echter Durchlauf

- [ ] **Step 1:** Testordner im Scratchpad mit Vault-Struktur, in `02-quellen/dateien/`: ein Open-Access-Zeitschriftenartikel mit Seitenbereich ab > 1, ein Report ab S. 1, eine .docx, ein Bild-PDF; Recherche-Protokoll mit Seitenbereich des Artikels und einem Eintrag ohne Datei.
- [ ] **Step 2:** Umwandeln; für 3 Seiten des Artikels die gedruckte Seitenzahl im PDF (pdftotext/Viewer) mit der Marke vergleichen. Erwartung: identisch, Bild-PDF `braucht-ocr`, Eintrag ohne Datei `fehlt`.
- [ ] **Step 3:** Mit der Beispiel-Forschungsfrage aus `02-quellen/BA_Forschungsfrage.md` Schritte 3–6 für eine Quelle durchspielen, eine Stelle absichtlich verfälschen. Erwartung: `❌ nicht gefunden`.
- [ ] **Step 4:** Ergebnis an Chris; Commit und Push nur nach Go.

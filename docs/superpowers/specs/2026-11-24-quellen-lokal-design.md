# Design: Lokale Quellenauswertung mit anydoc (v1.4.0)

Stand: 2026-11-24. Status: Entwurf, wartet auf Freigabe.

## Warum

Feedback aus Chris' DMs: Die Quellenauswertung (Phase 3) war oft falsch, Studierende mussten viel von Hand nachbessern. Typischer Fehler: falsche Seitenzahlen. Ursache: Die Auswertung läuft in Gemini/NotebookLM, Claude sieht die Quellen nie. v1.3.0 erkennt Seitenfehler nur rechnerisch und lässt die Studierenden jede Stelle per Nachfrage-Prompt selbst klären. Inhaltliche Fehler (Aussage steht so nicht in der Quelle) prüft niemand.

## Ziel

Studierende legen alle Quellen in einen Ordner. Die Pipeline wandelt sie lokal mit anydoc (github.com/firecrawl/anydoc, MIT) in Markdown um. Der Agent durchsucht sie nach Thema, Forschungsfrage, Unterfragen und Hypothesen und liefert pro Quelle die wichtigsten Stellen mit belegter Seitenzahl. Jede Stelle ist wörtlich am Quelltext geprüft.

## Nicht-Ziele

- OCR für gescannte PDFs als Standard (nur auf Nachfrage pro Quelle, siehe unten)
- Änderungen am Empirik-Strang (Interviews, Fragebögen)
- Änderungen an Recherche (Phase 2), Writer, Reviewer außer den nötigen Anschlüssen
- Website-Doku `/docs/study-texter` (lebt im Website-Repo, eigener Schritt)

## Anti-Ziele (wäre ein Fehlschlag, auch wenn es technisch läuft)

- Eine Seitenzahl wird gesetzt, die nicht am Text belegt ist
- Quellen verlassen ohne ausdrückliche Zustimmung den Rechner
- Claude lädt ganze PDFs in den Kontext (Token-Kosten explodieren)
- Studierende müssen wieder Prompts zwischen Tools hin- und herkopieren

## Rahmenbedingungen

- Laufzeit: Claude Desktop-App, Code-Tab (lokaler Ordner + Shell). Chat-Tab wird nicht unterstützt.
- anydoc braucht Python ≥ 3.10, macOS bringt oft nur 3.9 mit. Fertige Pakete gibt es für macOS (Intel, Apple Silicon), Windows x64, Linux.
- anydoc liefert bei PDFs **ein** Markdown ohne Seitengrenzen. Seitenzahlen müssen wir selbst erhalten.
- Die Pipeline wird dreifach ausgeliefert: `.claude/skills/`, `dist/cowork-plugin/skills/`, `dist/master-skill/studienarbeit/references/`. Alle drei müssen synchron bleiben, `.plugin` und `.skill` werden neu gebaut.

## Ansätze

| Ansatz | Was | Abwägung |
|---|---|---|
| **A. Lokal ersetzen (gewählt)** | Phase 3 läuft komplett lokal: anydoc + Claude-Suche + Wortlaut-Check. NotebookLM bleibt für die Recherche (Phase 2). | Behebt die Ursache, keine Tool-Wechsel mehr. Größerer Umbau. Braucht die Dateien lokal. |
| B. Daneben | Gemini-Weg bleibt Standard, lokaler Weg als Option | Weniger Umbau, aber zwei Wege pflegen, Fehlerquelle bleibt Standard |
| C. Nur besser markieren | Gemini prüft seine Stellen selbst nach | Kaum Aufwand, KI prüft KI, Seiten bleiben unsicher |

**Entscheidung:** A. Chris hat am 2026-11-24 entschieden: Phase 3 ersetzen.

## Ablauf (neu)

```
02-quellen/dateien/        ← Studierende legen PDFs, Word, PPT, EPUB ab
        │  quellen_umwandeln.py (anydoc, Seite für Seite)
        ▼
02-quellen/markdown/<kurzname>.md + _index.md
        │  Claude sucht nach FF, Unterfragen, Hypothesen, Belegpflicht
        ▼
02-quellen/fundstellen/Fundstellen_<kurzname>.md   ← pro Quelle
        │  fundstellen_pruefen.py (Wortlaut + Seite)
        ▼
02-quellen/Auswertung_Kapitel_<X>_<Kurztitel>.md   ← bisheriges Writer-Format
```

### 1. Umwandeln (`quellen_umwandeln.py`)

Aufruf: `uv run --with firecrawl-anydoc --with pypdf <skill-dir>/scripts/quellen_umwandeln.py 02-quellen`

- Jede Datei in `dateien/` → `markdown/<kurzname>.md`. Kurzname: Erstautor-Jahr aus Dateiname, sonst Dateiname in kebab-case.
- **PDF:** mit pypdf in Einzelseiten zerlegen, jede Seite einzeln durch `anydoc.to_markdown_bytes`. Vor jede Seite eine Marke: `<!-- seite pdf=7 gedruckt=325 -->`.
- **Gedruckte Seite bestimmen**, in dieser Reihenfolge:
  1. Zahl in den ersten oder letzten zwei Zeilen der Seite (Kopf-/Fußzeile). Gilt nur, wenn über mehrere Seiten ein konstanter Versatz `gedruckt − pdf` herauskommt (mindestens 3 Seiten, Mehrheit gleicher Versatz). Dann wird der Versatz auf alle Seiten angewandt.
  2. Sonst: Seitenbereich aus dem Recherche-Protokoll (Spalte „Seiten"), Versatz = Bereichsanfang − 1, wenn die Seitenzahl des PDFs zur Länge des Bereichs passt.
  3. Sonst: `gedruckt=?`. Zitiert wird dann mit Marker `[SEITE PRÜFEN]`.
- **Word, PPT, EPUB:** ein Dokument ohne Seiten. Zitiert wird mit Abschnitt/Überschrift statt Seite.
- **Gescannte PDFs** (`NeedsOcr`): werden nicht umgewandelt, landen im Bericht. Claude fragt pro Quelle, ob die hosted OCR von Firecrawl genutzt werden darf (Hinweis: das ganze Dokument geht an Firecrawl). Ohne Ja bleibt die Quelle draußen.
- `_index.md`: eine Zeile pro Quelle mit Format, Seitenzahl, Versatz-Herkunft (Kopfzeile / Crossref / unbekannt), Zuordnung zum Recherche-Protokoll, Status.
- Schon umgewandelte Dateien werden übersprungen (Vergleich über Änderungszeit).

### 2. Suchen und auswählen (Claude, im Skill)

- Suchplan aus `Forschungsfrage.md` (Hauptfrage, Unterfragen, Hypothesen) und der Belegpflicht-Liste des Kapitels aus `Gliederung.md`.
- Pro Quelle: erst Stichwortsuche (grep) über das Markdown, dann nur die Trefferseiten mit einer Seite Kontext lesen. Nie ganze Quellen in den Kontext laden.
- Pro Quelle 3 bis 8 wichtigste Stellen, je Stelle: wörtliches Zitat (1–3 Sätze), gedruckte Seite (PDF-Seite), Bezug (FF / Unterfrage / Hypothese / Belegpflicht-Punkt), Funktion (Definition, Beleg, Gegenargument, Zahl), Kapitel.
- Ausgabe: `02-quellen/fundstellen/Fundstellen_<kurzname>.md`.

### 3. Prüfen (`fundstellen_pruefen.py`)

- Für jede Fundstelle: Steht das Zitat wörtlich im Markdown, und zwar auf der angegebenen Seite? Vergleich nach Normalisierung (Leerraum, Silbentrennung am Zeilenende, typografische Anführungszeichen, Ligaturen).
- Ergebnis je Stelle: `✅ belegt`, `⚠️ andere Seite (S. x)` (wird mit Protokoll korrigiert, weil am Text belegt), `❌ nicht gefunden` (Stelle wird gestrichen oder als `[ZITAT PRÜFEN]` markiert, nie still behalten).
- Claude schreibt erst danach die Kapitel-Auswertung.

### 4. Kapitel-Auswertung

Aus den geprüften Fundstellen baut Claude `Auswertung_Kapitel_<X>_*.md` im bisherigen Template (Abschnitte 1–7 + Quellenverzeichnis). Der Writer (Phase 4) bleibt unverändert lesbar. Nur geprüfte Stellen fließen ein.

## Änderungen pro Skill

| Skill | Änderung |
|---|---|
| onboarding | Prüft `uv`, installiert es bei Bedarf (Befehl je Betriebssystem), testet anydoc mit einer Mini-Datei. Hinweis: Code-Tab der Desktop-App nutzen. |
| planung | Optionaler Abschnitt „Hypothesen" in `Forschungsfrage.md` (bei empirischen Arbeiten empfohlen, sonst leitende Annahmen). |
| recherche | Am Ende: Hinweis, die gefundenen Volltexte als Dateien in `02-quellen/dateien/` abzulegen. Sonst unverändert. |
| quellenauswertung | Literatur-Strang neu nach diesem Design. Gem-Setup und Prompts A–F entfallen. Empirik-Strang unverändert. |
| writer | Liest nur geprüfte Stellen, Marker `[ZITAT PRÜFEN]` nie still auflösen. |
| finalisierung | Seiten-Check nutzt den Prüfbericht statt der Rechenregel. |
| CLAUDE.md, README | Phase-3-Beschreibung, Tool-Tabelle (Gemini fällt für Phase 3 weg), Version 1.4.0. |

## Ablage und Datenschutz

- `02-quellen/dateien/`, `02-quellen/markdown/`, `02-quellen/fundstellen/` kommen in `.gitignore` (urheberrechtlich geschützte Texte).
- Keine Netzwerkaufrufe außer `uv`-Installation und opt-in OCR.

## Prüfung (Definition of Done)

- Unit-Tests für Versatz-Erkennung (Kopfzeile, Crossref-Fallback, unbekannt, Bereich ab S. 1) und Wortlaut-Normalisierung.
- Echter Durchlauf mit mindestens: einem Zeitschriftenartikel mit Versatz (z. B. S. 319–340), einem Buchkapitel ab S. 1, einer .docx, einem gescannten PDF. Erwartung: Seiten stimmen mit der gedruckten Seite überein, Scan wird gemeldet.
- Eine absichtlich verfälschte Fundstelle wird als `❌ nicht gefunden` erkannt.
- dist-Kopien synchron (diff leer), `.plugin` und `.skill` neu gebaut und installierbar.

## Entscheidungen nach Builder-Check (Claudes Entscheidungen, von Chris prüfbar)

- **Ohne Shell** (Chat-Tab, Master-Skill ohne Code-Umgebung): Phase 3 stoppt mit dem Hinweis, den Code-Tab der Desktop-App zu öffnen. Kein Gemini-Fallback.
- **OCR:** braucht laut anydoc-README keinen Key (`FIRECRAWL_API_KEY` nur für höhere Limits). Bleibt opt-in pro Datei, kein Key-Handling in v1.4.0.
- **Quellen ohne Datei** (Webseiten, nur in NotebookLM): `_index.md` listet Einträge aus dem Recherche-Protokoll ohne Datei als `fehlt`. Der Skill bittet, Webseiten im Browser per „Drucken → Als PDF" in `dateien/` zu speichern. Ohne Datei keine Fundstellen, die Quelle fließt nicht in die Auswertung ein.

## Dem Builder überlassen

- Genaue Regex für Seitenzahlen in Kopf-/Fußzeilen (römische Ziffern im Vorspann ignorieren)
- Kurzname-Bildung und Zuordnung zum Recherche-Protokoll
- Wo die Skripte im Plugin liegen und wie der Skill sie findet (Skill-Basisordner)

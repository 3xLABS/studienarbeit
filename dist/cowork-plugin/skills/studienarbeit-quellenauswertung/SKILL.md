---
name: studienarbeit-quellenauswertung
description: >
  Phase 3 der Studienarbeit-Pipeline (Hausarbeit bis Masterarbeit): wertet die
  Quellen lokal aus. Der User legt seine Quellen (PDF, Word, PowerPoint, EPUB) in
  02-quellen/dateien/, Claude wandelt sie mit anydoc seitengenau in Markdown um,
  durchsucht sie nach Forschungsfrage, Unterfragen und Hypothesen und liefert pro
  Quelle die wichtigsten Stellen mit gedruckter Seitenzahl. Jedes Zitat wird per
  Skript wörtlich am Quelltext geprüft, Seiten werden nur mit Beleg gesetzt.
  Daraus entsteht die Kapitel-Auswertung im Writer-Format. Bei empirischer
  Komponente zusätzlich ein Empirik-Strang für Interviews, Fragebögen und
  Beobachtungen. Braucht den Code-Tab der Claude Desktop-App. Nutze bei: "Quellen
  auswerten", "Literatur analysieren", "Quellenauswertung", "Fundstellen",
  "Kernaussagen extrahieren", "Seitenzahlen prüfen", "Interviews auswerten",
  "Fragebogen analysieren". Nicht für die Quellensuche, dafür gibt es
  studienarbeit-recherche.
---

# Studienarbeit: Phase 3, Quellenauswertung (lokal)

Die Quellenauswertung läuft **lokal auf dem Rechner des Users**. Claude liest die Quellen selbst, aber nie ganz: Ein Skript wandelt sie in durchsuchbares Markdown mit Seitenmarken um, Claude sucht gezielt und liest nur die Trefferseiten. Ein zweites Skript prüft jedes Zitat wörtlich am Quelltext. So stimmen Seitenzahlen und Wortlaut, ohne dass der User von Hand nachbessern muss.

**Claudes Rolle in Phase 3:**
1. Quellen umwandeln und den Bestand melden
2. Pro Quelle die wichtigsten Stellen zu Forschungsfrage, Unterfragen und Hypothesen finden
3. Jede Stelle prüfen lassen und nur belegte Stellen weitergeben
4. Daraus die Kapitel-Auswertung im Writer-Format bauen

**Grundregeln:**
- Keine Seitenzahl ohne Beleg aus dem Quelltext. Unbelegt heißt `[SEITE PRÜFEN]`.
- Kein Zitat, das das Prüfskript nicht gefunden hat. Nicht gefunden heißt `[ZITAT PRÜFEN]` oder streichen.
- Nie eine ganze Quelle in den Kontext laden. Erst suchen, dann nur Trefferseiten lesen.
- Literaturquellen verlassen den Rechner nicht. Einzige Ausnahme: OCR für gescannte PDFs, nur nach ausdrücklichem Ja des Users pro Datei. (Der Empirik-Strang unten arbeitet bewusst mit Gemini.)

## Übersicht: Workflow

```
02-quellen/dateien/            ← User legt Quellen ab (PDF, Word, PPT, EPUB)
        │  Schritt 2: quellen_umwandeln.py
        ▼
02-quellen/markdown/<kurzname>.md  + _index.md
        │  Schritt 3–4: Suchplan, Stichwortsuche, Trefferseiten lesen
        ▼
02-quellen/fundstellen/Fundstellen_<kurzname>.md
        │  Schritt 5: fundstellen_pruefen.py
        ▼
02-quellen/Auswertung_Kapitel_<X>_<Kurztitel>.md   ← für den Writer (Phase 4)
```

Im Folgenden steht `<SKILL>` für den Ordner, der den Unterordner `scripts/` mit `quellen_umwandeln.py` enthält. Im Plugin ist das der Ordner dieses Skills (`studienarbeit-quellenauswertung/`), im Master-Skill der Ordner `studienarbeit/` mit der Haupt-SKILL.md, nicht `references/`. Im Zweifel: `find ~ -name quellen_umwandeln.py -path "*studienarbeit*" 2>/dev/null | head -1`.

## Ablauf

### Schritt 1: Voraussetzungen prüfen

1. **Shell vorhanden?** Prüfe mit `uv --version`, ob du Befehle ausführen kannst und `uv` installiert ist.
   - Keine Shell (z. B. Chat-Tab): Stopp. Sage dem User: „Die Quellenauswertung läuft im **Code-Tab der Claude Desktop-App**. Öffne dort deinen Arbeitsordner und sag mir dann noch mal Bescheid."
   - Shell da, aber kein `uv`: zurück zum Onboarding (`studienarbeit-onboarding`), dort wird `uv` installiert.
2. Lies:
   - `01-docs/Gliederung.md`: Welches Kapitel wird ausgewertet, welche Belegpflicht-Punkte hat es?
   - `02-quellen/Forschungsfrage.md` (oder `BA_Forschungsfrage.md`): Hauptfrage, Unterfragen, Hypothesen
   - `02-quellen/Recherche_Kapitel_[X]_*.md`: Welche Quellen gehören zum Kapitel, mit Seitenbereich?
3. Liegen Dateien in `02-quellen/dateien/`? Falls nicht:
   > Lege bitte die Volltexte deiner Quellen in den Ordner `02-quellen/dateien/`. Benenne sie nach dem Muster `Nachname Jahr Stichwort.pdf`, z. B. `Mueller 2021 Risikomanagement.pdf`, genau mit Nachname und Jahr wie im Recherche-Protokoll (auch `2021a`, falls dort so). Webseiten speicherst du im Browser über **Drucken → Als PDF speichern**.

### Schritt 2: Quellen umwandeln

```bash
uv run --with firecrawl-anydoc --with pypdf "<SKILL>/scripts/quellen_umwandeln.py" 02-quellen
```

Das Skript wandelt jede Datei in `02-quellen/markdown/<kurzname>.md` um. PDFs werden Seite für Seite umgewandelt; vor jeder Seite steht eine Marke:

```
<!-- seite pdf=7 gedruckt=325 -->
```

`pdf` ist die Seite im PDF-Viewer, `gedruckt` die Seitenzahl, die auf der Seite steht und zitiert wird. Das Skript erkennt sie aus Kopf- und Fußzeilen oder rechnet sie aus dem Seitenbereich im Recherche-Protokoll um. Jede Seite wird einzeln gegengeprüft. Kann es die Zahl für eine Seite nicht belegen (Vorspann, eingeschobene Bildseite, widersprüchliche Zählung), steht dort `gedruckt=?`.

Bereits umgewandelte, unveränderte Dateien werden übersprungen. Den Befehl kannst du also jederzeit wieder laufen lassen.

Lies danach `02-quellen/markdown/_index.md` und fasse für den User zusammen:
- Wie viele Quellen umgewandelt wurden
- **Versatz `unbekannt`:** Hier kann keine Seitenzahl belegt werden. Zitate aus dieser Quelle bekommen `[SEITE PRÜFEN]`. Tipp an den User: den Seitenbereich der Quelle im Recherche-Protokoll ergänzen (Spalte „Seiten"), dann Schritt 2 wiederholen.
- **Versatz `konflikt`:** Der Seitenbereich im Recherche-Protokoll widerspricht den Seitenzahlen in den Kopf- oder Fußzeilen (oft ein Zahlendreher im Protokoll). Alle Seiten bekommen `?`. Bitte den User, den Bereich im Protokoll mit dem PDF abzugleichen und zu korrigieren, dann Schritt 2 wiederholen.
- **Status `braucht-ocr`:** Gescanntes PDF ohne Text. Frage pro Datei:
  > `[Datei]` ist ein Scan ohne Text. Ich kann ihn über den Texterkennungs-Dienst von Firecrawl lesen lassen. Dafür geht **das ganze Dokument** an Firecrawl. Soll ich das machen? Alternativ suchst du eine Textfassung des PDFs.

  Nur bei einem klaren Ja: `uv run --with firecrawl-anydoc --with pypdf "<SKILL>/scripts/quellen_umwandeln.py" 02-quellen --ocr "<Dateiname>"`. OCR-Ergebnisse haben keine Seitenmarken, Zitate daraus bekommen `[SEITE PRÜFEN]`.
- **Abschnitt „Ohne Datei" (`fehlt`):** Quellen aus dem Recherche-Protokoll, zu denen keine Datei gefunden wurde. Bitte den User, sie abzulegen. Ohne Datei werden sie in dieser Phase nicht ausgewertet.

### Schritt 3: Suchplan erstellen

Leite aus Forschungsfrage, Unterfragen, Hypothesen und den Belegpflicht-Punkten des Kapitels einen Suchplan ab:

- 8 bis 15 Suchbegriffe, jeweils auf Deutsch und Englisch (die meisten Fachquellen sind englisch), inklusive Synonymen und Wortstämmen (`risik`, `risk`)
- Zu jedem Begriff: welche Frage oder Hypothese er bedient
- Zeige den Suchplan dem User kurz als Tabelle. Er kann ergänzen, muss aber nicht.

### Schritt 4: Fundstellen pro Quelle auswählen

Für jede Quelle des Kapitels:

1. **Seitenmarken holen:** `grep -n "^<!-- seite" 02-quellen/markdown/<kurzname>.md` liefert die Zeilennummer jeder Seite.
2. **Suchen, ohne Text zu laden:** `grep -n -i -o -E "begriff1|begriff2|…" 02-quellen/markdown/<kurzname>.md | head -80` zeigt nur Zeilennummer und Treffer-Wort, nicht die ganzen Absätze. Ordne jede Zeilennummer der Seitenmarke darüber zu und zähle Treffer pro Seite.
3. **Lesen:** Nur die Seiten mit den meisten Treffern lesen, jeweils von ihrer Seitenmarke bis zur nächsten (Read mit `offset`/`limit`), höchstens 6 Seiten pro Quelle. Nie die ganze Datei.
4. **Auswählen:** 3 bis 8 Stellen pro Quelle, die eine Frage, Unterfrage, Hypothese oder einen Belegpflicht-Punkt am stärksten stützen oder ihm widersprechen. Gegenpositionen gehören dazu.
5. **Schreiben** nach `02-quellen/fundstellen/Fundstellen_<kurzname>.md` in genau diesem Format:

```markdown
# Fundstellen: <Autor> (<Jahr>), <Kurztitel>

**Datei:** [[<kurzname>]]
**Kapitel:** <X>

### Stelle 1
- Zitat: „<1 bis 3 Sätze, Zeichen für Zeichen aus dem Markdown kopiert>"
- Seite: <gedruckt> (PDF <n>)
- Bezug: <FF / FF1 / H2 / Belegpflicht-Punkt>
- Funktion: <Definition | Beleg | Zahl | Gegenargument | Methode>
- Kapitel: <X oder X.Y>
- Check: offen
```

Regeln dafür:
- Das Zitat wird **kopiert**, nie aus dem Gedächtnis formuliert oder geglättet. Fußnotenzeichen darfst du weglassen, Wörter änderst du nicht.
- Mindestens 5 Wörter, sonst kann das Skript nicht prüfen, ob die Stelle eindeutig ist.
- **Keine Auslassungen** (`[…]`, `...`). Brauchst du zwei Teile einer Passage, lege zwei Stellen an.
- Das Zitat steht in **einer** Zeile.
- Die Seite stammt aus der Seitenmarke über der Fundstelle (`gedruckt`). Steht dort `?`, schreibe `? (PDF <n>)`.
- Bei Quellen ohne Seiten (Word, PowerPoint, EPUB) schreibst du statt der Seite den Abschnitt, z. B. `Seite: Abschnitt 3.2 Risikosteuerung`.

### Schritt 5: Fundstellen prüfen

Für jede Fundstellen-Datei:

```bash
uv run "<SKILL>/scripts/fundstellen_pruefen.py" 02-quellen/fundstellen/Fundstellen_<kurzname>.md 02-quellen/markdown/<kurzname>.md
```

Das Skript schreibt das Ergebnis in jede Stelle zurück:
- `✅ belegt`: Zitat steht wörtlich auf der angegebenen Seite
- `⚠️ korrigiert von S. x`: Zitat steht wörtlich, aber auf einer anderen Seite. Die Seite wurde anhand des Quelltexts korrigiert.
- `❌ nicht gefunden [ZITAT PRÜFEN]`: Zitat steht so nicht in der Quelle. Suche die Stelle erneut (Schritt 4) und kopiere den Wortlaut neu. Gelingt das nicht, streiche die Stelle.
- `⚠️ steht auf mehreren Seiten …`: Der Satz kommt mehrfach vor (z. B. Abstract und Fazit), keine Fundstelle passt zur Angabe. Die Seite wird nicht geraten, sondern auf `[SEITE PRÜFEN]` gesetzt. Prüfe die Seitenmarken der genannten PDF-Seiten und trage die richtige ein.
- `❌ zu kurz` / `❌ Auslassung` / `❌ Zitat nicht in einer Zeile`: Zitat verlängern, aufteilen bzw. in eine Zeile mit schließendem Anführungszeichen schreiben und erneut prüfen.
- `Seite: [SEITE PRÜFEN] (PDF n)`: Wortlaut belegt, aber die gedruckte Seitenzahl der Quelle ist unbekannt. Bei Quellen ohne Seitenmarken (Word, EPUB, OCR) setzt das Skript jede Zahlenangabe auf `[SEITE PRÜFEN]`, weil es sie nicht belegen kann.

Fasse das Ergebnis für den User in einem Satz pro Quelle zusammen.

### Schritt 6: Kapitel-Auswertung schreiben

Baue aus den geprüften Fundstellen die Datei `02-quellen/Auswertung_Kapitel_[X]_[Kurztitel].md` im Template unten:

- Nur Stellen mit `✅ belegt` oder `⚠️ korrigiert`. Stellen mit `❌` kommen nicht hinein. Stellen mit `⚠️ steht auf mehreren Seiten` nur mit sichtbarem `[SEITE PRÜFEN]`.
- Direkte Zitate übernimmst du wörtlich aus den Fundstellen, Paraphrasen formulierst du eng an der Fundstelle.
- Jede Aussage trägt Autor, Jahr und Seite im Zitierstil aus dem Meta-Block von `04-fortschritt/Fortschritt.md`.
- `[SEITE PRÜFEN]` bleibt sichtbar stehen und kommt zusätzlich in Abschnitt 7 „Offene Stellen".
- Aspekte ohne passende Fundstelle markierst du mit `[QUELLE ERGÄNZEN]`.
- Verlinke die Fundstellen-Dateien im Quellenverzeichnis (`[[Fundstellen_<kurzname>]]`).

### Schritt 7: Vollständigkeits-Check

Prüfe gegen das Recherche-Protokoll (`02-quellen/Recherche_Kapitel_[X]_*.md`):

- Sind alle als „Relevanz 4–5" markierten Quellen ausgewertet? Fehlt die Datei (`fehlt` im Index), sag es dem User.
- Hat jede Unterfrage und jede Hypothese mindestens eine belegte Stelle? Falls nicht:
  > Für [Aspekt X] fehlen Belege. Du solltest mit dem Recherche-Skill (`studienarbeit-recherche`) nachlegen, bevor wir zum Schreiben übergehen.

### Schritt 8: Fortschritt.md aktualisieren

Trage in `04-fortschritt/Fortschritt.md` ein:
- Phase 3 für Kapitel [X]: „Abgeschlossen"
- Offene Punkte (`[QUELLE ERGÄNZEN]`, `[SEITE PRÜFEN]`, Quellen mit `fehlt` oder `braucht-ocr`)
- Nächster Schritt: Phase 4 (Writer) für dieses Kapitel

## Erwartetes Dateiformat (Template)

Das ist das Format, das der Writer-Skill (Phase 4) erwartet. Die Nachbearbeitung muss sicherstellen, dass das Auswertungsdokument diesem Format entspricht:

```markdown
# Quellenauswertung Kapitel [X]: [Kapiteltitel]

**Forschungsfrage:** [[Forschungsfrage]]
**Gliederung:** [[Gliederung]]
**Recherche-Protokoll:** [[Recherche_Kapitel_X_Kurztitel]]
**Datum:** [YYYY-MM-DD]
**Anzahl ausgewerteter Quellen:** [Anzahl]

## 1. Thematischer Überblick
## 2. Relevante Quellen für dieses Kapitel
## 3. Vergleichende Analyse
## 4. Argumentationsketten
## 5. Forschungslücken und offene Fragen
## 6. Empfehlung für den Kapitelaufbau
## 7. Offene Stellen
## Quellenverzeichnis (Kapitel)
```

## Handoff an Phase 4

Wenn die Auswertung für ein Kapitel abgeschlossen ist:

> Phase 3 (Quellenauswertung) für Kapitel [X] ist abgeschlossen. Die Auswertung liegt unter `02-quellen/Auswertung_Kapitel_[X]_[Kurztitel].md`.
>
> **Nächster Schritt — Phase 4: Schreiben.**
> Sag einfach: „Schreib mir Kapitel [X]" — der Writer-Skill greift auf Forschungsfrage, Gliederung und die Quellenauswertung zurück.

## Empirik-Strang — Auswertung eigener Erhebungen

Falls die Meta-Block in `04-fortschritt/Fortschritt.md` das Flag `empirie: true` enthält, nutzt deine Studienarbeit auch Primärforschung — Interviews, Fragebögen, Beobachtungen, Analysen. Diese Daten müssen parallel zur Literaturauswertung (oder danach) strukturiert ausgewertet werden.

**Aktivierungsbedingung:** Empirik-Strang startet nur, wenn:
1. Meta-Block enthält `empirie: true`
2. Eingabedateien existieren: `02-quellen/Empirik_[Kapitel_X]_Rohdaten.md` (transkribierte Interviews, Fragebogenergebnisse, Codierungstabellen, etc.)
3. Gliederung sieht Empiriekapitel vor (z.B. "Erhebung und Methodik", "Ergebnisse aus Primärforschung")

**Claudes Rolle im Empirik-Strang:**
- Systemanweisung für Gemini bereitstellen (mit methodischem Framework, z.B. Mayring-Paraphrasentechnik für qualitativ, deskriptive Statistik für quantitativ)
- 6 kapitelspezifische Prompts generieren (je 3 für qualitativ, 3 für quantitativ/mixed)
- Gemini-Output nachbearbeiten ins Writer-Format

**Wichtig:** Der User wertet NICHT die Rohdaten selbst in Gemini aus — Gemini bekommt strukturierte Eingabedateien und wendet darauf Analysemethoden an (Codierung, Kategorienbildung, Statistik).

### Empirik-Workflow

```
Claude                          User (im Browser)                Gemini
──────                          ─────────────────                ──────
1. Gem-Systemprompt           User erstellt Gem in Gemini
   (mit Empirik-Framework) +   User lädt Rohdaten-PDF/Datei
   Schritt-für-Schritt     →   ins Gem-Context
   Anleitung

2. Empirik-Prompts            User gibt Prompts ein           → Gemini codiert/kategorisiert/
   (Q1-Q3, S1-S3)         →                                    tabelliert
                                User kopiert Output            →   
3. Nachbearbeitung           ←  User gibt Output an Claude
4. Fertige Auswertung        →  Datei in 02-quellen/Empirik_
```

### Schritt E.1: Rohdaten-Vorbereitung

Der User muss die Rohdaten vorher strukturiert haben (nicht von dir gefordert, aber du weist darauf hin):

- **Interviews:** Transkript in `02-quellen/Empirik_[Kapitel_X]_Interviews_Transkript.md` (mit Sprecherwechsel, Zeilenummern)
- **Fragebögen:** Ergebnistabelle in `02-quellen/Empirik_[Kapitel_X]_Fragebogen_Ergebnisse.md` (z.B. CSV, mit offene/geschlossene Antworten)
- **Beobachtungen:** Protokoll in `02-quellen/Empirik_[Kapitel_X]_Beobachtung_Protokoll.md` (chronologisch, mit Kategorien)

### Schritt E.2: Gem-Systemprompt für Empirik

Der Empirik-Strang läuft weiter in Gemini. So richtet der User den Gem einmalig ein:

> 1. Öffne [gemini.google.com](https://gemini.google.com) und klicke links auf **„Gems"** → **„Neuen Gem erstellen"**
> 2. **Name:** `Empirik-Auswertung`
> 3. **Anweisungen:** den Systemprompt einfügen, den ich dir gleich gebe
> 4. Speichern und deine aufbereiteten Rohdaten (Schritt E.1) als Datei in den Gem-Chat hochladen

Lies (oder generiere zielgerichtet basierend auf der Methode aus der Gliederung):

```
.claude/skills/studienarbeit-quellenauswertung/references/gem-systemprompt-empirik.md
```

Falls die Datei nicht existiert, generiere einen ad-hoc Systemprompt, z.B.:

```
Du bist eine Forschungsmethoden-KI, spezialisiert auf qualitative und quantitative Datenanalyse.
Nutze für QUALITATIVE Daten: Mayring-Paraphrasentechnik oder Kuckartz-Kodierverfahren.
Nutze für QUANTITATIVE Daten: Deskriptive Statistik (Häufigkeiten, Mittelwerte, Standardabweichung).
Nutze für MIXED-METHODS: Ergebnisse triangulieren.
Gib ALLE Ergebnisse mit Begründung, Quellenangabe (Zeilennummer, Fragebogennummer) und wissenschaftlichem Kontext aus.
```

### Schritt E.3: Empirik-Prompts (Q1-Q3, S1-S3)

Generiere konkrete, kapitelspezifische Prompts. Der User kopiert diese in den Gem und erhält strukturierte Outputs.

#### Qualitative Prompts (Q1–Q3)

**Q1 — Offene Codierung**

```
Analysiere die Interviews in [Dateiname] mit offener Kodierung (nach Mayring / Kuckartz).

Gehe Absatz für Absatz durch und extrahiere:
1. Paraphrase (Kernaussage in einer Zeile)
2. Generalisierung (abstrahiert auf Konzeptebene)
3. Code (1–3 Wörter Kategorie)

Gib die Ergebnisse als Tabelle aus: Zeile | Zitat | Paraphrase | Generalisierung | Code

Achte besonders auf [Themen aus Forschungsfrage].
```

**Q2 — Kategorienbildung**

```
Basierend auf den Codes aus Q1: Gruppiere die Codes in Kategorien und Subkategorien.

Gib aus:
1. Kategorie
2. Definition (wozu gehört diese Kategorie?)
3. Anzahl Codes
4. Exemplarische Zitate (mit Zeilennummer)

Format: Markdown-Liste.
```

**Q3 — Thematische Synthese**

```
Erstelle eine thematische Synthese basierend auf den Kategorien aus Q2.

Beschreibe:
1. Zentrale Themen (mit Häufigkeit/Relevanz)
2. Narrativen und Muster
3. Spannungen oder Widersprüche zwischen Interviews
4. Implikationen für [Kapitelthema]

Gib als Markdown-Prosa mit Quellenbelegen aus.
```

#### Quantitative Prompts (S1–S3)

**S1 — Deskriptive Statistik**

```
Analysiere die Fragebogenergebnisse in [Dateiname] deskriptiv.

Für jede Frage berechne:
1. Häufigkeitsverteilung (absolute und prozentual)
2. Bei Skalen: Mittelwert, Standardabweichung, Min/Max
3. Grafische Darstellung (nur Text-ASCII oder Markdown-Tabelle)

Gib jede Frage mit Ergebnissen einzeln aus.
```

**S2 — Filtergruppen-Analyse**

```
Führe eine Filtergruppen-Analyse durch nach [Filterkriterium: z.B. Erfahrung, Alter, Branche].

Vergleiche die Antworten zwischen Gruppen:
1. Unterschied in Häufigkeit/Mittelwert
2. Größe des Unterschieds (z.B. prozentuale Differenz)
3. Mögliche Interpretationen

Tabelle pro Frage: Filtergruppe | Ergebnis | Differenz | Interpretation
```

**S3 — Korrelationen oder Zusammenhänge**

```
Prüfe auf Zusammenhänge zwischen Fragen/Dimensionen in [Dateiname]:

Für jedes Fragenpaar:
1. Gemeinsame Muster erkennen
2. Gegensätzliche Antwortmuster
3. Hypothesenbildung (warum könnte X mit Y korrelieren?)

Tabelle: Frage A | Frage B | Gemeinsames Muster | Stärke | Interpretation
```

### Schritt E.4: Nachbearbeitung Empirik-Output

Wenn der User die Gemini-Outputs zurückbringt:

1. **Formatierung:** Tabellen in sauberes Markdown, ASCII-Grafiken in Markdown-Tabellen
2. **Quellenbelege:** Zeilennummern / Fragebogennummern konsistent halten
3. **Methodenbegründung:** Prüfe, ob Gemini die Methode (Mayring, Kuckartz, deskriptive Statistik) korrekt angewendet hat
4. **Fehlende Analysen:** Falls Gemini eine Methode nicht vollständig ausgeführt hat, schlage einen Nach-Prompt vor
5. **Qualitätsflag:** Markiere mit `[METHODE PRÜFEN]`, falls die Kodierung oder Analyse fragwürdig wirkt
6. **Datei erstellen:** Speichere als `02-quellen/Empirik_Auswertung_Kapitel_[X]_[Kurztitel].md`

### Schritt E.5: Empirik-Auswertung-Template

Das Ausgabedokument sollte folgendes Format haben:

```markdown
# Empirische Auswertung Kapitel [X]: [Kapiteltitel]

**Empirische Methode:** [Qualitativ / Quantitativ / Mixed]
**Forschungsfrage:** [[Forschungsfrage]]
**Kapitel-Focus:** [Welche Aspekte der Forschungsfrage werden durch Empirie untersucht?]

## 1. Datengrundlage
- Quelle(n): [Interview / Fragebogen / Beobachtung / Kombiniert]
- Anzahl Datensätze: [n=...]
- Zeitraum: [wann erhoben?]

## 2. Methodisches Vorgehen
[Beschreibung der Analysemethode]

## 3. Offene Codierung / Deskriptive Statistik
[Tabelle oder Auswertung]

## 4. Kategorienbildung / Filtergruppen-Vergleiche
[Tabelle oder Auswertung]

## 5. Thematische Synthese / Korrelationsanalyse
[Prosa mit Quellenbelegen]

## 6. Implikationen für dieses Kapitel
[Was bedeuten diese Ergebnisse für die Argumentation?]

## 7. Offene Stellen
[`[METHODE PRÜFEN]`, `[QUELLEN ERGÄNZEN]`, etc.]

## Datensätze und Codes
[Anhang mit vollständiger Codierungstabelle / Statistiktabelle]
```

### Schritt E.6: Literatur + Empirie kombinieren

Falls ein Kapitel SOWOHL Literatur-Quellenauswertung (Phase 3, Strang A) ALS AUCH Empirik-Auswertung (Phase 3, Strang E) braucht:

- Literatur-Auswertung und Empirik-Auswertung sind **zwei separate Dateien**
- Der Writer-Skill (Phase 4) nutzt **beide** für das Kapitel — erst Literatur-Fundament, dann Empirik-Ergebnisse, dann Diskussion
- Im Fortschritt.md notieren: Kapitel [X] → Phase 3a (Literatur-Auswertung) ✓ + Phase 3b (Empirik-Auswertung) ✓ → Phase 4 (Writer)

### Zusammenspiel mit anderen Skills (erweitert)

- **Vor Phase 3, Strang E** → User hat Daten erhoben und in `02-quellen/` dokumentiert (nicht Phase 2 — das ist nur Literaturrecherche)
- **Phase 3a (Literatur)** + **Phase 3b (Empirik)** → Können parallel laufen oder sequenziell, je nach Kapitel
- **Nach Phase 3** → `studienarbeit-writer` nutzt BEIDE Auswertungen
- **Beim Review (Phase 5)** → Reviewer prüft korrekte Datenanalyse-Methoden und Quellenintegration

## Zusammenspiel mit anderen Skills

- **Vor Phase 3** → `studienarbeit-recherche` findet die Quellen; der User legt die Volltexte in `02-quellen/dateien/`
- **Nach Phase 3** → `studienarbeit-writer` nutzt die Auswertung und die geprüften Fundstellen als Schreibgrundlage
- **Zurück zu Phase 2** → Bei unzureichender Quellenlage Nachrecherche starten
- **Beim Review (Phase 5)** → Der Reviewer prüft, ob die Quellen korrekt eingearbeitet wurden

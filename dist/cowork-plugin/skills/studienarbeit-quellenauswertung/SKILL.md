---
name: studienarbeit-quellenauswertung
description: >
  Phase 3 der Studienarbeit-Pipeline (Hausarbeit bis Masterarbeit): Leitet den User durch die Quellenauswertung mit Gemini und NotebookLM. Der User hat seine Quellen bereits in einem NotebookLM-Notebook gesammelt (Phase 2). Jetzt öffnet er Gemini im Browser, verknüpft das Notebook, und wertet die Quellen dort mit vorbereiteten Prompts von Claude aus. Claude liefert die Prompts und den Gem-Systemprompt, der User führt alles im Browser durch, und Claude übernimmt die Nachbearbeitung des Gemini-Outputs ins Writer-Format. Falls `empirie: true` in Fortschritt.md: Paralleler Empirik-Strang für Analyse von Interviews, Fragebögen, Beobachtungen. Spart Token, weil die eigentliche Analyse bei Gemini läuft. Nutze bei: "Quellen auswerten", "Literatur analysieren", "was sagen die Quellen zu", "Quellenauswertung", "Literaturanalyse", "Quellen zusammenfassen", "Quellen vergleichen", "was steht in den Papers", "extrahiere die Kernaussagen", "Interviews auswerten", "Fragebogen analysieren", "Empirik auswerten", "erstelle eine Quellenübersicht", "werte die Quellen aus", "Gem erstellen", "Gemini Auswertung". Nicht für Quellensuche — dafür gibt es `studienarbeit-recherche`.
---

# Studienarbeit — Phase 3: Quellenauswertung (via Gemini)

Die Quellenauswertung läuft **nicht in Claude**, sondern in **Gemini** — der User bedient Gemini und NotebookLM selbstständig im Browser. Das spart Token und nutzt Geminis Stärke: über die NotebookLM-Verknüpfung hat Gemini direkten Zugriff auf alle indexierten Quellen.

**Claudes Rolle in Phase 3:**
1. **Vorbereitung:** Gem-Systemprompt bereitstellen, kapitelspezifische Prompts generieren
2. **Nachbearbeitung:** Gemini-Output ins exakte Format bringen, das der Writer-Skill (Phase 4) erwartet

**Claudes Rolle ist NICHT:** Die Quellen selbst zu lesen oder auszuwerten. Das macht Gemini.

## Übersicht: Workflow

```
Claude                          User (im Browser)                Gemini
──────                          ─────────────────                ──────
1. Gem-Systemprompt +           User erstellt Gem in Gemini
   Schritt-für-Schritt      →  User verknüpft NotebookLM     
   Anleitung                    Notebook mit Gemini

2. Kapitel-Prompts           →  User gibt Prompts ein         → Gemini analysiert Quellen
                                                                 anhand des Notebooks
                                User kopiert Markdown-Output  →   
3. Nachbearbeitung           ←  User gibt Output an Claude
4. Fertige Auswertung        →  Datei in 02-quellen/
```

## Ablauf

### Schritt 1: Voraussetzungen prüfen

Bevor du startest, lies:
- `01-docs/Gliederung.md` — Welches Kapitel wird ausgewertet?
- `02-quellen/Forschungsfrage.md` oder `02-quellen/BA_Forschungsfrage.md` — Worauf arbeitet alles hin?
- `02-quellen/Recherche_Kapitel_[X]_*.md` — Welche Quellen liegen vor? (aus Phase 2)

Falls die Recherche für das Kapitel noch nicht abgeschlossen ist → zurück zu Phase 2 (`studienarbeit-recherche`).

### Schritt 2: NotebookLM + Gemini verknüpfen (einmalig)

Das ist der zentrale Schritt — hier verbindet der User seine gesammelten Quellen mit Gemini. Es gibt zwei Wege, und Claude erklärt dem User beide:

#### Weg A: Gem in Gemini erstellen und Notebook verknüpfen (empfohlen)

Gib dem User diese Anleitung:

> **NotebookLM-Quellen mit Gemini verbinden — Schritt für Schritt:**
>
> **Teil 1: Gem erstellen**
> 1. Öffne [gemini.google.com](https://gemini.google.com) in deinem Browser
> 2. Melde dich mit dem **gleichen Google-Konto** an, das du für NotebookLM benutzt
> 3. Klicke links in der Seitenleiste auf **„Gem Manager"** oder **„Gems"**
> 4. Klicke **„Neuen Gem erstellen"** / **„New Gem"**
> 5. **Name:** `BA Quellenauswertung`
> 6. **Anweisungen / Instructions:** Kopiere den Systemprompt, den ich dir gleich gebe, komplett in dieses Feld
> 7. Klicke **„Speichern"** / **„Save"**
>
> **Teil 2: NotebookLM-Notebook verknüpfen**
> 1. Öffne deinen neuen Gem (klicke auf „BA Quellenauswertung" in der Gem-Liste)
> 2. Unten links im Chat-Eingabefeld siehst du einen **+**-Button
> 3. Klicke darauf und wähle **„NotebookLM"** als Quelle
> 4. Wähle dein BA-Notebook aus der Liste
> 5. Jetzt hat Gemini Zugriff auf alle Quellen in deinem Notebook
>
> **Fertig!** Du kannst jetzt im Gem-Chat Fragen zu deinen Quellen stellen, und Gemini antwortet basierend auf den Dokumenten im Notebook.
>
> Bestätige mir, wenn der Gem erstellt und das Notebook verknüpft ist.

Gib dem User dann den Inhalt der Datei `references/gem-systemprompt.md` als Copy-Paste-Block für das Anweisungen-Feld. Lies dazu:

```
.claude/skills/studienarbeit-quellenauswertung/references/gem-systemprompt.md
```

#### Weg B: Direkt in NotebookLM chatten (einfacher, aber weniger steuerbar)

Falls der User den Gem-Weg zu kompliziert findet:

> **Alternative: Direkt in NotebookLM auswerten**
>
> 1. Öffne [notebooklm.google.com](https://notebooklm.google.com)
> 2. Öffne dein BA-Notebook
> 3. Wähle links die Quellen aus, die zu diesem Kapitel gehören (Häkchen setzen)
> 4. Nutze den **Chat** unten, um die Prompts einzugeben, die ich dir gleich gebe
>
> Nachteil: Ohne den Gem-Systemprompt gibt Gemini die Antworten nicht im exakten Auswertungsformat aus. Du musst dann ggf. nachfragen oder Claude macht mehr Nachbearbeitung.

**Empfehlung:** Weg A (Gem), weil der Systemprompt dafür sorgt, dass Gemini die Quellen gleich im richtigen Format auswertet — mit Seitenangaben, Harvard-Zitierung und strukturierten Argumentationsketten.

**Wichtig:** Der Gem und die Notebook-Verknüpfung müssen nur **einmal** eingerichtet werden. Bei weiteren Kapiteln öffnet der User einfach denselben Gem.

### Schritt 3: Kapitelspezifische Prompts generieren

Für jedes Kapitel generierst du **konkrete, fertige Prompts** — keine Platzhalter, sondern mit den tatsächlichen Werten aus Forschungsfrage und Gliederung vorausgefüllt.

Generiere diese Prompts und gib sie dem User als nummerierte Copy-Paste-Blöcke:

#### Prompt A — Kapitelauswertung (Hauptprompt)

Fülle die Platzhalter mit den konkreten Werten des Users:

```
Erstelle eine vollständige Quellenauswertung für Kapitel [X]: "[Kapiteltitel]" meiner Bachelorarbeit.

Die Forschungsfrage lautet: "[Forschungsfrage]"

Dieses Kapitel soll folgende Unterkapitel abdecken:
[Unterkapitel aus Gliederung auflisten]

Gehe alle relevanten Quellen im Notebook durch und werte sie kapitelspezifisch aus. Gib die Antwort als vollständiges Markdown-Dokument aus. Achte besonders auf:
- Kernaussagen mit Seitenangaben
- Verwendbare direkte Zitate
- Argumentationsketten
- Vergleichende Analyse (Gemeinsamkeiten, Widersprüche)
- Konkrete Empfehlung für den Kapitelaufbau
```

#### Prompt B — Definitionen (für Theoriekapitel)

```
Durchsuche alle Quellen nach Definitionen für folgende Begriffe, die in Kapitel [X] zentral sind:

1. [Begriff 1]
2. [Begriff 2]
3. [Begriff 3]

Für jeden Begriff: Alle Definitionen mit Autor, Jahr, Seite. Gemeinsamkeiten, Unterschiede, und eine Empfehlung für die Arbeitsdefinition. Formatiere die Antwort als Markdown.
```

#### Prompt C — Argumentationsketten

```
Baue eine wissenschaftliche Argumentationskette für Kapitel [X]: "[Kapiteltitel]".

Die zentrale These dieses Kapitels: "[These — aus Gliederung/Forschungsfrage ableiten]"

Für jedes Argument: Claim → Reason → Evidence (mit konkreten Quellen und Seitenangaben). Zeige auch Gegenargumente und eine Synthese. Formatiere als Markdown.
```

#### Prompt D — Methodik-Auswertung (nur für Methodenkapitel)

```
Werte die methodenbezogenen Quellen für mein Methodenkapitel aus.

Geplante Methode: [Methode aus Gliederung]

Liefere als Markdown-Dokument:
1. Methodenbeschreibung (mit Seitenangaben)
2. Begründung für den Einsatz bei meiner Forschungsfrage
3. Ablauf/Schritte laut Quellen
4. Gütekriterien
5. Limitationen
6. Alternative Methoden und warum meine Wahl besser ist
```

#### Prompt E — Widersprüche und Forschungslücken

```
Analysiere die Quellen zu Kapitel [X] auf:

1. Wo widersprechen sich Autoren? Wer vertritt welche Position? Welche ist besser belegt?
2. Welche Aspekte von [Kapitelthema] werden NICHT oder nur unzureichend abgedeckt?
3. Gibt es einen erkennbaren Forschungstrend oder Paradigmenwechsel?

Formatiere als Markdown mit klaren Überschriften.
```

#### Prompt F — Diskussionsvorbereitung (nur für Diskussionskapitel)

```
Bereite mein Diskussionskapitel vor:

1. Theorie-Empirie-Abgleich: Welche theoretischen Vorhersagen werden bestätigt/widerlegt?
2. Einordnung in den Forschungsstand
3. Praktische Implikationen und Handlungsempfehlungen
4. Limitationen ähnlicher Studien
5. Offene Fragen und Forschungsbedarf

Immer mit konkreten Quellenbelegen (Autor, Jahr, Seite). Formatiere als Markdown.
```

**Welche Prompts du generierst, hängt vom Kapiteltyp ab:**

| Kapiteltyp | Prompts |
|---|---|
| Theoretischer Rahmen | A + B + C + E |
| Methodik | A + D |
| Ergebnisse | A + C + E |
| Diskussion | A + C + E + F |
| Einleitung | A (nur Überblick) |
| Fazit | A (nur Überblick) |

### Schritt 4: User führt Auswertung in Gemini durch

Gib dem User diese Anleitung:

> **So wertest du die Quellen aus:**
>
> 1. Öffne deinen **BA Quellenauswertung**-Gem in Gemini (gemini.google.com → Gems → BA Quellenauswertung)
> 2. Stelle sicher, dass dein NotebookLM-Notebook verknüpft ist (du siehst es als Kontext-Quelle im Chat)
> 3. Kopiere **Prompt A** und füge ihn in den Chat ein → warte auf die vollständige Antwort
> 4. Gib dann die weiteren Prompts (B, C, D, E, F — je nach Kapitel) **einzeln** ein
> 5. **Wichtig — Markdown-Output sichern:**
>    - Markiere die gesamte Antwort von Gemini und kopiere sie
>    - Oder klicke auf das **Kopieren-Symbol** neben der Antwort
>    - Gib die kopierten Antworten hier bei mir (Claude) ein — ich bringe sie ins richtige Format
>
> **Tipp:** Falls eine Antwort zu lang wird und Gemini abbricht, sage "Fahre fort" oder "Bitte den Rest ausgeben".
>
> **Tipp für NotebookLM-Weg:** Wenn du direkt in NotebookLM arbeitest statt im Gem, kannst du vor dem Chat bestimmte Quellen auswählen (Häkchen setzen), um die Antwort auf die kapitelrelevanten Quellen einzuschränken.

### Schritt 5: Nachbearbeitung (Claude)

Wenn der User den Gemini-Output zurückbringt, machst du Folgendes:

1. **Prüfe die Struktur:** Entspricht der Output dem Format, das der Writer-Skill erwartet? (Siehe Template unten)
2. **Ergänze fehlende Abschnitte:** Falls Gemini einen Abschnitt ausgelassen hat (z.B. Argumentationsketten, Forschungslücken), weise darauf hin und schlage einen Nachfrage-Prompt für Gemini vor
3. **Markierungen setzen:**
   - `[SEITE PRÜFEN]` bei Seitenangaben, die verdächtig rund oder unplausibel wirken
   - `[QUELLE ERGÄNZEN]` bei Aspekten, die keine Quellenabdeckung haben
4. **Formatierung normalisieren:** Harvard-Zitierformat konsistent machen, Obsidian-Wiki-Links ergänzen wo nötig
5. **Quellenverzeichnis prüfen:** Sind alle zitierten Quellen im Verzeichnis am Ende aufgeführt?
6. **Datei erstellen:** Speichere als `02-quellen/Auswertung_Kapitel_[X]_[Kurztitel].md`

**Was Claude in der Nachbearbeitung NICHT tut:**
- Keine neuen Quellen erfinden oder ergänzen
- Keine inhaltlichen Aussagen ohne Quellengrundlage hinzufügen
- Keine Quellen selbst auswerten (das hat Gemini gemacht)

### Schritt 6: Vollständigkeits-Check

Prüfe gegen das Recherche-Protokoll (`02-quellen/Recherche_Kapitel_[X]_*.md`):

- Sind alle als "Relevanz 4–5" markierten Quellen in der Auswertung verarbeitet?
- Gibt es Lücken, die eine Nachrecherche (Phase 2) erfordern?

Falls ja, sage dem User:
> Für [Aspekt X] fehlen Quellen. Du solltest mit dem Recherche-Skill (`studienarbeit-recherche`) nachlegen, bevor wir zum Schreiben übergehen.

### Schritt 7: Fortschritt.md aktualisieren

Trage in `04-fortschritt/Fortschritt.md` ein:
- Phase 3 für Kapitel [X]: "Abgeschlossen"
- Offene Punkte (z.B. `[QUELLE ERGÄNZEN]`-Stellen)
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

- **Vor Phase 3** → `studienarbeit-recherche` sammelt die Quellen im NotebookLM-Notebook (User im Browser)
- **Nach Phase 3** → `studienarbeit-writer` nutzt die Auswertung als Schreibgrundlage
- **Zurück zu Phase 2** → Bei unzureichender Quellenlage Nachrecherche starten (User recherchiert selbst in NotebookLM im Browser)
- **Beim Review (Phase 5)** → Der Reviewer prüft, ob die Quellen korrekt eingearbeitet wurden

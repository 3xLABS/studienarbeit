# Studienarbeiten-Pipeline

Du unterstützt beim Schreiben einer **wissenschaftlichen Arbeit** — egal ob Hausarbeit, Seminararbeit, Studienarbeit, Bachelorarbeit oder Masterarbeit. Dafür stehen **acht spezialisierte Skills** bereit, die als strikt getrennte Phasen zusammenarbeiten. Jede Phase hat klare Voraussetzungen (was muss vorliegen, damit sie starten kann) und einen klar definierten Output (was sie der nächsten Phase übergibt).

**Grundprinzip: Phasen sind nicht austauschbar und nicht durchmischbar.** Der Planungs-Skill sucht keine Quellen. Der Recherche-Skill wertet nichts aus. Der Writer fügt keine neuen Quellen hinzu. Diese Trennung ist Absicht — sie macht die Pipeline robust und nachvollziehbar.

## Arbeitstypen

Die Pipeline passt sich an den Arbeitstyp an. Der Typ wird im **Onboarding** abgefragt und im Meta-Block von `04-fortschritt/Fortschritt.md` gespeichert. Alle Skills lesen diesen Block und passen Tiefe, Umfang und Erwartungen entsprechend an.

| Typ | Seitenumfang | Empirie | Tiefe |
|---|---|---|---|
| Hausarbeit | 10–20 | nein | Reproduktion + leichte Synthese |
| Seminararbeit | 15–25 | selten | Synthese |
| Studienarbeit (FH/HS) | 20–40 | optional | Synthese + ggf. Mini-Empirie |
| Bachelorarbeit | 30–60 | empfohlen | eigenständige Synthese, oft Empirie |
| Masterarbeit | 60–100 | erwartet | eigenständiger Beitrag, fundierte Empirie |

Alle Details und Standardgliederungen pro Typ → `_foundation/arbeitstypen.md`.

## Die acht Phasen

```
┌───────────────────────────────────────────────────────────────────┐
│ Phase 0: Onboarding         → studienarbeit-onboarding            │
│ Phase 1: Planung            → studienarbeit-planung               │
│ Phase 2: Recherche          → studienarbeit-recherche             │
│ Phase 3: Quellenauswertung  → studienarbeit-quellenauswertung     │
│         (Literatur-Strang + Empirik-Strang)                       │
│ Phase 4: Schreiben          → studienarbeit-writer                │
│ Phase 5: Review             → studienarbeit-reviewer              │
│ Phase 6: Überarbeitung      → studienarbeit-ueberarbeitung        │
│ Phase 7: Finalisierung      → studienarbeit-finalisierung         │
└───────────────────────────────────────────────────────────────────┘
```

Die Phasen 2–6 werden **pro Kapitel** durchlaufen und sind dabei oft verschachtelt: Während für Kapitel 3 gerade geschrieben wird (Phase 4), kann für Kapitel 4 schon recherchiert werden (Phase 2).

## Phasen im Detail

### Phase 0 — Onboarding (`studienarbeit-onboarding`)
Prüft die Voraussetzungen: richtiger Ordner, Google-Account für NotebookLM & Gemini, Sub-Skills vorhanden, Internetzugang, bestehender Fortschritt. **Fragt zusätzlich den Arbeitstyp und die Meta-Daten ab** (Hochschule, Fach, Zitierstil, Seitenumfang, Abgabedatum, Empirie geplant ja/nein) und schreibt sie in den Meta-Block von Fortschritt.md.

**Input:** Nichts
**Output:** System-Check-Report, Meta-Block in Fortschritt.md, ggf. automatische Reparatur fehlender Teile

### Phase 1 — Planung (`studienarbeit-planung`)
Inhaltliches Fundament: Themenfindung, Forschungsfrage, Gliederung mit Seitenzahlen (typen-spezifisch — Hausarbeit ohne Methodikkapitel, MA mit Stand-der-Forschung-Kapitel), Ordnerstruktur, Zeitplanung. **Berührt keine Quellen** — das ist explizit Phase 2.

**Input:** Thema (oder gar nichts), Meta-Block aus Phase 0
**Output:** `02-quellen/Forschungsfrage.md`, `01-docs/Gliederung.md`, `03-text/XX-*/`-Ordner, initialisierte `04-fortschritt/Fortschritt.md` mit Zeitplanung
**Tools:** Claude im Dialog

### Phase 2 — Recherche (`studienarbeit-recherche`)
Systematische Quellensuche, kapitelweise. Claude entwickelt die Recherchestrategie und generiert Suchbegriffe. Der User navigiert **selbstständig** zu NotebookLM im Browser und führt Deep Research, schnelle Recherche und manuelles Hinzufügen bekannter Quellen dort durch. Claude dokumentiert alles im Recherche-Protokoll. **Wertet nichts aus** — das ist Phase 3.

**Input:** Forschungsfrage, Gliederung
**Output:** NotebookLM-Notebook mit indexierten Quellen (vom User im Browser verwaltet), `02-quellen/Recherche_Kapitel_[X]_*.md` pro Kapitel
**Tools:** Claude (Strategie + Dokumentation), User bedient NotebookLM selbstständig im Browser

### Phase 3 — Quellenauswertung (`studienarbeit-quellenauswertung`)
Die Quellenauswertung läuft **in Gemini**, nicht in Claude — das spart Token. Claude liefert die Anleitung (Gem-Setup, kapitelspezifische Prompts) und übernimmt die Nachbearbeitung des Gemini-Outputs ins Writer-Format. Der User öffnet **selbstständig** Google AI Studio / NotebookLM im Browser und führt die Prompts dort aus. **Produziert keinen Fließtext** — das ist Phase 4.

**Zwei parallele Stränge:**
- **Literatur-Strang** — Auswertung von Papers, Büchern, Artikeln, Reports (Standard für alle Arbeitstypen)
- **Empirik-Strang** — Auswertung eigener Interviews, Fokusgruppen, Fragebogen-Daten, Beobachtungsprotokolle (nur wenn Empirie geplant; siehe Meta-Block)

Der Empirik-Strang nutzt einen separaten Gem-Systemprompt, der für Transkript-Kodierung (qualitative Inhaltsanalyse nach Mayring/Kuckartz) bzw. Fragebogen-Auswertung (deskriptive und inferenzstatistische Analyse) optimiert ist. Methodische Referenz: `_foundation/empirische-methoden.md`.

**Input:** Recherche-Protokoll + indexiertes NotebookLM-Notebook (Literatur), ggf. Transkripte / Rohdaten (Empirik)
**Output:** `02-quellen/Auswertung_Kapitel_[X]_*.md` (Literatur), `02-quellen/Empirik_Auswertung_Kapitel_[X]_*.md` (Empirik) — beide im Format, das der Writer erwartet
**Tools:** Claude (Anleitung + Nachbearbeitung), User bedient Gemini / Google AI Studio selbstständig im Browser

### Phase 4 — Schreiben (`studienarbeit-writer`)
Schreibt **ein Kapitel pro Lauf** im wissenschaftlichen Stil mit dem im Meta-Block gewählten **Zitierstil** (Harvard / APA / Deutsche Zitierweise / Chicago / MLA) und Obsidian-Wiki-Links. Beachtet Kapiteltyp (Einleitung/Theorie/Methodik/Ergebnisse/Diskussion/Fazit) und Nachbarkapitel. Tiefe und Umfang nach Arbeitstyp aus Meta-Block (Hausarbeit knapper, MA tiefer). **Gate:** Startet nur, wenn die Quellenauswertung vorliegt.

**Input:** Forschungsfrage, Gliederung, Meta-Block, Quellenauswertung (Literatur und/oder Empirik), ggf. Nachbarkapitel
**Output:** `03-text/XX-Kapitel/Kapitel_[X]_[Kurztitel].md` mit Status "Erster Entwurf"
**Tools:** Claude

### Phase 5 — Review (`studienarbeit-reviewer`)
Bewertet Struktur, Argumentation, Quellenarbeit, Sprache, Formalia und (bei empirischen Kapiteln) Methodik aus Professorensicht. Validierung gegen den Muss-Check-Katalog in `_foundation/validierung.md`. Priorisiert Feedback in Muss/Sollte/Optional.

**Input:** Kapitel-Datei + Quellenauswertung + Forschungsfrage + Gliederung + Meta-Block
**Output:** `05-review/Review_Kapitel_[X]_[Kurztitel].md` mit Status-Entscheidung, Status des Kapitels in Fortschritt.md auf "Reviewed"
**Tools:** Claude

### Phase 6 — Überarbeitung (`studienarbeit-ueberarbeitung`)
Arbeitet das Review-Feedback (oder Betreuer-Feedback) systematisch ein. Bewahrt Textidentität, stärkt Argumente, ergänzt Quellen, harmonisiert. Erstellt versionierte Datei.

**Input:** Kapitel-Datei + Review-Datei (oder Betreuer-Feedback)
**Output:** `03-text/XX-Kapitel/Kapitel_[X]_[Kurztitel]_v2.md` mit Änderungsprotokoll, Status "Überarbeitet"
**Tools:** Claude

### Phase 7 — Finalisierung (`studienarbeit-finalisierung`)
Gesamtcheck der Arbeit (roter Faden, Begriffskonsistenz, Übergänge), Erstellung des Literaturverzeichnisses **im im Meta-Block gewählten Zitierstil** aus allen Kapitel-Quellenlisten, Word-Formatierung nach Hochschulvorgaben. Bei Deutscher Zitierweise / Chicago-Notes: Konvertierung der Markdown-Fußnoten (`[^n]`) in echte docx-Fußnoten.

**Input:** Alle reviewten/überarbeiteten Kapitel-Dateien + Formatvorgaben + Titelblatt-Infos + Meta-Block
**Output:** `06-final/studienarbeit_final.docx` + `02-quellen/Literaturverzeichnis_final.md` + Prüfbericht
**Tools:** Claude + docx-js

## Pipeline-Flow

```
Phase 0: Onboarding  (einmal zu Beginn — fragt Arbeitstyp + Meta ab)
        │
        ▼
Phase 1: Planung
        │     ↓ Forschungsfrage + Gliederung + Zeitplan
        ▼
Phase 2: Recherche  ────┐
        │               │  (pro Kapitel)
        ▼               │
Phase 3: Quellenauswertung
   - Literatur-Strang   │
   - Empirik-Strang     │  (nur wenn Empirie geplant)
        │               │
        ▼               │
Phase 4: Writer         │
        │               │
        ▼               │
Phase 5: Reviewer       │
        │               │
        ▼               │
  Muss-Punkte? ──ja─▶ Phase 6: Überarbeitung
        │                     │
       nein                   └──▶ zurück zu Phase 5 (Re-Review)
        │
        ▼
  Alle Kapitel Status "Reviewed" oder "Final"?
        │
        ▼
Phase 7: Finalisierung → studienarbeit_final.docx
```

## Status-Flow eines Kapitels

```
Ausstehend → Erster Entwurf → Reviewed → Überarbeitet → Reviewed → Final
(Planung)     (Writer)        (Reviewer) (Überarbeitung) (Reviewer)  (Finalisierung)
```

- **Ausstehend** — Kapitel ist in der Gliederung, aber noch nichts geschrieben
- **Erster Entwurf** — Writer hat eine v1 produziert
- **Reviewed** — Reviewer hat ein Review geschrieben (die Review-Datei sagt, ob Überarbeitung nötig ist)
- **Überarbeitet** — Überarbeitungs-Skill hat v2 (oder v3, v4) produziert
- **Final** — Finalisierung hat das Kapitel in die Word-Datei übernommen

## Fortschritt.md als geteilter State

Alle Skills lesen und schreiben `04-fortschritt/Fortschritt.md`. Diese Datei ist die **einzige Quelle der Wahrheit** für:

- **Meta-Block** (oben in der Datei) — Arbeitstyp, Hochschule, Fach, Zitierstil, Sprache, Seitenumfang, Abgabedatum, Empirie ja/nein
- Welche Phase der Pipeline gerade läuft
- Welchen Status jedes Kapitel hat
- Welche Muss-Punkte aus Reviews noch offen sind
- Welche `[QUELLE ERGÄNZEN]`-Stellen noch zu füllen sind
- Was als nächstes ansteht
- Soll-/Ist-Vergleich der Zeitplanung

Jeder Skill aktualisiert Fortschritt.md am Ende seines Laufs. Wenn du unsicher bist, wo der User gerade steht, lies diese Datei.

**Format des Meta-Blocks:** Siehe `_foundation/arbeitstypen.md` (letzter Abschnitt).

## Empfohlene Schreibreihenfolge

1. **Theoretischer Rahmen** — legt die begriffliche Grundlage
2. **Methodik** — danach steht die empirische Herangehensweise (nur wenn empirisch)
3. **Ergebnisse** — basierend auf der Methodik
4. **Diskussion** — setzt Theorie und Ergebnisse in Bezug
5. **Einleitung** — braucht den Überblick über die ganze Arbeit
6. **Fazit** — beantwortet die Forschungsfrage auf Basis der Ergebnisse

Einleitung und Fazit **zuletzt**, weil sie erst dann sauber geschrieben werden können, wenn der Kern der Arbeit steht.

## Wann welchen Skill nutzen

| User sagt... | Skill |
|---|---|
| „Alles bereit?" / „Setup" / „kann es losgehen?" | studienarbeit-onboarding |
| „Ich will eine Arbeit schreiben" / „Wo fange ich an?" | studienarbeit-planung |
| „Hilf mir bei der Forschungsfrage" / „Gliederung erstellen" / „Zeitplan" | studienarbeit-planung |
| „Quellen suchen" / „Literatur finden" / „Deep Research" | studienarbeit-recherche |
| „Quellen auswerten" / „was sagen die Papers" / „Kernaussagen extrahieren" | studienarbeit-quellenauswertung |
| „Interviews auswerten" / „Transkripte kodieren" / „Mayring-Auswertung" / „Fragebogen analysieren" | studienarbeit-quellenauswertung (Empirik-Strang) |
| „Schreib mir Kapitel 3" / „Theorieteil schreiben" | studienarbeit-writer |
| „Schau dir mein Kapitel an" / „Review" / „Feedback" | studienarbeit-reviewer |
| „Arbeite das Feedback ein" / „Überarbeite" / „Mein Betreuer hat gesagt..." | studienarbeit-ueberarbeitung |
| „Mach die Arbeit fertig" / „Word-Datei" / „Abgabeversion" | studienarbeit-finalisierung |
| „Wie ist der Stand?" | → Lies `04-fortschritt/Fortschritt.md` |

## Foundation — geteiltes Wissen aller Skills

Im Ordner `.claude/skills/_foundation/` liegen die Single Sources of Truth, die alle Skills lesen:

| Datei | Inhalt |
|---|---|
| `arbeitstypen.md` | Hausarbeit / Seminar / Studienarbeit / BA / MA — Seitenumfang, Tiefe, Standardgliederungen, Meta-Block-Format |
| `wissenschaftlicher-stil.md` | Person, Aktiv/Passiv, Satzbau, Fachsprache, Hedging, Verbotsliste, Kapiteltyp-Spezifika |
| `zitierstile.md` | Harvard, APA 7, Deutsche Zitierweise (Fußnoten), Chicago, MLA — mit Beispielen, Auswahl pro Projekt |
| `argumentationsstrukturen.md` | Linear / dialektisch / deduktiv / induktiv, Claim-Reason-Evidence, Toulmin |
| `anti-ki-muster.md` | KI-typische Schreibmuster (G1–G7) inkl. Wissenschaftsspezifika |
| `empirische-methoden.md` | Qualitative + quantitative + mixed methods, Mayring/Kuckartz/Grounded Theory, Stichproben, Gütekriterien |
| `validierung.md` | Muss-Check-Katalog für den Reviewer (Struktur / Quellen / Stil / KI / Methodik / Ergebnisse / Diskussion / Formalia) |

## Ordnerstruktur

```
[Projektordner]/                   ← Obsidian Vault Root + Git-Repo
├── .claude/
│   ├── CLAUDE.md                  ← Diese Datei (Pipeline-Orchestrierung)
│   └── skills/
│       ├── _foundation/           ← Geteilte Single Sources of Truth
│       ├── studienarbeit-onboarding/SKILL.md
│       ├── studienarbeit-planung/SKILL.md
│       ├── studienarbeit-recherche/SKILL.md
│       ├── studienarbeit-quellenauswertung/SKILL.md
│       ├── studienarbeit-writer/SKILL.md
│       ├── studienarbeit-reviewer/SKILL.md
│       ├── studienarbeit-ueberarbeitung/SKILL.md
│       └── studienarbeit-finalisierung/SKILL.md
├── 01-docs/
│   ├── Gliederung.md              ← Aus Phase 1
│   └── *-Muster.md                ← Vorlagen
├── 02-quellen/
│   ├── Forschungsfrage.md         ← Aus Phase 1
│   ├── Recherche_Kapitel_*.md     ← Aus Phase 2
│   ├── Auswertung_Kapitel_*.md    ← Aus Phase 3 (Literatur-Strang)
│   ├── Empirik_Auswertung_Kapitel_*.md  ← Aus Phase 3 (Empirik-Strang, optional)
│   └── Literaturverzeichnis_final.md    ← Aus Phase 7
├── 03-text/
│   ├── 01-Einleitung/
│   │   ├── Kapitel_1_Einleitung.md       ← v1 aus Phase 4
│   │   └── Kapitel_1_Einleitung_v2.md    ← Aus Phase 6
│   ├── 02-Theoretischer Rahmen/
│   ├── 03-Methodik/               (nur wenn empirisch)
│   ├── 04-Ergebnisse/             (nur wenn empirisch)
│   ├── 05-Diskussion/
│   └── 06-Fazit/
├── 04-fortschritt/
│   └── Fortschritt.md             ← Zentrales Protokoll inkl. Meta-Block
├── 05-review/
│   └── Review_Kapitel_*.md        ← Aus Phase 5
├── 06-final/
│   └── studienarbeit_final.docx   ← Aus Phase 7
└── Prompts.md                     ← Copy-Paste-Prompts für externe Tools
```

## Wichtige Konventionen

- **Zitierstil:** Wird im Onboarding gewählt (Default Harvard) und konsistent durchgehalten. Details pro Stil → `_foundation/zitierstile.md`
- **Obsidian-Wiki-Links:** Quellenangaben im Text verlinken in die Quellenauswertung: `[[Auswertung_Kapitel X#Autor, Jahr|Autor, Jahr]]`. Bei empirischen Belegen: `[[Empirik_Auswertung_Kapitel X#Interviewperson B|Int. B, Abs. 12]]`
- **Fehlende Quellen:** Immer `[QUELLE ERGÄNZEN]` markieren, nie erfinden
- **Unsichere Seitenangaben:** `[SEITE PRÜFEN]` (stammt aus Phase 3, wird vom Writer übernommen)
- **Dateinamen:** `Kapitel_[X]_[Kurztitel].md` in `03-text/[XX-Kapitel]/`, Reviews als `Review_Kapitel_[X]_[Kurztitel].md` in `05-review/`, Versionen mit `_v2`, `_v3`
- **Sprache:** Wissenschaftlich, dritte Person, kein Ich, kein Journalismus (vgl. `_foundation/wissenschaftlicher-stil.md`)
- **Argumentation:** Jeder Absatz mit mindestens einem gestützten Argument (Claim → Reason → Evidence; Details `_foundation/argumentationsstrukturen.md`)
- **Abbildungen:** Platzhalter `[ABBILDUNG X.Y: Beschreibung]` im Text (Nummerierung nach Kapitel)
- **Literaturverzeichnis:** Wird von Phase 7 automatisch im gewählten Zitierstil aus allen Kapitel-Quellenlisten zusammengebaut — Phase 4 pflegt pro Kapitel die `## Verwendete Quellen in diesem Kapitel`-Tabelle
- **Betreuer-Feedback:** Geht direkt in Phase 6 (Überarbeitung), egal in welchem Format
- **Empirie-Anhang:** Interview-Leitfäden, Codiersystem, Rohdatenauszüge, Fragebogen-Original im Anhang der finalen Datei

## Vor der Abgabe

Checkliste für den User:
1. Alle `[QUELLE ERGÄNZEN]`-Stellen geschlossen?
2. Alle `[SEITE PRÜFEN]`-Markierungen verifiziert?
3. Alle `[ABBILDUNG X.Y]`-Platzhalter durch echte Abbildungen ersetzt?
4. Bei empirischen Arbeiten: Anhang vollständig (Leitfaden / Codiersystem / Rohdaten-Auszüge)?
5. Literaturverzeichnis vollständig (Vorwärts- und Rückwärts-Check)?
6. Inhaltsverzeichnis in Word aktualisiert (Rechtsklick → Felder aktualisieren)?
7. Plagiatsprüfung mit Hochschul-Software durchgeführt?
8. Formatierung mit Hochschulvorgaben abgeglichen?
9. Eidesstattliche Erklärung unterschrieben (ab Bachelorarbeit Pflicht, bei Hausarbeiten optional je Hochschule)?

# Studienarbeiten-Pipeline

Ein KI-gestütztes Skill-System für **wissenschaftliche Arbeiten aller Art** — Hausarbeit, Seminararbeit, Studienarbeit, Bachelorarbeit, Masterarbeit. Acht spezialisierte Claude-Skills arbeiten als Pipeline zusammen — von der Themenfindung bis zur abgabefertigen Word-Datei. Die Pipeline passt Tiefe, Umfang, Struktur und Zitierstil dynamisch an den im Onboarding gewählten Arbeitstyp an.

## Überblick

Die Pipeline verteilt die Arbeit auf mehrere Tools, die jeweils das tun, was sie am besten können:

| Tool | Rolle | Wann |
|---|---|---|
| **Perplexity** | Quellenrecherche | Quellen finden (Echtzeit-Websuche mit Quellenangaben) |
| **NotebookLM** | Recherche | Quellen finden und sichten |
| **anydoc** (lokal) | Quellenumwandlung | PDFs, Word, PowerPoint, EPUB seitengenau in durchsuchbares Markdown umwandeln |
| **Gemini** | Empirik-Auswertung | Nur bei eigener Erhebung: Interviews, Fragebögen kodieren |
| **Claude** | Strukturarbeit + Schreiben | Planung steuern, Prompts generieren, Kapitel schreiben, reviewen, überarbeiten |
| **Obsidian** | Übersicht | Ordnerstruktur, Fortschritt, alle Dateien an einem Ort |

**Grundregel:** Perplexity und NotebookLM suchen, Claude wertet lokal aus und schreibt, ein Skript prüft jedes Zitat am Quelltext, Obsidian hält alles zusammen.

## Die acht Skills

### 0. studienarbeit-onboarding
Prüft die Voraussetzungen: richtiger Ordner, Google-Account für NotebookLM & Gemini, Sub-Skills vorhanden, Internetzugang, bestehender Fortschritt.

### 1. studienarbeit-planung
Der Einstiegspunkt. Bringt dich vom groben Thema zur schreibfertigen Ausgangslage: Forschungsfrage, Gliederung mit Seitenzahlen, Quellenrecherche und -auswertung. Orchestriert den Multi-Tool-Workflow und generiert Copy-Paste-Prompts für Perplexity und Gemini.

### 2. studienarbeit-recherche
Systematische Quellensuche, kapitelweise. Claude liefert Strategie und Suchbegriffe, der User arbeitet selbstständig in NotebookLM im Browser.

### 3. studienarbeit-quellenauswertung
Wertet deine Quellen lokal aus. Du legst die Volltexte in `02-quellen/dateien/`, Claude wandelt sie mit anydoc seitengenau um, sucht pro Quelle die wichtigsten Stellen zu Forschungsfrage, Unterfragen und Hypothesen und liefert sie mit gedruckter Seitenzahl. Ein Skript prüft jedes Zitat wörtlich am Quelltext, falsche Seiten werden mit Beleg korrigiert.

### 4. studienarbeit-writer
Schreibt einzelne Kapitel auf Basis von Forschungsfrage, Gliederung und Quellenauswertung. Produziert wissenschaftlichen Fließtext im Harvard-Zitierstil mit Claim-Reason-Evidence-Argumentation. Berücksichtigt Nachbarkapitel und kapiteltyp-spezifische Anforderungen.

### 5. studienarbeit-reviewer
Reviewt ein fertiges Kapitel aus Professorensicht. Bewertet Struktur, Argumentation, Quellenarbeit, Sprache und Formalia. Priorisiert Feedback in Muss/Sollte/Optional.

### 6. studienarbeit-ueberarbeitung
Arbeitet Review- oder Betreuer-Feedback systematisch in das Kapitel ein. Bewahrt die Textidentität, stärkt Argumente, ergänzt Quellen, harmonisiert mit der Gesamtarbeit.

### 7. studienarbeit-finalisierung
Prüft die gesamte Arbeit als Einheit (roter Faden, Begriffe, Zitierung, Übergänge), erstellt das Literaturverzeichnis und formatiert alles als abgabefertige Word-Datei (.docx).

## Gesamtablauf

```
Phase 0: ONBOARDING  → System-Check, Voraussetzungen prüfen
Phase 1: PLANUNG     → Thema → Forschungsfrage → Gliederung → Zeitplan
Phase 2: RECHERCHE   → Quellen suchen (NotebookLM + Perplexity)
Phase 3: AUSWERTUNG  → Quellen lokal umwandeln, Fundstellen finden, Zitate prüfen
Phase 4-6: SCHREIBEN (pro Kapitel wiederholen)
   Writer → Reviewer → Überarbeitung
                          ↓
              Bei Bedarf: Review → Überarbeitung (Zyklus)
Phase 7: FINALISIERUNG → Gesamtcheck → Literaturverzeichnis → Word-Datei
```

## Voraussetzungen

- **Claude Desktop-App**, Code-Tab (die Quellenauswertung führt lokale Skripte aus; der Chat-Tab reicht dafür nicht)
- **uv** (installiert das Onboarding automatisch, holt sich das passende Python selbst)
- **Perplexity** (für Quellenrecherche — kostenlose Version reicht)
- **Google NotebookLM** (kostenlos unter notebooklm.google.com)
- **Obsidian** (kostenlos unter obsidian.md — optional, aber empfohlen)

## Installation

Es gibt mehrere Wege — sortiert von einfach nach maximaler Kontrolle. **Variante A (Marketplace) ist die zuverlässigste und braucht keinen Datei-Download.**

### Variante A: Marketplace (ein Befehl, empfohlen)

Dieses Repo ist ein Claude-Plugin-Marketplace. Du musst keine `.plugin`-Datei herunterladen, suchen oder hineinziehen — zwei Befehle genügen. In **Claude Code** oder im **Cowork-Chat** eingeben:

```
/plugin marketplace add e3xler/studienarbeit
/plugin install studienarbeit-pipeline@studienarbeit
```

Fertig. Du hast jetzt zehn Skills (`studienarbeit-pipeline`, `studienarbeit-onboarding`, `-planung`, `-recherche`, `-quellenauswertung`, `-writer`, `-reviewer`, `-ueberarbeitung`, `-finalisierung`, `humanizer`), die geteilte `_foundation/`-Wissensbasis und einen `/start`-Befehl.

Updates später holst du dir mit:

```
/plugin marketplace update studienarbeit
```

Danach in einer neuen Session einfach sagen:
> „Ich will eine Hausarbeit / Bachelorarbeit / Masterarbeit über [Thema] schreiben."

oder:
> `/start`

### Variante B: Plugin-Datei per Drag-&-Drop (Fallback ohne Marketplace)

Falls du den Marketplace nicht nutzen willst: Lade [`dist/studienarbeit-pipeline.plugin`](dist/studienarbeit-pipeline.plugin) herunter (Rechtsklick → „Datei speichern unter" bzw. auf GitHub „Download raw file"), ziehe sie in den Cowork-Chat und klicke im Preview auf **„Save plugin"**. Wichtig: Die Datei muss die Endung `.plugin` behalten und darf vom Browser nicht entpackt werden — falls dein Browser ein `.zip` daraus macht, einfach wieder in `.plugin` umbenennen.

### Variante C: Einzelner Skill (`.skill`)

Wenn du keinen Plugin-Wust willst, sondern nur einen einzelnen Skill: Lade [`dist/studienarbeit.skill`](dist/studienarbeit.skill) herunter und ziehe die Datei in Cowork → **„Save skill"**. Genau dieselbe Pipeline, aber als ein einziger Skill `studienarbeit`, der intern zwischen den Phasen routet. Die Foundation-Dateien (Arbeitstypen, Zitierstile, Stil, Argumentation, empirische Methoden, Anti-KI-Muster, Validierung) sind als `references/foundation-*.md` enthalten.

### Variante D: Repo klonen (Claude Code oder Cowork mit Vault-Ordner)

Wenn du den Vault-Ordner sowieso lokal brauchst (Obsidian, Git-Versionierung, eigene Anpassungen):

```bash
git clone https://github.com/e3xler/studienarbeit.git
```

Dann:

1. Öffne **Claude Desktop** (Cowork-Mode) oder **Claude Code**
2. Wähle den `studienarbeit/`-Ordner als Arbeitsverzeichnis
3. Fertig — Claude erkennt `.claude/CLAUDE.md` und alle Skills automatisch

Alle Skills liegen in `.claude/skills/`, geteiltes Foundation-Wissen in `.claude/skills/_foundation/`. Variante C ist identisch zu Variante A in Sachen Funktionalität, gibt dir aber zusätzlich die Vault-Struktur als Git-Repo.

### In Obsidian öffnen (optional, für jede Variante)

Öffne den Vault-Ordner als Obsidian-Vault: Obsidian → Vault öffnen → Ordner auswählen.

### Loslegen

Sage Claude einfach:
> „Ich will eine Bachelorarbeit / Hausarbeit / Masterarbeit schreiben."

oder:
> „Hilf mir bei der Forschungsfrage zu [dein Thema]."

Claude startet automatisch den Planungs-Skill.

## Ordnerstruktur

```
studienarbeit/                   ← Obsidian Vault Root + Git-Repo
├── dist/                        ← Vorgebackene Cowork-Pakete
│   ├── studienarbeit-pipeline.plugin   ← Plugin-Variante (alle Skills + /start + Foundation)
│   ├── studienarbeit.skill             ← Einzel-Skill-Variante
│   ├── cowork-plugin/                  ← Plugin-Quellordner
│   └── master-skill/                   ← Master-Skill-Quellordner
├── .claude/
│   ├── CLAUDE.md                ← Pipeline-Orchestrierung (liest Claude automatisch)
│   └── skills/                  ← Alle 8 Skills (werden automatisch erkannt)
│       ├── studienarbeit-onboarding/
│       ├── studienarbeit-planung/
│       ├── studienarbeit-recherche/
│       ├── studienarbeit-quellenauswertung/
│       ├── studienarbeit-writer/
│       ├── studienarbeit-reviewer/
│       ├── studienarbeit-ueberarbeitung/
│       ├── studienarbeit-finalisierung/
│       └── notebooklm/
├── 01-docs/
│   ├── Gliederung.md            ← Deine Gliederung (wird in Phase 1 erstellt)
│   ├── BA-Gliederung-Muster.md  ← Vorlage mit Beispielgliederung
│   └── *-Muster.md              ← Vorlagen für Gliederung/Struktur (typen-spezifisch)
├── 02-quellen/
│   ├── Forschungsfrage.md       ← Deine Forschungsfrage (wird in Phase 1 erstellt)
│   ├── Quellenverzeichnis.md    ← Alle gesammelten Quellen
│   └── Auswertung_KapX_*.md    ← Quellenauswertungen pro Kapitel
├── 03-text/
│   ├── 01-Einleitung/
│   ├── 02-Theoretischer Rahmen/
│   ├── 03-Methodik/
│   ├── 04-Ergebnisse/
│   ├── 05-Diskussion/
│   └── 06-Fazit/
├── 04-fortschritt/
│   └── Fortschritt.md           ← Zentrales Protokoll (geteilter State aller Skills)
├── 05-review/
│   └── Review_Kapitel_*.md      ← Reviews
├── 06-final/
│   └── studienarbeit_final.docx   ← Abgabe-Datei
└── Prompts.md                   ← 17 Copy-Paste-Prompts für alle Tools
```

## Schritt-für-Schritt-Anleitung

### Phase 0: Planung (1–2 Tage)

1. **Starte den Planungs-Skill** — Sage Claude: „Ich will eine Arbeit über [Thema] schreiben"
2. **Forschungsfrage entwickeln** — Claude führt dich durch die Themenfindung und hilft bei der Eingrenzung
3. **Gliederung erstellen** — Claude erstellt eine Gliederung mit Seitenvorgaben pro Kapitel
4. **Quellen recherchieren** — Claude generiert Perplexity-Prompts (siehe `Prompts.md`, Codes P-1 bis P-5). Kopiere die Prompts in Perplexity und sammle 40–80 Quellen
5. **Volltexte ablegen:** Lege die PDFs (oder Word, PowerPoint, EPUB) in `02-quellen/dateien/`, am besten als `Nachname Jahr Stichwort.pdf`. Webseiten im Browser per „Drucken → Als PDF speichern".
6. **Quellen auswerten:** Sage Claude „Quellen auswerten für Kapitel X". Claude wandelt die Dateien um, zeigt dir die wichtigsten Stellen pro Quelle mit Seitenzahl und prüft jedes Zitat am Quelltext.

### Phase 1: Kapitel schreiben

Empfohlene Reihenfolge:
1. Theoretischer Rahmen
2. Methodik
3. Ergebnisse
4. Diskussion
5. Einleitung (braucht den Überblick über die ganze Arbeit)
6. Fazit

Sage Claude pro Kapitel: „Schreib mir Kapitel 2: Theoretischer Rahmen" — der Writer-Skill übernimmt.

### Phase 2: Review

Sage Claude: „Review mein Kapitel 2" — der Reviewer-Skill prüft aus Professorensicht.

### Phase 3: Überarbeitung

Sage Claude: „Arbeite das Feedback ein" — der Überarbeitungs-Skill setzt die Review-Ergebnisse um.

Falls dein Betreuer eigenes Feedback gibt, sage: „Mein Betreuer hat gesagt: [Feedback]" — der Skill übersetzt das in konkrete Verbesserungen.

**Wiederhole Phase 1–3 für jedes Kapitel.**

### Phase 4: Finalisierung

Wenn alle Kapitel mindestens den Status „Überarbeitet" haben:

Sage Claude: „Mach die Arbeit fertig" — der Finalisierungs-Skill prüft den roten Faden, erstellt das Literaturverzeichnis und generiert die Word-Datei.

## Die Prompts.md

Die `Prompts.md` im Wurzelverzeichnis enthält 17 vorbereitete Prompts mit Platzhaltern:

| Code | Tool | Zweck |
|---|---|---|
| P-1 bis P-5 | Perplexity | Themenfindung, Hauptrecherche (80 Quellen), Nachrecherche, URL-Extraktion, Lückenanalyse |
| N-1 bis N-3 | NotebookLM | Setup-Anleitung, Quellenübersicht, Widersprüche finden |
| G-1 bis G-6 | Gemini | Forschungsfrage, Kapitel-Auswertung, Argumentationsketten, Definitionen, Methodik, Diskussion |
| C-1 bis C-5 | Claude | Planung, Kapitel schreiben, Review, Überarbeitung, Finalisierung |

Der Planungs-Skill füllt die `{{PLATZHALTER}}` automatisch mit deinen konkreten Werten aus.

## Fortschritt verfolgen

Die `Fortschritt.md` in `04-fortschritt/` wird von allen Skills automatisch aktualisiert. Sie zeigt:

- Forschungsfrage
- Status der Planungsphasen
- Kapiteltabelle mit Wörtern, Seiten, Datum und Status
- Offene `[QUELLE ERGÄNZEN]`-Stellen
- Nächste Schritte

Status-Flow eines Kapitels:
```
Planung → Erster Entwurf → Reviewed → Überarbeitet → Final
```

Frage jederzeit: „Wie ist der Stand?" — Claude liest die Fortschritt.md und gibt dir eine Übersicht.

## Konventionen

- **Zitierstil:** Harvard, durchgehend (vgl. Müller, 2023, S. 45)
- **Fehlende Quellen:** Werden als `[QUELLE ERGÄNZEN]` markiert, nie erfunden
- **Argumentation:** Jeder Absatz folgt dem Claim-Reason-Evidence-Muster
- **Sprache:** Wissenschaftlich, dritte Person, Präsens/Präteritum
- **Abbildungen:** Platzhalter `[ABBILDUNG X.Y: Beschreibung]` im Text

## Checkliste vor der Abgabe

1. Alle `[QUELLE ERGÄNZEN]`-Stellen geschlossen?
2. Alle `[ABBILDUNG X.Y]`-Platzhalter durch echte Abbildungen ersetzt?
3. Literaturverzeichnis vollständig (Vorwärts- und Rückwärts-Check)?
4. Inhaltsverzeichnis in Word aktualisiert?
5. Plagiatsprüfung mit Hochschul-Software durchgeführt?
6. Formatierung mit Hochschul-Vorgaben abgeglichen?
7. Eidesstattliche Erklärung unterschrieben?

## Was aus PaperOrchestra übernommen ist (v1.2.0)

Drei Mechaniken stammen aus [PaperOrchestra](https://github.com/google-research/paper-orchestra) (Google Cloud AI Research, Apache 2.0), einem Multi-Agent-Framework für Forschungs-Paper. Übernommen sind die Ideen, kein Code:

- **Gliederung als Suchplan** (`studienarbeit-planung`): Einleitung (Makro) und Forschungsstand (Mikro, Cluster mit Grenze und Brücke) getrennt, Belegpflicht-Liste pro Unterkapitel.
- **Quellen-Check** (`studienarbeit-recherche`): Jede Quelle wird gegen Crossref oder Semantic Scholar geprüft, mit Stichtag und Dubletten-Abgleich. Nicht auffindbare Quellen sind nicht zitierfähig.
- **Score-Gate** (`studienarbeit-reviewer` + `studienarbeit-ueberarbeitung`): Reviews vergeben Punkte, eine Überarbeitung mit schlechterem Score wird verworfen, maximal 3 Runden.

**v1.2.1 (nach Testlauf):** Untertitel-Vergleich, Erstautor-Pflicht und AIS-Konferenzbände im Quellen-Check, Status `abweichend` für falsch zugeordnete Quellen, Rausch-Schwelle von 0,5 Punkten im Score-Gate (zwei Reviews desselben Texts lagen 0,4 Punkte auseinander).

**v1.3.0 (Seitenzahlen, nach Nutzer-Feedback):** Der Gem nennt jetzt gedruckte Seite, PDF-Seite und einen wörtlichen Anker. Die Recherche speichert den Seitenbereich aus Crossref. Quellenauswertung und Finalisierung prüfen jede Seitenangabe gegen diesen Bereich und erkennen den typischen PDF-Versatz (PDF-Seite 2 statt gedruckter S. 320). Unsichere Seiten bleiben als `[SEITE PRÜFEN]` markiert, mit fertigem Nachfrage-Prompt für NotebookLM.

**v1.4.0 (lokale Quellenauswertung, nach Nutzer-Feedback):** Phase 3 läuft nicht mehr über Gemini, sondern lokal. [anydoc](https://github.com/firecrawl/anydoc) (Firecrawl, MIT) wandelt die Quellen Seite für Seite in Markdown um, die gedruckte Seitenzahl kommt aus Kopf- oder Fußzeile oder dem Crossref-Seitenbereich. Claude liefert pro Quelle die wichtigsten Stellen zu Forschungsfrage, Unterfragen und neu auch Hypothesen. Ein Prüfskript sucht jedes Zitat wörtlich im Quelltext: Seiten werden nur mit Beleg gesetzt, nicht gefundene Zitate als `[ZITAT PRÜFEN]` markiert. Damit entfällt das manuelle Nachfragen in NotebookLM aus v1.3.0. Gescannte PDFs werden gemeldet und nur nach Zustimmung per OCR gelesen.

## Lizenz

Frei nutzbar für persönliche und akademische Zwecke.

---

Erstellt mit der [Studienarbeiten-Pipeline](https://github.com/e3xler/studienarbeit) von [Chris Eichler (@e3xler)](https://e3xler.com).

---
name: studienarbeit
description: >
  Komplette Pipeline für eine wissenschaftliche Arbeit — Hausarbeit,
  Seminararbeit, Studienarbeit, Bachelorarbeit oder Masterarbeit. Passt sich
  an den Arbeitstyp an (10 bis 100 Seiten, mit oder ohne Empirie). Acht klar
  getrennte Phasen, Multi-Tool-Workflow mit NotebookLM, Gemini und Perplexity,
  durchgängiger wissenschaftlicher Stil mit aktivem Anti-KI-Muster-Check.
  Nutze diesen Skill bei JEDER Anfrage, die mit einer wissenschaftlichen
  Studien-/Abschlussarbeit zu tun hat: "ich will eine Hausarbeit schreiben",
  "Bachelorarbeit planen", "Masterarbeit starten", "Seminararbeit",
  "Forschungsfrage entwickeln", "Gliederung erstellen", "Zeitplan",
  "Quellen suchen", "Literaturrecherche", "Deep Research", "Quellen
  auswerten", "Interviews codieren", "Fragebogen analysieren", "Kapitel
  schreiben", "Theorieteil", "Methodik formulieren", "Fazit schreiben",
  "Einleitung", "Diskussion", "Kapitel reviewen", "Feedback zu meinem Text",
  "Betreuer-Feedback einarbeiten", "Überarbeitung", "Revision", "Arbeit
  finalisieren", "Word-Datei erstellen", "Abgabeversion", "Literatur-
  verzeichnis", "wie ist der Stand", "wo bin ich gerade". Auch wenn der User
  nur ein Kapitel teilt und fragt "schau mal drüber" oder eine Gliederung
  pastet — diesen Skill nutzen.
---

# Studienarbeiten-Pipeline (Master-Skill)

Du unterstützt beim Schreiben einer **wissenschaftlichen Arbeit** — Hausarbeit, Seminararbeit, Studienarbeit, Bachelorarbeit oder Masterarbeit. Dieser Skill bündelt **acht spezialisierte Phasen** in einem einzigen Skill — die Detail-Anleitung pro Phase liegt in `references/`. Lade die Phase, in der du arbeitest, und folge ihrer Anleitung.

**Grundprinzip: Phasen sind nicht austauschbar und nicht durchmischbar.** Die Planungs-Phase sucht keine Quellen. Die Recherche-Phase wertet nichts aus. Der Writer fügt keine neuen Quellen hinzu.

## Wie du diesen Skill benutzt

1. Lies zuerst diese SKILL.md komplett.
2. Bestimme aus der User-Anfrage, welche **Phase** dran ist (Routing-Tabelle unten).
3. Lies die zugehörige Datei in `references/` — sie ist die vollständige Anleitung für diese Phase.
4. Für Grundlagen (Zitierstile, Stil, Argumentation, empirische Methoden, Anti-KI-Muster) lies die `foundation-*.md`-Dateien.
5. Folge der Phasen-Anleitung. Aktualisiere am Ende `04-fortschritt/Fortschritt.md`.
6. Übergib sauber an die nächste Phase, wenn die aktuelle abgeschlossen ist.

## Arbeitstypen

Die Pipeline passt sich an den Arbeitstyp an. Der Typ wird im **Onboarding** abgefragt und im Meta-Block von `04-fortschritt/Fortschritt.md` gespeichert. Alle Phasen lesen diesen Block.

| Typ | Seitenumfang | Empirie | Tiefe |
|---|---|---|---|
| Hausarbeit | 10–20 | nein | Reproduktion + leichte Synthese |
| Seminararbeit | 15–25 | selten | Synthese |
| Studienarbeit (FH/HS) | 20–40 | optional | Synthese + ggf. Mini-Empirie |
| Bachelorarbeit | 30–60 | empfohlen | eigenständige Synthese, oft Empirie |
| Masterarbeit | 60–100 | erwartet | eigenständiger Beitrag, fundierte Empirie |

Details und Standardgliederungen pro Typ → `references/foundation-arbeitstypen.md`.

## Die acht Phasen

```
Phase 0: Onboarding         → references/phase-0-onboarding.md
Phase 1: Planung            → references/phase-1-planung.md
Phase 2: Recherche          → references/phase-2-recherche.md
Phase 3: Quellenauswertung  → references/phase-3-quellenauswertung.md
                              (Literatur-Strang + Empirik-Strang)
Phase 4: Schreiben          → references/phase-4-writer.md
Phase 5: Review             → references/phase-5-reviewer.md
Phase 6: Überarbeitung      → references/phase-6-ueberarbeitung.md
Phase 7: Finalisierung      → references/phase-7-finalisierung.md
```

Die Phasen 2–6 werden **pro Kapitel** durchlaufen.

## Routing — welche Phase bei welcher Anfrage

| User sagt... | Phase | Reference |
|---|---|---|
| "Alles bereit?", "Setup" | 0 | `phase-0-onboarding.md` |
| "Ich will eine Hausarbeit/Bachelorarbeit/Masterarbeit schreiben" | 1 | `phase-1-planung.md` |
| "Forschungsfrage entwickeln", "Gliederung erstellen" | 1 | `phase-1-planung.md` |
| "Quellen suchen", "Literatur finden", "Deep Research" | 2 | `phase-2-recherche.md` |
| "Quellen auswerten", "Interviews codieren", "Fragebogen analysieren" | 3 | `phase-3-quellenauswertung.md` |
| "Schreib mir Kapitel 3", "Theorieteil schreiben" | 4 | `phase-4-writer.md` |
| "Schau dir mein Kapitel an", "Review", "Feedback" | 5 | `phase-5-reviewer.md` |
| "Arbeite das Feedback ein", "Mein Betreuer hat gesagt..." | 6 | `phase-6-ueberarbeitung.md` |
| "Mach die Arbeit fertig", "Word-Datei", "Abgabeversion" | 7 | `phase-7-finalisierung.md` |
| "Wie ist der Stand?" | — | Lies `04-fortschritt/Fortschritt.md` |

## Status-Flow eines Kapitels

```
Ausstehend → Erster Entwurf → Reviewed → Überarbeitet → Reviewed → Final
```

## Fortschritt.md als geteilter State

Alle Phasen lesen und schreiben `04-fortschritt/Fortschritt.md`. Sie enthält:

- **Meta-Block:** Arbeitstyp, Hochschule, Fach, Zitierstil, Seitenumfang, Abgabedatum, Empirie ja/nein
- Phasenstatus
- Kapitelstatus
- Offene Muss-Punkte aus Reviews
- Offene `[QUELLE ERGÄNZEN]`-Stellen
- Soll-/Ist-Vergleich Zeitplanung

## Empirik-Strang (optional)

Wenn der Meta-Block `empirie: true` setzt, läuft in Phase 2 und 3 zusätzlich ein **Empirik-Strang**:

- **Phase 2:** Erhebungsdesign (Interviews, Fragebögen, Beobachtungen) und Datensammlung
- **Phase 3:** Auswertung (Codierung, deskriptive Statistik, Inferenzstatistik) parallel zur Literaturauswertung

Methodische Grundlagen → `references/foundation-empirische-methoden.md`.

## Empfohlene Schreibreihenfolge

1. **Theoretischer Rahmen**
2. **Methodik** (falls relevant)
3. **Ergebnisse**
4. **Diskussion**
5. **Einleitung** (zuletzt)
6. **Fazit** (zuletzt)

## Ordnerstruktur

```
studienarbeit/                     ← Vault-Root
├── 01-docs/Gliederung.md
├── 02-quellen/
│   ├── Forschungsfrage.md
│   ├── Recherche_Kapitel_*.md
│   ├── Auswertung_Kapitel_*.md
│   └── Literaturverzeichnis_final.md
├── 03-text/[01-Einleitung, 02-Theoretischer Rahmen, ...]
├── 04-fortschritt/Fortschritt.md    ← Meta-Block + Phasenstatus
├── 05-review/Review_Kapitel_*.md
└── 06-final/studienarbeit_final.docx
```

## Wichtige Konventionen

- **Zitierstil:** Aus dem Meta-Block. Details und Beispiele in `references/foundation-zitierstile.md` (Harvard, APA, Chicago, MLA, Numerisch).
- **Wissenschaftlicher Stil:** Dritte Person, Claim → Reason → Evidence. Siehe `references/foundation-wissenschaftlicher-stil.md` und `references/foundation-argumentationsstrukturen.md`.
- **Anti-KI-Muster:** Aktiv vermeiden (Negation-Affirmation, Rule of Three, leere Floskeln). Siehe `references/foundation-anti-ki-muster.md`.
- **Empirische Methoden:** `references/foundation-empirische-methoden.md`.
- **Validierung:** Vor jeder Abgabe `references/foundation-validierung.md` konsultieren.
- **Obsidian-Wiki-Links:** `[[Auswertung_Kapitel X#Autor, Jahr|Autor, Jahr]]`
- **Fehlende Quellen:** Immer `[QUELLE ERGÄNZEN]` markieren, nie erfinden
- **Unsichere Seitenangaben:** `[SEITE PRÜFEN]`
- **Sprache:** Wissenschaftlich, dritte Person, kein Ich

## Vor der Abgabe

1. Alle `[QUELLE ERGÄNZEN]`-Stellen geschlossen?
2. Alle `[SEITE PRÜFEN]`-Markierungen verifiziert?
3. Alle `[ABBILDUNG X.Y]`-Platzhalter ersetzt?
4. Literaturverzeichnis vollständig?
5. Inhaltsverzeichnis in Word aktualisiert?
6. Plagiatsprüfung mit Hochschul-Software durchgeführt?
7. Formatierung mit Hochschulvorgaben abgeglichen?
8. Eidesstattliche Erklärung unterschrieben?

---

**Wichtig:** Diese SKILL.md ist die **Routing-Schicht**. Die operative Anleitung pro Phase steht in der jeweiligen `references/phase-N-*.md`. Wenn du eine Phase startest, **lies die Reference komplett** — sie enthält Schritt-für-Schritt-Anweisungen, Prompts und Output-Spezifikationen.

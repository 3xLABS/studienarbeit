---
name: studienarbeit-pipeline
description: >
  Orchestrator-Skill für die Studienarbeiten-Pipeline. Erklärt die acht Phasen
  (Onboarding, Planung, Recherche, Quellenauswertung, Schreiben, Review,
  Überarbeitung, Finalisierung), den Status-Flow eines Kapitels, die fünf
  Arbeitstypen (Hausarbeit, Seminararbeit, Studienarbeit, Bachelorarbeit,
  Masterarbeit) und welche Konventionen für Zitierung, Obsidian-Links und
  Argumentation gelten. Nutze diesen Skill bei Anfragen wie "wie funktioniert
  die Pipeline", "welche Phasen gibt es", "wie ist der Stand", "was kommt als
  Nächstes", "Überblick", "wie hängen die Skills zusammen", "Konventionen",
  "welcher Arbeitstyp", "Hausarbeit vs Bachelorarbeit". Wenn der User klar in
  einer bestimmten Phase ist (z. B. "Forschungsfrage entwickeln", "Kapitel 3
  schreiben", "Review machen"), nutze stattdessen den jeweiligen Phasen-Skill.
---

# Studienarbeiten-Pipeline — Orchestrator

Du unterstützt beim Schreiben einer **wissenschaftlichen Arbeit** — egal ob Hausarbeit, Seminararbeit, Studienarbeit, Bachelorarbeit oder Masterarbeit. Dafür stehen **acht spezialisierte Skills** bereit, die als strikt getrennte Phasen zusammenarbeiten. Jede Phase hat klare Voraussetzungen und einen klar definierten Output.

**Grundprinzip: Phasen sind nicht austauschbar und nicht durchmischbar.** Der Planungs-Skill sucht keine Quellen. Der Recherche-Skill wertet nichts aus. Der Writer fügt keine neuen Quellen hinzu.

## Arbeitstypen

Die Pipeline passt sich an den Arbeitstyp an. Der Typ wird im **Onboarding** abgefragt und im Meta-Block von `04-fortschritt/Fortschritt.md` gespeichert. Alle Skills lesen diesen Block und passen Tiefe, Umfang und Erwartungen entsprechend an.

| Typ | Seitenumfang | Empirie | Tiefe |
|---|---|---|---|
| Hausarbeit | 10–20 | nein | Reproduktion + leichte Synthese |
| Seminararbeit | 15–25 | selten | Synthese |
| Studienarbeit (FH/HS) | 20–40 | optional | Synthese + ggf. Mini-Empirie |
| Bachelorarbeit | 30–60 | empfohlen | eigenständige Synthese, oft Empirie |
| Masterarbeit | 60–100 | erwartet | eigenständiger Beitrag, fundierte Empirie |

Details und Standardgliederungen pro Typ stehen in `_foundation/arbeitstypen.md`.

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

## Wann welchen Skill nutzen

| User sagt... | Skill |
|---|---|
| "Alles bereit?" / "Setup" / "kann es losgehen?" | studienarbeit-onboarding |
| "Ich will eine Hausarbeit/Bachelorarbeit/Masterarbeit schreiben" | studienarbeit-planung |
| "Hilf mir bei der Forschungsfrage" / "Gliederung erstellen" | studienarbeit-planung |
| "Quellen suchen" / "Literatur finden" / "Deep Research" | studienarbeit-recherche |
| "Quellen auswerten" / "Interviews codieren" / "Fragebogen analysieren" | studienarbeit-quellenauswertung |
| "Schreib mir Kapitel 3" / "Theorieteil schreiben" | studienarbeit-writer |
| "Schau dir mein Kapitel an" / "Review" / "Feedback" | studienarbeit-reviewer |
| "Arbeite das Feedback ein" / "Mein Betreuer hat gesagt..." | studienarbeit-ueberarbeitung |
| "Mach die Arbeit fertig" / "Word-Datei" / "Abgabeversion" | studienarbeit-finalisierung |
| "Wie ist der Stand?" | → Lies `04-fortschritt/Fortschritt.md` |

## Status-Flow eines Kapitels

```
Ausstehend → Erster Entwurf → Reviewed → Überarbeitet → Reviewed → Final
```

## Fortschritt.md als geteilter State

Alle Skills lesen und schreiben `04-fortschritt/Fortschritt.md` — sie enthält den **Meta-Block** (Arbeitstyp, Hochschule, Fach, Zitierstil, Seitenumfang, Abgabedatum, Empirie ja/nein) sowie Phasenstatus, Kapitelstatus, offene Muss-Punkte und `[QUELLE ERGÄNZEN]`-Stellen. Wenn du unsicher bist, wo der User steht — lies diese Datei.

## Empirik-Strang (optional)

Wenn der User im Onboarding `empirie: true` gesetzt hat, läuft in Phase 2 und 3 zusätzlich ein **Empirik-Strang**:

- **Phase 2:** Erhebungsdesign (Interviews, Fragebögen, Beobachtungen) und Datensammlung
- **Phase 3:** Auswertung (Codierung, deskriptive Statistik, Inferenzstatistik) parallel zur Literaturauswertung

Methodische Grundlagen stehen in `_foundation/empirische-methoden.md`.

## Empfohlene Schreibreihenfolge

1. **Theoretischer Rahmen**
2. **Methodik** (falls relevant)
3. **Ergebnisse**
4. **Diskussion**
5. **Einleitung** (zuletzt — braucht den Überblick)
6. **Fazit** (zuletzt — beantwortet die Forschungsfrage)

## Wichtige Konventionen

- **Zitierstil:** Aus dem Meta-Block in Fortschritt.md (Harvard, APA, Chicago, …). Details in `_foundation/zitierstile.md`.
- **Wissenschaftlicher Stil:** Dritte Person, keine Floskeln, Claim → Reason → Evidence. Siehe `_foundation/wissenschaftlicher-stil.md` und `_foundation/argumentationsstrukturen.md`.
- **Anti-KI-Muster:** Phase 4 und 6 vermeiden bewusst KI-typische Phrasen (Negation-Affirmation, Rule of Three, leere Floskeln). Siehe `_foundation/anti-ki-muster.md`.
- **Obsidian-Wiki-Links:** Quellenangaben verlinken in die Quellenauswertung: `[[Auswertung_Kapitel X#Autor, Jahr|Autor, Jahr]]`
- **Fehlende Quellen:** Immer `[QUELLE ERGÄNZEN]` markieren, nie erfinden
- **Unsichere Seitenangaben:** `[SEITE PRÜFEN]`
- **Dateinamen:** `Kapitel_[X]_[Kurztitel].md` in `03-text/[XX-Kapitel]/`, Reviews als `Review_Kapitel_[X]_[Kurztitel].md` in `05-review/`, Versionen mit `_v2`, `_v3`
- **Abbildungen:** Platzhalter `[ABBILDUNG X.Y: Beschreibung]`
- **Literaturverzeichnis:** Wird in Phase 7 automatisch aus den Kapitel-Quellenlisten zusammengebaut

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
├── 04-fortschritt/Fortschritt.md     ← Meta-Block + Phasenstatus
├── 05-review/Review_Kapitel_*.md
└── 06-final/studienarbeit_final.docx
```

## Vor der Abgabe

1. Alle `[QUELLE ERGÄNZEN]`-Stellen geschlossen?
2. Alle `[SEITE PRÜFEN]`-Markierungen verifiziert?
3. Alle `[ABBILDUNG X.Y]`-Platzhalter durch echte Abbildungen ersetzt?
4. Literaturverzeichnis vollständig?
5. Inhaltsverzeichnis in Word aktualisiert?
6. Plagiatsprüfung mit Hochschul-Software durchgeführt?
7. Formatierung mit Hochschulvorgaben abgeglichen?
8. Eidesstattliche Erklärung unterschrieben?

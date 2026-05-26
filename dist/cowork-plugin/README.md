# Studienarbeiten-Pipeline (Cowork-Plugin)

Acht spezialisierte Skills, die zusammen jede wissenschaftliche Arbeit begleiten — von Hausarbeit (10 Seiten) bis Masterarbeit (100 Seiten). Die Pipeline passt sich an den Arbeitstyp an (Tiefe, Seitenumfang, Empirik-Strang).

## Arbeitstypen

| Typ | Seitenumfang | Empirie |
|---|---|---|
| Hausarbeit | 10–20 | nein |
| Seminararbeit | 15–25 | selten |
| Studienarbeit (FH/HS) | 20–40 | optional |
| Bachelorarbeit | 30–60 | empfohlen |
| Masterarbeit | 60–100 | erwartet |

## Phasen

| Phase | Skill | Output |
|---|---|---|
| 0 | `studienarbeit-onboarding` | System-Check + Meta-Block (Arbeitstyp, Hochschule, Zitierstil, Empirie ja/nein) |
| 1 | `studienarbeit-planung` | Forschungsfrage, Gliederung, Ordnerstruktur, Zeitplan |
| 2 | `studienarbeit-recherche` | Recherche-Protokoll, NotebookLM-Notebook (+ optional Erhebungsdesign) |
| 3 | `studienarbeit-quellenauswertung` | Auswertung pro Kapitel im Writer-Format (Literatur + Empirik) |
| 4 | `studienarbeit-writer` | Fließtext pro Kapitel |
| 5 | `studienarbeit-reviewer` | Review pro Kapitel aus Professorensicht |
| 6 | `studienarbeit-ueberarbeitung` | Versionierte Überarbeitung (_v2, _v3) |
| 7 | `studienarbeit-finalisierung` | `studienarbeit_final.docx` + Literaturverzeichnis |

Zusätzlich:

- `studienarbeit-pipeline` — Orchestrator-Skill, der die Phasen erklärt und Status-Fragen beantwortet
- `humanizer` — Hilfsskill zum Entfernen KI-typischer Schreibmuster
- `_foundation/` — geteilte Wissensbasis (Arbeitstypen, Zitierstile, Stil, Argumentation, empirische Methoden, Anti-KI-Muster, Validierung) — wird von mehreren Skills referenziert

## Installation

In Cowork: Klick auf die `studienarbeit-pipeline.plugin`-Datei → "Save plugin".

## Externe Tools

- **NotebookLM** (notebooklm.google.com) — Quellenspeicher
- **Gemini / Google AI Studio** — Quellenauswertung (Phase 3)
- **Perplexity** — Quellenrecherche (Phase 2)
- **Obsidian** (optional) — Vault-Ansicht

Claude liefert für jeden externen Schritt fertige Copy-Paste-Prompts.

## Start

> "Ich will eine Hausarbeit / Bachelorarbeit / Masterarbeit über [Thema] schreiben."

oder

> `/start`

## Quelle & Lizenz

[github.com/3xLABS/studienarbeit](https://github.com/3xLABS/studienarbeit) — MIT.

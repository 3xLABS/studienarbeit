# Arbeitstypen — Referenz für die Studienarbeiten-Pipeline

Single Source of Truth für die unterstützten Arbeitstypen. Jeder Skill der Pipeline liest aus `04-fortschritt/Fortschritt.md` (Block `## Meta`), um welchen Typ es geht, und passt sein Verhalten an dieser Referenz aus.

Unterstützte Typen: **Hausarbeit**, **Seminararbeit**, **Studienarbeit**, **Bachelorarbeit**, **Masterarbeit**.

---

## Übersicht

| Typ | Seitenumfang (typisch) | Zeitfenster | Empirie | Tiefe | Quellen-Mindestzahl |
|---|---|---|---|---|---|
| Hausarbeit | 10–20 | 4–8 Wochen | nein (selten Mini-Empirie) | Reproduktion + leichte Synthese | 10–20 |
| Seminararbeit | 15–25 | 6–10 Wochen | nein (vereinzelt) | Reproduktion + Synthese | 15–25 |
| Studienarbeit (FH/HS) | 20–40 | 8–14 Wochen | optional | Synthese, ggf. kleine Empirie | 20–35 |
| Bachelorarbeit | 30–60 | 8–14 Wochen | empfohlen | eigenständige Synthese, oft Empirie | 30–60 |
| Masterarbeit | 60–100 | 16–26 Wochen | erwartet | eigenständiger Beitrag, fundierte Empirie | 60–120 |

Seitenumfänge sind **Erwartungswerte** — die Hochschulvorgabe schlägt immer alle Defaults. Die konkreten Werte stehen in der `Meta` von Fortschritt.md.

---

## Standard-Gliederungen pro Typ

Die Pipeline schlägt typen-spezifische Gliederungs-Templates vor. Sie sind Startpunkte, nicht Vorschriften — die Forschungsfrage bestimmt am Ende die Struktur.

### Hausarbeit / Seminararbeit (rein literaturbasiert)

```
1. Einleitung                              ~10 % der Seitenzahl
   1.1 Problemstellung & Relevanz
   1.2 Zielsetzung & Forschungsfrage
   1.3 Aufbau der Arbeit
2. Theoretische Grundlagen / Stand der Forschung   ~30 %
   2.1 Begriffsklärung
   2.2 Theoretischer Bezugsrahmen
   2.3 Forschungsstand
3. Analyse / Diskussion / Anwendung        ~40 %
   3.1 [Themenfeld A]
   3.2 [Themenfeld B]
   3.3 Synthese
4. Fazit & Ausblick                        ~10 %
Literaturverzeichnis                       ~10 %
Anhang (optional)
```

### Bachelorarbeit (mit Empirie)

```
1. Einleitung                              ~7–10 %
   1.1 Problemstellung & Praxisrelevanz
   1.2 Forschungsfrage(n) & Zielsetzung
   1.3 Aufbau & Vorgehen
2. Theoretische Grundlagen                 ~25–30 %
   2.1 Begriffsklärung
   2.2 Theoretischer Bezugsrahmen
   2.3 Stand der Forschung
3. Methodik                                ~10–15 %
   3.1 Forschungsdesign
   3.2 Datenerhebung
   3.3 Auswertungsverfahren
   3.4 Gütekriterien
4. Ergebnisse                              ~20–25 %
5. Diskussion                              ~15–20 %
   5.1 Einordnung in den Forschungsstand
   5.2 Implikationen für die Praxis
   5.3 Limitationen
6. Fazit & Ausblick                        ~5–8 %
Literaturverzeichnis
Anhang (Interviewleitfäden, Codiersystem, Rohdaten-Auszüge)
```

### Bachelorarbeit (rein literaturbasiert)

Wie oben, aber Methodik schrumpft auf einen Methodenüberblick (Literaturanalyse, Suchstrategie, Auswahlkriterien) und Ergebnisse + Diskussion verschmelzen typisch zu einem Synthesekapitel.

### Masterarbeit

```
1. Einleitung                              ~5–8 %
2. Theoretische Grundlagen                 ~20–25 %
3. Stand der Forschung / Literature Review ~15 %    ← oft eigenes Kapitel
4. Methodik                                ~10–15 %
5. Ergebnisse                              ~20 %
6. Diskussion                              ~15–20 %
7. Fazit & Ausblick                        ~5 %
Literaturverzeichnis
Anhang
```

Bei stark theoretischer MA verschwindet die Methodik und Kapitel 3 wird ein systematisches Literature Review.

---

## Anforderungen pro Typ

### Hausarbeit / Seminararbeit
- Ziel: Vorhandene Theorie auf eine konkrete Frage anwenden
- Kein Anspruch auf Originalbeitrag
- Quellen überwiegend Lehrbücher, Journal-Artikel, Standardwerke
- Eigenleistung = strukturierte Argumentation, klare Begriffsarbeit
- Einleitung + Fazit dürfen knapp sein (1–2 Seiten)

### Studienarbeit
- Im FH-/HS-Kontext oft Vorstufe zur BA, manchmal mit Praxispartner
- Häufig Methoden-Anwendungs-Charakter (Konzeptentwicklung, Fallstudie, Tool-Evaluation)
- Kann empirisch sein, muss aber nicht
- Strukturell mehr Spielraum als BA — Methodik nur, wenn Empirie

### Bachelorarbeit
- Eigenständige Bearbeitung einer Forschungsfrage
- Theoretischer Rahmen + (oft) eigene Empirie
- Methodische Reflexion erwartet (Begründung der Methode, Gütekriterien, Limitationen)
- Originalität in der Frage oder in der Anwendung, nicht zwingend in der Methode
- Diskussion muss Theorie und Empirie zusammenführen

### Masterarbeit
- Substanzieller eigener Forschungsbeitrag
- Vertiefte methodische Reflexion (Methodendiskussion, Triangulation, Gütekriterien)
- Stand-der-Forschung-Kapitel oft als systematischer Review
- Diskussion mit theoretischer Einordnung **und** praktischen Implikationen
- Forschungslücke muss klar benannt und geschlossen werden

---

## Zeitplanungs-Heuristiken

Rückwärtsplanung ab Abgabedatum. Default-Aufteilung:

| Phase | Hausarbeit (6 Wo) | BA (12 Wo) | MA (24 Wo) |
|---|---|---|---|
| Planung & Forschungsfrage | 1 Wo | 1–2 Wo | 2–3 Wo |
| Recherche | 1 Wo | 2 Wo | 4 Wo |
| Quellenauswertung | 1 Wo | 2 Wo | 3–4 Wo |
| Empirie (Erhebung + Auswertung) | — | 3–4 Wo | 6–8 Wo |
| Schreiben | 2 Wo | 3 Wo | 6 Wo |
| Review + Überarbeitung | 0,5 Wo | 1 Wo | 2 Wo |
| Finalisierung & Pufferzeit | 0,5 Wo | 1 Wo | 2 Wo |

Pufferzeit am Ende ist **kein Optionalposten** — Reviewer- und Hochschul-Bürokratie verschlingt typischerweise 1–2 Wochen vor Abgabe.

---

## Handhabung in den Skills

| Skill | Verhalten basierend auf Arbeitstyp |
|---|---|
| `studienarbeit-onboarding` | Fragt Typ ab, schreibt in `04-fortschritt/Fortschritt.md` Meta-Block |
| `studienarbeit-planung` | Wählt passendes Gliederungs-Template, kalkuliert Seiten pro Kapitel |
| `studienarbeit-recherche` | Skaliert Mindest-Quellenzahl pro Kapitel nach Typ |
| `studienarbeit-quellenauswertung` | Aktiviert Empirik-Strang nur, wenn Typ Empirie vorsieht und User sie plant |
| `studienarbeit-writer` | Schreibtiefe + Argumentationskomplexität nach Typ; bei Hausarbeit knapper, bei MA tiefer |
| `studienarbeit-reviewer` | Validierungs-Checks gewichten anders: Hausarbeit ohne Methodik-Block, MA mit hoher Methoden-Tiefe |
| `studienarbeit-finalisierung` | Formatvorgaben oft typ-abhängig (z. B. Eidesstattliche Erklärung erst ab BA) |

---

## Format des Meta-Blocks in Fortschritt.md

Jeder Skill liest oben in Fortschritt.md den Meta-Block. Der Onboarding-Skill legt ihn an, andere Skills aktualisieren bei Bedarf:

```markdown
## Meta

- **Arbeitstyp:** Bachelorarbeit
- **Hochschule:** [Name]
- **Fach / Studiengang:** [BWL / Wirtschaftsinformatik / ...]
- **Lehrstuhl / Betreuung:** [Name]
- **Zitierstil:** Harvard
- **Sprache:** Deutsch
- **Seitenumfang:** 40–50 Seiten (laut Hochschulvorgabe)
- **Abgabedatum:** YYYY-MM-DD
- **Empirie geplant:** Ja — qualitative Interviews (n=8)
- **Forschungsfrage:** [...]
```

Wenn der Block nicht existiert oder unvollständig ist, weisen Skills auf `studienarbeit-onboarding` hin.

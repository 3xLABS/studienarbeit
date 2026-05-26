# Validierung — Muss-Checks für das Review-Gate

Das Pflicht-Raster, das `studienarbeit-reviewer` beim Review eines Kapitels abklopft. Jede Regel = Ja/Nein. „Ja" = bestanden.

**Zielgröße:** ≤ 50 Muss-Checks, unter 2 Minuten Lesezeit. Erweiterte Prüfpunkte stehen im Anhang (kein Muss, nur Nachschlag).

**Typ-Sensitivität:** Kategorien mit [M+] gelten erst ab Masterarbeit, mit [BA+] ab Bachelorarbeit, mit [E] nur bei empirischen Kapiteln. Hausarbeit/Seminararbeit überspringen automatisch Empirik-Checks.

Arbeits-Meta (Typ, Zitierstil, Empirie ja/nein) liest der Reviewer aus `04-fortschritt/Fortschritt.md`, Block `## Meta`.

---

## A. Struktur und Argumentation (6)

- [ ] **A1**: Kapitel-Einleitung benennt, was das Kapitel leistet und wie es zur Forschungsfrage beiträgt?
- [ ] **A2**: Absätze folgen Claim-Reason-Evidence oder einer anderen erkennbaren Argumentationsstruktur (vgl. `argumentationsstrukturen.md`)?
- [ ] **A3**: Übergänge zwischen Abschnitten explizit, kein Themen-Zerfall?
- [ ] **A4**: Kapitel schließt mit Zwischenfazit oder Überleitung zum nächsten Kapitel?
- [ ] **A5**: Aufbau passt zum Kapiteltyp (Einleitung / Theorie / Methodik / Ergebnisse / Diskussion / Fazit)?
- [ ] **A6**: Forschungsfrage wird im Kapitel sichtbar gemacht (direkt oder durch inhaltliche Ausrichtung)?

## B. Quellenarbeit (6)

- [ ] **B1**: Jeder gestützte Claim hat eine Quelle? (Ausnahme: allgemein bekannte Definitionen, eigene Ergebnisse)
- [ ] **B2**: Zitierstil konsistent im gesamten Kapitel (Harvard / APA / Deutsche Zitierweise / Chicago / MLA)?
- [ ] **B3**: Seitenangaben bei Paraphrasen — wo nötig — und bei direkten Zitaten immer?
- [ ] **B4**: Keine erfundenen Quellen? Alle zitierten Quellen lassen sich in der Quellenauswertung nachweisen?
- [ ] **B5**: Keine `[QUELLE ERGÄNZEN]`- oder `[SEITE PRÜFEN]`-Platzhalter mehr im finalen Stand (gilt ab Review-Runde 2)?
- [ ] **B6**: Direkte Zitate maßvoll eingesetzt (nicht mehr als ca. 10 % des Kapitels)?

## C. Sprache und Stil (7)

Vollständiger Katalog: `_foundation/wissenschaftlicher-stil.md`.

- [ ] **C1**: Dritte Person, keine Ich-Form (außer explizit erlaubt)?
- [ ] **C2**: Sätze mehrheitlich < 25 Wörter, keine Endlos-Hypotaxen?
- [ ] **C3**: Satzrhythmus variiert — kein Monotonie-Plateau?
- [ ] **C4**: Fachbegriffe bei Ersterwähnung eingeführt, danach konsistent?
- [ ] **C5**: Keine Umgangssprache, kein Journalismus-Ton, keine rhetorischen Fragen?
- [ ] **C6**: Hedging dosiert (max. 1–2 Hedges pro Absatz)?
- [ ] **C7**: Keine Absolutismen („immer", „nie", „alle") ohne Beleg?

## D. Anti-KI-Muster (6)

Vollständiger Katalog: `_foundation/anti-ki-muster.md` (G1–G7).

- [ ] **D1** (G1): Keine Negation-Affirmation, Rule-of-Three-Ketten, „Von-X-bis-Y"-Formeln?
- [ ] **D2** (G2): Keine Superficial Analysis (Subjekte, die „unterstreichen"/„verdeutlichen")?
- [ ] **D3** (G3): Kein Puffery („zentrale Rolle", „revolutionär", „wegweisend")?
- [ ] **D4** (G4): Kein Synonym-Hopping für denselben Fachbegriff?
- [ ] **D5** (G5): Max. 1–2 AI-Vokabeln pro Absatz (kultivieren, verkörpern, ganzheitlich)?
- [ ] **D6** (G7): Keine wissenschaftsspezifischen KI-Muster (Pseudo-Literaturüberblick, schwammige Forschungslücke, abstraktes Fazit)?

## E. Methodik [BA+ bei Methodikkapitel / E wenn empirisch] (6)

Vollständige Referenz: `_foundation/empirische-methoden.md`.

- [ ] **E1** [E]: Forschungsdesign (qual/quant/mixed) mit Begründung?
- [ ] **E2** [E]: Datenerhebung reproduzierbar beschrieben (Instrument, Sampling, Durchführung)?
- [ ] **E3** [E]: Auswertungsverfahren mit Quelle (Mayring, Kuckartz, statistischer Test)?
- [ ] **E4** [E]: Gütekriterien explizit benannt (qual. nach Mayring/Lincoln&Guba, quant. Objektivität/Reliabilität/Validität)?
- [ ] **E5** [E]: Forschungsethik / Datenschutz / Einwilligung angesprochen?
- [ ] **E6** [E]: Stichprobengröße zum Arbeitstyp passend (vgl. `arbeitstypen.md`)?

## F. Ergebnisse [E wenn empirisch] (4)

- [ ] **F1** [E]: Ergebnisse deskriptiv dargestellt, nicht interpretierend?
- [ ] **F2** [E]: Tabellen und Abbildungen nummeriert, mit Titel und Quelle?
- [ ] **F3** [E]: Bei qualitativen Daten: ankernde Zitate mit Fundstellenverweis (z. B. `[Int. B, Abs. 12]`)?
- [ ] **F4** [E]: Bei quantitativen Daten: Testwerte, p-Werte, Effektstärken korrekt berichtet?

## G. Diskussion [BA+ bei Diskussionskapitel / E wenn empirisch] (4)

- [ ] **G1**: Ergebnisse in den Forschungsstand eingeordnet (Bestätigung / Widerspruch / Erweiterung)?
- [ ] **G2**: Theoretische und praktische Implikationen getrennt diskutiert?
- [ ] **G3**: Limitationen ehrlich benannt (Stichprobe, Methode, Generalisierbarkeit)?
- [ ] **G4**: Ausblick konkret — keine Allgemeinplätze wie „weitere Forschung ist nötig"?

## H. Formalia (5)

- [ ] **H1**: Kapitel-Überschriften-Hierarchie sauber (max. 3 Ebenen, nichts übersprungen)?
- [ ] **H2**: Abkürzungen bei Ersterwähnung ausgeschrieben?
- [ ] **H3**: Zahlen korrekt gesetzt (1–12 ausgeschrieben, Ziffern ab 13, außer Jahreszahlen/Maße/Statistik)?
- [ ] **H4**: Typografische Zeichen korrekt („..." für deutsches Zitat, – mit Leerzeichen für Gedankenstrich)?
- [ ] **H5**: Kapiteldatei hat gepflegten Abschnitt „## Verwendete Quellen in diesem Kapitel" mit vollständigen Zitaten?

---

**Summe (vollständig):** 44 Muss-Checks (Hausarbeit/Seminar: ~32 nach Skip der Empirik-Blöcke; BA mit Empirie: ~44; MA mit Empirie: ~44).

---

## Ergebnisformat (für Review-Datei)

```
## Validierungsergebnis: Kapitel {X} — {Kurztitel}

**Datum:** {YYYY-MM-DD}
**Reviewer:** Claude (studienarbeit-reviewer)
**Kapiteltyp:** {Einleitung / Theorie / Methodik / Ergebnisse / Diskussion / Fazit}
**Gesamtergebnis:** 🟢 Freigegeben / 🟡 Überarbeitung nötig / 🔴 Grundlegend überarbeiten

### Muss-Punkte (kritisch)
- ...

### Sollte-Punkte (verbessern)
- ...

### Optional (wenn Zeit)
- ...

### Befunde-Tabelle
| Regel | Status | Anmerkung |
|---|---|---|
| A1 | 🟢/🟡/🔴 | {Beschreibung} |
```

**Ampel-Logik:**
- 🟢 **Freigegeben** — keine 🔴, max. 2 🟡. Kapitel geht direkt in Finalisierung
- 🟡 **Überarbeitung nötig** — 3+ 🟡 oder 1–2 🔴. Kapitel geht an `studienarbeit-ueberarbeitung`
- 🔴 **Grundlegend überarbeiten** — 3+ 🔴 oder A-/B-Kategorie unvollständig. Kapitel muss umfassend überarbeitet werden, danach Re-Review

---

## Anhang — Erweiterte Prüfpunkte (nur Nachschlag)

**Argumentations-Details:** Jeder Absatz enthält mindestens einen belegten Claim · Gegenpositionen explizit diskutiert (nicht verschwiegen) · Zirkelschlüsse vermieden · keine Strohmann-Argumente · keine Ad-populum-Formulierungen.

**Sprache-Details:** Nominalisierungs-Cluster dosiert (max. 1 pro Satz) · Gedankenstrich nicht übernutzt · keine „hier klicken"-/„siehe oben"-Verweise ohne Kapitelangabe · Konjunktiv sparsam.

**Quellen-Details:** Primärquellen bevorzugt, Sekundärzitate nur wenn unvermeidbar · bei mehreren Autor:innen konsistente Schreibweise · Online-Quellen mit Abrufdatum · graue Literatur als solche kenntlich.

**Formale Details:** Abbildungen mit Alt-Text-Beschreibung im Markdown · Tabellen im Markdown korrekt formatiert · Obsidian-Wiki-Links funktionieren (kein Dead Link) · Kapitel-Dateiname passt zum Kapitelnummerierung.

**Empirie-Details:** Anhang-Verweise funktionieren (Interviewleitfaden, Codiersystem, Rohdaten-Auszug) · Transkript-Konventionen konsistent · Pseudonymisierung durchgängig · Trennung Erhebung vs. Auswertung klar.

**Zitierstil-Details:** Bei Deutscher Zitierweise: alle Fußnoten korrekt nummeriert, Kurzbelege nach Ersterwähnung · Sammelwerk-Beiträge mit Herausgeber:innen-Nennung · Auflagenangabe konsistent.

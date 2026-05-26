# Anti-KI-Muster — Pattern-Katalog für wissenschaftliche Arbeiten

Single Source of Truth für KI-typische Schreibmuster, die akademische Texte maschinell wirken lassen. Der Writer vermeidet diese präventiv, der Reviewer sucht nach ihnen, der Überarbeitungs-Skill räumt sie weg.

Wissenschaftliche Texte tolerieren einen gewissen „KI-Geruch" noch weniger als andere Genres — die Prüfung der Arbeit durchläuft oft KI-Detektion und inhaltliche Plagiatsprüfung. Deshalb sind die Muster hier etwas strenger kuratiert als in allgemeinen Stil-Ratgebern.

---

## G1 — Strukturelle Patterns

| Pattern | BAD | FIX |
|---|---|---|
| **Negation-Affirmation** | „Es handelt sich nicht um X. Es handelt sich um Y." | Direkt sagen, was es ist |
| **Nicht-nur-sondern-auch** | „Die Methode spart nicht nur Zeit, sondern auch Ressourcen." | Auftrennen: „Die Methode spart Zeit und Ressourcen." |
| **Rule of Three** | „effizient, skalierbar und nachhaltig" | Auf den Kern reduzieren |
| **Von-X-bis-Y** | „Von der Datenerhebung bis zur Auswertung" | Konkret werden — welche Schritte genau? |
| **False Range** | „von kleinen Unternehmen bis zu Konzernen" | Wenn kein echtes Spektrum: streichen |
| **Challenges-and-Future** | „Trotz dieser Herausforderungen bleibt das Feld optimistisch" | Streichen oder mit Belegen konkretisieren |
| **Section Summary** | „Zusammenfassend lässt sich sagen ..." (im Fließtext) | Streichen oder präzisieren. Im Fazit ausnahmsweise erlaubt |
| **Didaktischer Disclaimer** | „Es ist wichtig zu beachten, dass ..." | Einfach sagen, was relevant ist |
| **Punkte-statt-Kommas** | „Sechs Monate. Achtundvierzig Seiten. Eine Forschungsfrage." | Kommas verwenden, wissenschaftlicher Stil |

---

## G2 — Superficial Analysis

Unbelebte Subjekte, die Dinge „unterstreichen", „verdeutlichen", „hervorheben". In wissenschaftlichen Texten besonders auffällig.

```
BAD: „Diese Entwicklung unterstreicht die Bedeutung ..."
BAD: „Das Ergebnis verdeutlicht den Wandel ..."
BAD: „Die Zahlen heben hervor, dass ..."
```

**Fix:** Sag was Sache ist. Keine abstrakte Metaebene.

```
FIX: „Die Entwicklung zeigt: [konkrete Aussage mit Beleg]."
FIX: „Die Auswertung ergibt einen Rückgang von 47 % zwischen 2018 und 2023 (vgl. Müller 2024, S. 17)."
```

**Grep-Pattern:** `unterstreicht|verdeutlicht|hebt hervor|beleuchtet|betont`

**Besonders häufig** in KI-Generierung von Zusammenfassungs- und Diskussionskapiteln.

---

## G3 — Puffery und Bedeutungsinflation

Bedeutungs-Aufblähung ohne Substanz. In wissenschaftlichen Arbeiten ein Killkriterium — das klingt nach Pressetext, nicht nach Forschung.

```
BAD: „spielt eine zentrale / entscheidende / pivotale Rolle"
BAD: „von entscheidender Bedeutung"
BAD: „prägt nachhaltig", „hinterlässt bleibenden Eindruck"
BAD: „revolutionär", „bahnbrechend", „wegweisend"
BAD: „Testament für ...", „symbolisch für ..."
```

**Fix:** Weglassen. Wenn etwas wichtig ist, zeigt es sich durch Fakten und Quellen.

```
FIX (streichen, oder:) „60 % der befragten Unternehmen setzen das Verfahren bereits ein (vgl. ...)."
```

**Grep-Pattern:** `entscheidende Rolle|zentrale Rolle|pivotale Rolle|von entscheidender Bedeutung|revolutionär|bahnbrechend|wegweisend|Testament`

---

## G4 — Elegant Variation (Synonym-Hopping)

Künstliches Synonym-Hopping, um Wiederholung zu vermeiden. In der Wissenschaftssprache ist **Klarheit wichtiger als Variation** — Wiederholung eines Fachbegriffs ist nicht nur erlaubt, sondern geboten.

```
BAD: „Die Anforderung ... Das Requirement ... Die Spezifikation ..."
BAD: „Das Unternehmen ... Die Firma ... Die Organisation ..."
BAD: „Der Kunde ... Der Klient ... Der Auftraggeber ..."
```

**Fix:** Beim selben Begriff bleiben. Definierter Fachbegriff bleibt konstant.

```
FIX: „Die Anforderung ... Die Anforderung ... Die Anforderung ..."
```

**Warum LLM-only erkennbar:** Erfordert semantisches Verständnis der Synonym-Äquivalenz im jeweiligen Kontext.

---

## G5 — AI-Vokabular

Wörter, die LLMs überproportional häufig verwenden. Eine Einzelerwähnung ist harmlos, mehrere davon in einem Kapitel sind ein starkes KI-Signal.

### Verben
`unterstreichen, hervorheben, verdeutlichen, aufzeigen, beleuchten, betonen, fördern, kultivieren, prägen, verkörpern, navigieren (als Metapher)`

### Adjektive
`entscheidend, zentral, pivotal, maßgeblich, nachhaltig (im übertragenen Sinn), vielschichtig, komplex, intrinsisch, ganzheitlich, facettenreich`

### Bedeutungs-Aufblähung
`„ist ein Testament für", „steht symbolisch für", „verkörpert den Geist von"`

### Transitions
`„Trotz dieser Herausforderungen", „Zusammenfassend", „Insgesamt", „Abschließend lässt sich sagen", „Es bleibt abzuwarten"`

### Hedging-Floskeln
`„Es ist wichtig zu beachten", „Man sollte nicht vergessen", „Nicht zu unterschätzen ist"`

**Grep-Pattern:** `kultivieren|verkörpern|vielschichtig|intrinsisch|ganzheitlich|facettenreich|navigieren durch`

**Regel:** Max. 1–2 dieser Begriffe pro Absatz. Alles darüber wirkt maschinell.

---

## G6 — Rhythmus und Konkretheit

Gesamtrhythmus eines Texts — erkennt man nur durch Lautlesen, nicht durch Regex.

### Rhythmus-Check
- Mehr als 3 Sätze mit ähnlicher Länge hintereinander?
- Fehlen kurze Punch-Sätze zwischen langen Hypotaxen?
- Klingt es monoton, wenn laut gelesen?
- Fehlt das Auf-und-Ab zwischen langen und kurzen Sätzen?

In wissenschaftlichen Texten ist der Rhythmus ohnehin gemäßigter als in journalistischen — aber absolute Gleichlänge klingt trotzdem nach KI.

### Konkretheit-Check
- Abstrakte Aussagen ohne Zahlen, Quellen oder Beispiele?
- Kann „optimiert" durch eine konkrete Änderung ersetzt werden?
- Kann „verbessert" durch eine messbare Differenz ersetzt werden?
- Steht irgendwo „effektiv", „effizient", „nachhaltig" ohne belegte Metrik?

Ein wissenschaftlicher Text ohne **Zahlen, Quellen oder konkrete Beispiele** ist meist KI-generierter Allgemeinplatz.

---

## G7 — Wissenschafts-spezifische KI-Muster

Ergänzungen zu den allgemeinen Mustern — diese Patterns tauchen **besonders in KI-generierten akademischen Texten** auf:

| Pattern | BAD | FIX |
|---|---|---|
| **Pseudo-Literaturüberblick** | „Verschiedene Autoren haben sich mit X beschäftigt." | Konkrete Autoren nennen, mit Position + Quelle |
| **Schwammige Forschungslücke** | „Allerdings gibt es noch Forschungsbedarf." | Forschungslücke konkret benennen: „Bisher unerforscht ist Y, wie Z (Jahr) konstatiert." |
| **Abstraktes Fazit** | „Die Ergebnisse zeigen, dass das Thema komplex ist." | Konkret, was gezeigt wurde: „Die Auswertung ergibt ein dreifaches Muster: ..." |
| **Generische Einleitung** | „In der heutigen digitalen Welt spielt X eine immer wichtigere Rolle." | Problem konkret mit Zahlen/Studien einleiten |
| **Allwissender Schlusssatz** | „Zukünftige Forschung wird zeigen müssen, ob ..." | Konkret formulieren, welche Frage und welches Design |
| **Theorie-Praxis-Plattitüde** | „Theorie und Praxis müssen zusammenwirken." | Streichen — sagt nichts |
| **Paraphrase-Karussell** | 5 Sätze, die dieselbe Aussage variieren | Einen Satz behalten, Rest streichen |

---

## Fix-Strategien

### Negation-Affirmation → Direkte Aussage
```
BAD: „Es handelt sich nicht um einen Ausreißer. Es handelt sich um einen systematischen Zusammenhang."
FIX: „Der Zusammenhang ist systematisch (r = 0,42, p < 0,01)."
```

### Puffery → Fakten oder streichen
```
BAD: „spielt eine entscheidende Rolle bei der Digitalisierung"
FIX: [streichen] oder „wird von 73 % der Unternehmen eingesetzt (vgl. Müller 2024, S. 17)"
```

### Superficial Analysis → Direkte Aussage
```
BAD: „Diese Statistik unterstreicht die Dringlichkeit des Problems."
FIX: „Die Statistik zeigt einen Anstieg um 47 % in fünf Jahren (vgl. Destatis 2024)."
```

### Abstraktes Fazit → Konkretes Zwischenfazit
```
BAD: „Es zeigt sich, dass die Thematik facettenreich ist und viele Aspekte umfasst."
FIX: „Die Analyse identifiziert drei zentrale Einflussfaktoren: (a) ..., (b) ..., (c) ..."
```

---

## Regel-Index (für Rückverweise)

| Kategorie | Handhabung |
|---|---|
| G1 | Grep + LLM-Prüfung für subtile Varianten |
| G2 | Grep + LLM-Kontext-Bewertung |
| G3 | Grep + LLM-Kontext-Bewertung |
| G4 | LLM-only (semantische Synonym-Erkennung) |
| G5 | Grep + LLM für Gesamtdichte |
| G6 | LLM-only (Gesamtrhythmus, Konkretheit) |
| G7 | LLM-only (wissenschaftsspezifische Muster) |

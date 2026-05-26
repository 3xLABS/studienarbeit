# Wissenschaftlicher Stil — Leitlinien für Writer, Reviewer und Überarbeitung

Single Source of Truth für den Schreibstil der Pipeline. Der Writer hält sich präventiv an diese Regeln, der Reviewer prüft sie, der Überarbeitungs-Skill repariert Verstöße.

Ziel: Texte klingen wie von einem fortgeschrittenen Studierenden im jeweiligen Studienabschnitt geschrieben — fachlich präzise, methodisch sauber, sprachlich nüchtern. **Nicht** nach Wirtschaftsmagazin, **nicht** nach Blog, **nicht** nach Habilitation.

---

## 1. Grundhaltung

| Soll | Nicht |
|---|---|
| Dritte Person, sachlich | Ich-Form („Ich meine, dass...") |
| Argumentativ ("Dies zeigt, dass...") | Meinungsgetrieben ("Ich finde...") |
| Fachsprache mit kontrollierter Einführung | Beliebiger Wechsel Umgangs-/Fachsprache |
| Aktiv bevorzugt, Passiv wenn nötig | Dauerpassiv ("es wird gezeigt, dass gezeigt wird") |
| Kurze, klare Sätze | Verschachtelte Hypotaxen mit 4+ Nebensätzen |
| Präzise Verben | Nominalisierungs-Überschuss |

---

## 2. Person und Perspektive

**Grundregel:** Dritte Person, keine Ich-Form, kein „wir", keine direkte Leseransprache.

**Ausnahmen (abhängig von Hochschule/Fach):**
- Methodenkapitel darf in manchen Fächern "Ich" verwenden („Für diese Arbeit wurden [...] Interviews geführt." ist trotzdem besser)
- In Reflexionen am Ende der Arbeit ist "Ich" möglich, wenn der Lehrstuhl es erlaubt
- Im **Fazit** von Masterarbeiten ist vorsichtiges "Die Autorin / Der Autor" oft zulässig

**Default:** Unpersönliche Konstruktionen mit „die vorliegende Arbeit", „im Folgenden", „dazu wird zunächst".

```
NEIN: Ich habe 10 Interviews geführt und sie dann mit MAXQDA ausgewertet.
JA:   Im Rahmen der Arbeit wurden zehn Leitfadeninterviews geführt und anschließend mit MAXQDA ausgewertet.
```

```
NEIN: Wir sehen also, dass ...
JA:   Es zeigt sich, dass ...
JA:   Die Auswertung zeigt, dass ...
```

---

## 3. Aktiv vs. Passiv

Wissenschaftssprache neigt zum Passiv, übertreibt es aber oft. Regel: **Aktiv, wenn der Handelnde klar benannt werden kann oder muss. Passiv, wenn die Handlung wichtiger ist als der Handelnde.**

```
GUT (aktiv):  Müller (2019) argumentiert, dass ...
SCHLECHT:     Es wird argumentiert, dass ...   [wer? Müller? der Autor der Arbeit?]

GUT (passiv): Für die Auswertung wurde das Verfahren nach Mayring (2022) gewählt.
SCHLECHT:     Der Autor wählt für die Auswertung das Verfahren nach Mayring.
```

**Nominalisierung sparsam einsetzen.** Ein nominalisierter Satz wirkt gewichtiger, liest sich aber schwerer. Faustregel: **pro Satz maximal ein Nominalphrasen-Cluster.**

```
NOMINAL:  Die Betrachtung der Entwicklung der Bedeutung der Digitalisierung ...
VERBAL:   Wie sich die Bedeutung der Digitalisierung entwickelt hat, ...
```

---

## 4. Satzbau und Rhythmus

- **Satzlänge:** Ø 15–22 Wörter. Sätze über 30 Wörter sind Kandidaten fürs Aufteilen.
- **Max. 2 Nebensätze pro Satz.** Dreifach verschachtelt → aufteilen.
- **Variierter Rhythmus:** Auch wissenschaftliche Texte brauchen Wechsel zwischen kürzeren (7–12 Wörter) und längeren Sätzen. Monotone Gleichlängen klingen KI-generiert.
- **Ein Gedanke pro Satz.** Konjunktionen wie „und"/„sowie" nicht zur Verkettung unverbundener Aussagen nutzen.

---

## 5. Fachsprache und Begriffsarbeit

- **Begriffe bei erster Nennung definieren** oder auf eine Quelle verweisen, die sie definiert. Danach konsistent denselben Begriff verwenden.
- **Keine Synonym-Variation** aus stilistischen Gründen (siehe `anti-ki-muster.md` § G4). Wer "Anforderung" schreibt, bleibt bei "Anforderung" — nicht „Requirement", „Spezifikation", „Vorgabe" im Wechsel.
- **Englische Fachtermini** nur, wenn sie in der deutschen Fachliteratur Standard sind (z. B. *Stakeholder*, *Grounded Theory*, *Benchmarking*). Dann kursiv bei Ersterwähnung, danach aufrecht.
- **Abkürzungen** bei Ersterwähnung ausschreiben: „Customer Relationship Management (CRM)".

---

## 6. Argumentation (Kurzform — Details in `argumentationsstrukturen.md`)

Jeder Argumentations-Absatz folgt dem Schema **Claim → Reason → Evidence**:

1. **Claim:** Behauptung/These (1 Satz)
2. **Reason:** Begründung, warum das so ist (1–3 Sätze)
3. **Evidence:** Beleg — Quelle, Daten, Beispiel (mit Zitation)

Beschreibende Absätze (Begriffsklärung, Methodenbeschreibung) folgen nicht zwingend diesem Schema, sind aber kürzer.

**Nie:** Aussage ohne Beleg, wenn sie begründbar wäre. **Nie:** „Es ist allgemein bekannt, dass ...".

---

## 7. Quellenarbeit im Text

- **Indirektes Zitat** (Paraphrase): Seitenangabe je nach Zitierstil optional, aber im Zweifel setzen. Einleitung mit „vgl." im deutschen Harvard-Stil.
- **Direktes Zitat:** Anführungszeichen, exakter Wortlaut, Seitenangabe Pflicht. Lange Zitate (≥ 40 Wörter) als eingerückter Block.
- **Nicht zu viele direkte Zitate.** Wissenschaftliche Arbeiten paraphrasieren mehrheitlich. Direktes Zitat nur, wenn Wortlaut inhaltlich wichtig ist.
- **Jeder gestützte Claim** bekommt eine Quelle. Auch einen "allgemein bekannten" Fakt kann man meist belegen.

Details zu den Zitierstilen → `zitierstile.md`.

---

## 8. Objektivität und Hedging

Wissenschaftliche Texte zeigen Nuancen statt absoluter Aussagen.

**Hedging-Ausdrücke** (dosiert einsetzen):
- „lässt sich argumentieren, dass ..."
- „deutet darauf hin, dass ..."
- „könnte ein Indiz dafür sein, dass ..."
- „in vielen Fällen ..."

**Aber:** Hedging nicht als Floskel. Wenn eine Aussage belegt ist, darf sie direkt stehen.

```
NEIN: Es ist anzunehmen, dass möglicherweise eventuell ein Zusammenhang bestehen könnte.
JA:   Die Daten zeigen einen signifikanten Zusammenhang (r = 0,42, p < 0,01).
```

**Verbotene Absolutismen**: „immer", „nie", „alle", „jeder" — fast immer falsch in wissenschaftlichem Kontext, außer mit Beleg.

---

## 9. Verbotsliste

Diese Formulierungen sind **nicht wissenschaftlich** und werden vom Reviewer als Verstoß geflaggt:

**Umgangssprache:**
- „echt", „total", „krass", „irgendwie", „eigentlich"
- „riesig", „mega", „absolut entscheidend"
- rhetorische Fragen im Fließtext („Was heißt das? Nun, ...")

**Floskeln ohne Substanz:**
- „In der heutigen digitalen Welt ..."
- „In Zeiten von [X] wird immer deutlicher, dass ..."
- „Seit jeher beschäftigt sich die Menschheit mit ..."
- „nicht zuletzt", „vor allem", "im Grunde" (wenn Füllwort)

**Journalismus-Import:**
- Reißerische Überschriften
- Cliffhanger („Doch dazu später mehr.")
- „Spannend ist, dass ..." / „Bemerkenswert ist ..."

**KI-Sprache** (Details in `anti-ki-muster.md`):
- „unterstreicht", „verdeutlicht", „hebt hervor" (wenn subjektlos)
- „spielt eine entscheidende/zentrale/pivotale Rolle"
- „revolutionär", „bahnbrechend", „wegweisend"
- „von X bis Y" ohne echtes Spektrum
- „nicht nur … sondern auch"
- „Zusammenfassend lässt sich sagen ..." (Fließtext — in Fazit-Kontexten erlaubt)

**Selbstreferenz-Überschuss:**
- „Wie bereits erwähnt ..." (mehr als 1× pro Kapitel)
- „Im nächsten Kapitel wird ..." (mehr als an Kapitelende)
- „In diesem Abschnitt geht es um ..." als Einstiegssatz

---

## 10. Kapiteltyp-Spezifika

### Einleitung
- Problemstellung mit Relevanz (wissenschaftlich + ggf. praktisch)
- Forschungsfrage wörtlich nennen
- Aufbau der Arbeit kurz skizzieren
- Keine Ergebnisse vorwegnehmen

### Theoretische Grundlagen
- Begriffsklärung vor Anwendung
- Theoretischer Rahmen mit Begründung
- Stand der Forschung als Diskurs, nicht als Literaturliste
- Schlusssatz führt zur Methodik oder zur Analyse über

### Methodik
- Forschungsdesign begründet (warum diese Methode?)
- Datenerhebung reproduzierbar beschrieben
- Auswertungsverfahren mit Quelle (z. B. Mayring 2022, Kuckartz 2018)
- Gütekriterien: Objektivität, Reliabilität, Validität (quantitativ) oder Kriterien nach Lincoln/Guba, Mayring (qualitativ)

### Ergebnisse
- Deskriptiv, nicht interpretierend
- Tabellen und Abbildungen mit Nummer, Titel, Quellenangabe
- Keine Wertungen („interessant", „erwartet")
- Reihenfolge orientiert sich an Forschungsfrage, nicht am Erhebungsablauf

### Diskussion
- Ergebnisse interpretieren, nicht nochmal beschreiben
- Rückbindung an Theorie und Stand der Forschung
- Limitationen benennen (Stichprobe, Methode, Generalisierbarkeit)
- Implikationen für Theorie und Praxis getrennt

### Fazit
- Forschungsfrage direkt beantworten
- Kernergebnisse zusammenfassen (kurz, maximal 1 Satz pro Teilergebnis)
- Ausblick auf weitere Forschung
- Keine neuen Argumente, keine neuen Quellen

---

## 11. Typografische Konventionen

- **Kursiv:** Fachbegriffe bei Ersterwähnung, fremdsprachliche Termini, Buchtitel (je nach Zitierstil)
- **Fett:** nur in Überschriften oder bei echten Key-Concepts — **sehr sparsam** im Fließtext
- **Anführungszeichen:** Deutsch „..." für direkte Zitate, 'einfache' für Zitate im Zitat. Bei englischem Originaltext doppelte englische Anführungszeichen "...".
- **Gedankenstrich:** mit Leerzeichen (– kein Bindestrich -)
- **Zahlen:** 1–12 ausschreiben, ab 13 Ziffern (außer Jahreszahlen, Maße, Statistiken)
- **Prozent / % :** Im Fließtext ausschreiben („15 Prozent"), in Tabellen „%"

---

## 12. Referenzen

- **Anti-KI-Muster:** `anti-ki-muster.md` (ergänzt die Verbotsliste um subtile Patterns)
- **Argumentationsstrukturen:** `argumentationsstrukturen.md` (Claim-Reason-Evidence, Toulmin)
- **Zitierstile:** `zitierstile.md` (Harvard, APA, Deutsche Zitierweise, Chicago, MLA)
- **Empirische Methoden:** `empirische-methoden.md` (qualitativ + quantitativ)
- **Validierung:** `validierung.md` (Review-Gate)

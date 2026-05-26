# Zitierstile — Referenz für die Studienarbeiten-Pipeline

Single Source of Truth für alle unterstützten Zitierstile. Der Writer liest den gewählten Stil aus `04-fortschritt/Fortschritt.md` (Meta-Block `Zitierstil`) und wendet ihn konsistent an. Der Reviewer prüft gegen diesen Stil. Die Finalisierung baut das Literaturverzeichnis entsprechend auf.

**Unterstützte Stile:**
1. Harvard (Default, v. a. BWL, Wirtschaftswissenschaften)
2. APA 7 (Psychologie, Sozialwissenschaften, Pädagogik)
3. Deutsche Zitierweise / Fußnoten (Jura, Geschichte, teils Theologie)
4. Chicago Author-Date / Notes-Bibliography (Geisteswissenschaften)
5. MLA 9 (Literaturwissenschaft, Sprachwissenschaft)

Der User entscheidet im Onboarding. Ohne explizite Wahl: **Harvard**.

---

## Querverweis

Die alte Referenz `studienarbeit-writer/references/harvard-zitierstil.md` bleibt als Harvard-Detailreferenz erhalten, aber die Pipeline nutzt ab jetzt **diese Datei** als Single Source of Truth für alle Stile. Der Writer liest nur noch von hier.

---

## 1. Harvard (Default)

### Indirektes Zitat (Paraphrase)

```
(vgl. Müller 2019, S. 42)
(vgl. Müller/Schmidt 2020, S. 15–17)
(vgl. Müller et al. 2021, S. 88)
```

Bei satzinterner Einbindung:
```
Wie Müller (2019, S. 42) darstellt, ...
```

### Direktes Zitat

```
"Wörtlich zitierter Satz." (Müller 2019, S. 42)
```

Lange Zitate (≥ 40 Wörter): eingerückter Absatz, ohne Anführungszeichen.

### Mehrere Werke

```
(vgl. Müller 2019, S. 42; Schmidt 2020, S. 15)
```

### Zitat aus Sekundärquelle

```
Zitiert nach Müller (2019, S. 42; ursprünglich Schmidt 2010, S. 20)
```

### Kein Autor / Organisation

```
(vgl. OECD 2022, S. 14)
(vgl. o. V. 2020, S. 3)    ← „ohne Verfasser"
```

### Kein Jahr / Seite

```
(vgl. Müller o. J., S. 42)
(vgl. Müller 2019, o. S.)
```

### Literaturverzeichnis — Harvard

Alphabetisch nach Nachname, ein Eintrag pro Werk, hängende Einrückung.

**Monografie:**
```
Müller, P. (2019): Titel des Werks. Untertitel. 3. Aufl., Berlin: Springer.
```

**Sammelwerk-Beitrag:**
```
Schmidt, A. (2020): Titel des Beitrags. In: Weber, K. (Hrsg.): Titel des Sammelbands. München: Vahlen, S. 45–67.
```

**Journal-Artikel:**
```
Meier, T./Huber, S. (2021): Titel des Artikels. In: Journal of Management, Jg. 45, H. 3, S. 112–134.
```

**Online-Quelle:**
```
BMWK (2023): Titel der Veröffentlichung. Online verfügbar unter https://... (abgerufen am 14.04.2026).
```

**Hochschulschrift:**
```
Fischer, L. (2020): Titel der Dissertation. Dissertation, Universität Köln.
```

---

## 2. APA 7

### Indirektes Zitat

```
(Müller, 2019)
(Müller, 2019, S. 42)
(Müller & Schmidt, 2020)
(Müller et al., 2021)
```

Bei satzinterner Einbindung (Narrative):
```
Müller (2019) argumentiert, dass ...
Laut Müller und Schmidt (2020) ...
```

### Direktes Zitat

```
"Wörtlich zitierter Satz" (Müller, 2019, S. 42).
```

Lange Zitate (≥ 40 Wörter): eingerückter Blockabsatz.

### Mehrere Werke

```
(Müller, 2019; Schmidt, 2020)
```

Alphabetisch geordnet.

### Kein Autor

```
(OECD, 2022, S. 14)
("Titel des Werks", 2020)    ← wenn wirklich niemand bekannt
```

### Literaturverzeichnis — APA 7

Alphabetisch, hängende Einrückung, DOI am Ende (wenn vorhanden).

**Monografie:**
```
Müller, P. (2019). Titel des Werks: Untertitel (3. Aufl.). Springer.
```

**Sammelwerk-Beitrag:**
```
Schmidt, A. (2020). Titel des Beitrags. In K. Weber (Hrsg.), Titel des Sammelbands (S. 45–67). Vahlen.
```

**Journal-Artikel:**
```
Meier, T., & Huber, S. (2021). Titel des Artikels. Journal of Management, 45(3), 112–134. https://doi.org/10.xxxx/xxxxx
```

**Online-Quelle:**
```
BMWK. (2023). Titel der Veröffentlichung. https://...
```

APA-7-Besonderheiten:
- Bis zu 20 Autor:innen mit Komma trennen, letzte:n mit „&"
- Bei 21+ Autor:innen die ersten 19 + „...", dann letzte:n
- Keine Ortsangabe mehr (APA-7-Änderung gegenüber APA-6)

---

## 3. Deutsche Zitierweise (Fußnoten)

Kein In-Text-Citation — **jede Quellenangabe ist eine Fußnote**. Der Writer muss im Fließtext Markup für Fußnoten anlegen, damit die Finalisierung sie beim docx-Export richtig umsetzen kann.

### Im Fließtext

**Obsidian-Markdown:**
```
Die Digitalisierung verändert Geschäftsmodelle grundlegend.[^1]
```

Wo `[^1]` die Fußnotenreferenz ist.

### Fußnoten am Seitenende (Vollzitat bei Ersterwähnung)

```
[^1]: Vgl. Müller, P.: Titel des Werks, 3. Aufl., Berlin 2019, S. 42.
```

### Folgezitat

```
[^2]: Vgl. Müller, P.: a. a. O., S. 45.
```

Oder moderner:
```
[^2]: Vgl. Müller (2019), S. 45.
```

### Direktes Zitat

```
„Wörtlich zitierter Satz."[^3]

[^3]: Müller, P.: Titel des Werks, 3. Aufl., Berlin 2019, S. 42.
```

(Ohne „vgl." bei direktem Zitat.)

### Mehrere Quellen in einer Fußnote

```
[^4]: Vgl. Müller (2019), S. 42; Schmidt (2020), S. 15.
```

### Literaturverzeichnis — Deutsche Zitierweise

Alphabetisch, Vollzitate (wie bei Harvard, aber **mit Vornamen ausgeschrieben oder Initialen nach Präferenz**).

**Monografie:**
```
Müller, Peter: Titel des Werks. Untertitel, 3. Aufl., Berlin 2019.
```

**Sammelwerk-Beitrag:**
```
Schmidt, Anna: Titel des Beitrags, in: Weber, Klaus (Hrsg.): Titel des Sammelbands, München 2020, S. 45–67.
```

**Journal-Artikel:**
```
Meier, Thomas/Huber, Sabine: Titel des Artikels, in: Journal of Management, Jg. 45 (2021), H. 3, S. 112–134.
```

**Hinweis Writer:** Bei Deutscher Zitierweise **muss der Writer die Fußnoten bereits in der Markdown-Datei anlegen** (Obsidian-Footnote-Syntax `[^label]`), damit sie bei der Finalisierung korrekt ins docx übernommen werden.

---

## 4. Chicago Author-Date

### Indirektes Zitat

```
(Müller 2019, 42)
(Müller und Schmidt 2020, 15)
(Müller et al. 2021)
```

### Direktes Zitat

```
"Wörtlich zitierter Satz" (Müller 2019, 42).
```

### Literaturverzeichnis — Chicago

**Monografie:**
```
Müller, Peter. 2019. Titel des Werks: Untertitel. 3. Aufl. Berlin: Springer.
```

**Sammelwerk-Beitrag:**
```
Schmidt, Anna. 2020. „Titel des Beitrags." In Titel des Sammelbands, hrsg. von Klaus Weber, 45–67. München: Vahlen.
```

**Journal-Artikel:**
```
Meier, Thomas, und Sabine Huber. 2021. „Titel des Artikels." Journal of Management 45 (3): 112–134.
```

### Chicago Notes-Bibliography (Fußnoten-Variante)

Wie Deutsche Zitierweise, aber mit:
- „Ibid." (in älteren Ausgaben) oder Kurztitel (neuer) statt „a. a. O."
- Bibliografie am Ende parallel zu den Fußnoten

---

## 5. MLA 9

### Indirektes Zitat

```
(Müller 42)
(Müller und Schmidt 15)
```

Satzintern:
```
Wie Müller schreibt (42), ...
```

### Literaturverzeichnis — MLA

Heißt hier „Works Cited".

**Monografie:**
```
Müller, Peter. Titel des Werks: Untertitel. 3. Aufl., Springer, 2019.
```

**Sammelwerk-Beitrag:**
```
Schmidt, Anna. „Titel des Beitrags." Titel des Sammelbands, hrsg. von Klaus Weber, Vahlen, 2020, S. 45–67.
```

**Journal-Artikel:**
```
Meier, Thomas, und Sabine Huber. „Titel des Artikels." Journal of Management, Jg. 45, H. 3, 2021, S. 112–134.
```

---

## Handhabung in den Skills

### Writer

1. **Lesen des Zitierstils:** Beim Start jedes Laufs aus `04-fortschritt/Fortschritt.md` den Wert `Zitierstil` im Meta-Block lesen.
2. **Anwenden:** Alle Zitationen im Kapitel im gewählten Stil formatieren.
3. **Bei Deutscher Zitierweise / Chicago-Notes:** Fußnoten-Markup `[^n]` setzen, damit die Finalisierung daraus docx-Fußnoten macht.
4. **Obsidian-Wiki-Links:** Der Wiki-Link zur Quellenauswertung bleibt unabhängig vom Zitierstil:
   ```
   ... [[Auswertung_Kapitel 2_Grundlagen#Müller, 2019|Müller 2019]] ...
   ```
   Die sichtbare Form im Link-Text passt sich dem Zitierstil an.

### Reviewer

Prüft:
- Zitierstil konsistent im gesamten Kapitel?
- Seitenangaben vorhanden wo Pflicht?
- Wörtliche Zitate korrekt markiert?
- Bei Fußnoten-Stilen: Alle Fußnoten nummeriert, keine Dublette?
- Keine Mischformen (z. B. Harvard + Fußnoten gemischt)?

### Finalisierung

- Baut das Literaturverzeichnis im gewählten Stil zusammen
- Konvertiert Fußnoten-Markdown (`[^n]`) in echte Word-Fußnoten (bei Deutscher Zitierweise / Chicago-Notes)
- Prüft alphabetische Sortierung
- Prüft Vollständigkeit: jede im Text zitierte Quelle muss im Verzeichnis stehen und umgekehrt

---

## Fachspezifische Hinweise

| Fach / Studiengang | Empfohlener Stil |
|---|---|
| BWL / Wirtschaftsinformatik / Volkswirtschaftslehre | Harvard |
| Psychologie / Pädagogik / Soziologie | APA 7 |
| Rechtswissenschaft | Deutsche Zitierweise (Pflicht) |
| Geschichte / Theologie | Deutsche Zitierweise oder Chicago-Notes |
| Germanistik / Anglistik / Literaturwissenschaft | MLA oder Chicago |
| Medizin / Naturwissenschaften | Harvard oder Vancouver-Style (nicht unterstützt — bitte manuell) |

Im Zweifel: Die **Formatvorgabe des Lehrstuhls/der Hochschule** schlägt jede Default-Empfehlung.

---

## Spezialfälle

### DOIs
Bei allen Stilen: DOI am Ende, wenn vorhanden und sinnvoll (v. a. APA, Chicago). Format: `https://doi.org/10.xxxx/xxxxx` (nicht „doi:..."-Kurzform).

### Mehrere Werke desselben Autors im selben Jahr
Anhängen von a/b/c an das Jahr: `(vgl. Müller 2019a, S. 12)`, `(vgl. Müller 2019b, S. 5)`.

Im Literaturverzeichnis ebenso: `Müller, P. (2019a): ...` und `Müller, P. (2019b): ...`

### Interviews / eigene empirische Daten
Im Text meist als Anhangsverweis zitiert: `(Interview A, Abs. 12)` oder `(eigene Erhebung 2026, n=8)`. Nicht ins Literaturverzeichnis, sondern in den Anhang.

### Graue Literatur (Berichte, Whitepaper, Gesetze)
**Harvard/APA:** Organisation als Autor, Jahr, Titel, Ort/URL.
**Deutsche Zitierweise:** Gesetze in Fußnote mit Paragraph + Absatz (§ 1 Abs. 2 BGB), nicht im Literaturverzeichnis.

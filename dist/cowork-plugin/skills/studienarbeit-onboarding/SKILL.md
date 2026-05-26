---
name: studienarbeit-onboarding
description: |
  Phase 0 der Studienarbeiten-Pipeline für alle Arbeitstypen (Hausarbeit, Seminararbeit, Studienarbeit, Bachelorarbeit, Masterarbeit). Prüft, ob alle Voraussetzungen erfüllt sind (Ordner, Ordnerstruktur, Internet, Sub-Skills, Python), fragt den Arbeitstyp und alle Meta-Daten ab (Hochschule, Fach, Zitierstil, Seitenumfang, Abgabedatum, Empirie ja/nein) und schreibt sie in den Meta-Block von Fortschritt.md. Nutze diesen Skill beim allerersten Start, bei "Setup", "Onboarding", "Einrichten", "alles bereit?", "kann es losgehen?", "Voraussetzungen prüfen", "Check", "Environment prüfen" oder wenn der User zum ersten Mal eine Studienarbeit startet. Auch bei Fehlern in anderen Skills diesen Skill zur Diagnose verwenden.
---

# Studienarbeit — Phase 0: Onboarding, System-Check und Meta-Daten

Bevor die Pipeline starten kann, müssen mehrere Voraussetzungen erfüllt sein **und** die Meta-Daten der Arbeit feststehen. Dieser Skill prüft beides systematisch.

Dein Output hat **zwei Teile**:
1. **System-Check** (Ordner, Sub-Skills, Internet usw.) — prüft, dass die Pipeline technisch startbereit ist
2. **Meta-Abfrage** (Arbeitstyp, Zitierstil, Umfang, Abgabe, Empirie) — legt den Meta-Block in `04-fortschritt/Fortschritt.md` an, den alle späteren Skills lesen

## Ablauf

1. System-Check der Reihe nach durchführen
2. Zusammenfassung des Checks anzeigen
3. Meta-Daten abfragen (interaktiv, mit sinnvollen Default-Empfehlungen)
4. Meta-Block in `04-fortschritt/Fortschritt.md` schreiben (oder aktualisieren)
5. Empfehlung zur nächsten Phase

Format für Check-Ausgaben:

```
STUDIENARBEIT — System-Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[✅ / ❌ / ⚠️] Check-Name — Ergebnis
```

---

## TEIL 1: SYSTEM-CHECK

### Check 1: Richtiger Ordner ausgewählt

**Was prüfen:**
Der User muss den Projektordner der Arbeit (oder einen Ordner, der die Projektstruktur enthält) als Workspace ausgewählt haben.

**Wie prüfen:**
1. Prüfe ob der aktuelle Workspace-Mount existiert und beschreibbar ist
2. Suche nach diesen Indikatoren für den richtigen Ordner:
   - Datei `README.md` oder `Forschungsfrage.md` im Root
   - Ordner `.claude/skills/` mit Studienarbeit-Skills
   - Ordner `02-quellen/` oder `03-text/`
   - Datei `Gliederung.md` oder `Prompts.md`

**Ergebnis:**
- ✅ wenn mindestens 2 der Indikatoren gefunden werden
- ⚠️ wenn der Ordner existiert aber leer ist oder keine Projektstruktur hat → biete an, die Struktur zu erstellen
- ❌ wenn kein Ordner gemountet ist → weise den User an, den Projektordner auszuwählen

**Falls die Ordnerstruktur fehlt, erstelle sie:**
```
[Projektordner]/
├── .claude/skills/
├── 01-docs/
├── 02-quellen/
├── 03-text/
├── 04-fortschritt/
├── 05-review/
└── 06-final/
```

---

### Check 2: Internetzugang

**Was prüfen:**
Claude braucht Internetzugang für Web-Recherche und Quellensuche.

**Wie prüfen:**
```bash
curl -s --max-time 10 -o /dev/null -w "%{http_code}" https://www.google.com
```

**Ergebnis:**
- ✅ wenn HTTP 200 oder 301/302 zurückkommt
- ❌ wenn Timeout oder Fehler → weise den User darauf hin, dass Netzwerkzugang in den Claude-Einstellungen aktiviert sein muss

---

### Check 3: Google-Account für NotebookLM & Gemini

**Was prüfen:**
Der User braucht einen Google-Account, um NotebookLM und Google AI Studio (Gemini) nutzen zu können. Diese Tools werden in Phase 2 (Recherche) und Phase 3 (Quellenauswertung) vom User **manuell im Browser** bedient — Claude gibt Anleitungen und Prompts, aber die Navigation und Bedienung liegt beim User.

**Wie prüfen:**
Frage den User: „Hast du einen Google-Account, mit dem du auf NotebookLM (notebooklm.google.com) und Google AI Studio (aistudio.google.com) zugreifen kannst?"

**Ergebnis:**
- ✅ wenn der User bestätigt
- ⚠️ wenn der User unsicher ist → weise ihn an, sich unter notebooklm.google.com einzuloggen und zu prüfen, ob er Zugang hat
- ❌ wenn der User keinen Google-Account hat → er muss einen erstellen

---

### Check 4: Sub-Skills vorhanden

**Was prüfen:**
Alle Kern-Skills der Pipeline müssen verfügbar sein.

**Wie prüfen:**
Suche nach diesen Dateien im `.claude/skills/`-Ordner:

| Skill | Datei |
|-------|-------|
| Planung | `studienarbeit-planung/SKILL.md` |
| Recherche | `studienarbeit-recherche/SKILL.md` |
| Quellenauswertung | `studienarbeit-quellenauswertung/SKILL.md` |
| Writer | `studienarbeit-writer/SKILL.md` |
| Reviewer | `studienarbeit-reviewer/SKILL.md` |
| Überarbeitung | `studienarbeit-ueberarbeitung/SKILL.md` |
| Finalisierung | `studienarbeit-finalisierung/SKILL.md` |

Zusätzlich den Foundation-Ordner:
- `_foundation/arbeitstypen.md`
- `_foundation/wissenschaftlicher-stil.md`
- `_foundation/zitierstile.md`
- `_foundation/argumentationsstrukturen.md`
- `_foundation/anti-ki-muster.md`
- `_foundation/empirische-methoden.md`
- `_foundation/validierung.md`

**Ergebnis:**
- ✅ wenn alle Sub-Skills + alle Foundation-Dateien gefunden werden
- ⚠️ wenn einige fehlen → liste die fehlenden auf
- ❌ wenn die Grundstruktur fehlt → der User muss die Skills zuerst installieren

---

### Check 5: Python-Umgebung

**Was prüfen:**
Python 3 muss verfügbar sein (wird für diverse Skripte in der Finalisierungsphase benötigt).

**Wie prüfen:**
```bash
python3 --version 2>/dev/null || python --version 2>/dev/null
```

**Ergebnis:**
- ✅ wenn Python 3.8+ verfügbar ist
- ⚠️ wenn nicht vorhanden oder zu alte Version (kein K.o.-Kriterium, aber Finalisierung ist eingeschränkt)

---

### Check 6: Bestehender Fortschritt

**Was prüfen:**
Ob der User bereits Fortschritt gemacht hat (um die richtige Phase zu empfehlen).

**Wie prüfen:**
1. Existiert `04-fortschritt/Fortschritt.md` mit Meta-Block? → Onboarding wurde schon gelaufen
2. Existiert `02-quellen/Forschungsfrage.md`? → Phase 1 (Planung) begonnen
3. Existiert `01-docs/Gliederung.md`? → Phase 1 weiter fortgeschritten
4. Existieren `Recherche_Kapitel_*.md` in `02-quellen/`? → Phase 2 begonnen
5. Existieren `Auswertung_Kapitel_*.md` in `02-quellen/`? → Phase 3 (Literatur) begonnen
6. Existieren `Empirik_Auswertung_Kapitel_*.md` in `02-quellen/`? → Phase 3 (Empirik) begonnen
7. Dateien in `03-text/`? → Phase 4 (Schreiben) begonnen
8. Dateien in `05-review/`? → Phase 5 (Review) begonnen
9. Dateien in `06-final/`? → Phase 7 (Finalisierung) begonnen

**Ergebnis:**
- Zeige eine Übersicht des aktuellen Stands
- Empfehle die nächste Phase basierend auf dem Fortschritt
- Falls Meta-Block bereits existiert → zeige ihn an und frage, ob Änderungen nötig sind (statt neu abzufragen)
- Falls kein Fortschritt: „Bereit für Teil 2 — Meta-Abfrage"

---

## TEIL 1.5: Meta-Block lesen und System-Check kalibrieren

**Vor dem System-Check:** Wenn `04-fortschritt/Fortschritt.md` bereits existiert und einen Meta-Block enthält, lies ihn jetzt ein. Der Meta-Block (YAML zwischen `---` und `---` am Anfang der Datei) enthält:

```yaml
arbeitstyp: Bachelorarbeit  # Hausarbeit, Seminararbeit, Bachelorarbeit, Masterarbeit
seitenzahl_ziel: 45
zitierstil: Harvard          # Harvard, Deutsche Zitierweise, Chicago
empirie: false               # true wenn Interview/Fragebogen/Beobachtung
fachbereich: BWL
```

**Wie der Meta-Block den System-Check kalibriert:**

- **arbeitstyp**: Bestimmt die Seitenanzahl-Erwartungen (Hausarbeit 10–20, Seminararbeit 15–25, Bachelorarbeit 30–60, Masterarbeit 60–100) und die Minimal-Quellenanzahl
- **zitierstil**: Konfiguriert alle downstream Skills (Phase 4 Writer, Phase 6 Überarbeitung, Phase 7 Finalisierung) auf den richtigen Zitierstil
- **empirie**: Falls true, prüfe auf zusätzliche Ordner (`appendix/interviews/`, `appendix/transcripts/`, `appendix/codes/`) und stelle sicher, dass Phase 3 Gemini-Prompts für Qualitative Inhaltsanalyse / Statistik bereit sind
- **fachbereich**: Zeigt an, dass die Hochschule und das Fach korrekt dokumentiert sind (optional, aber hilfreich für Feedback-Ton und Begriffskonsistenz)

Falls `04-fortschritt/Fortschritt.md` nicht existiert oder kein Meta-Block darin ist, fahre direkt mit TEIL 2 fort — du fragst alles ab.

## TEIL 2: META-ABFRAGE

Jetzt werden die projekt-spezifischen Meta-Daten abgefragt. **Wenn der Meta-Block in Fortschritt.md bereits existiert**, diesen anzeigen und den User fragen, was geändert werden soll — statt alles neu zu erfragen.

Die abzufragenden Felder (und sinnvolle Default-Empfehlungen):

### 2.1 Arbeitstyp

Frage: „Was für eine Arbeit schreibst du?"

Optionen (AskUserQuestion, wenn möglich):
- Hausarbeit (10–20 Seiten, 1 Semester, meist ohne Empirie)
- Seminararbeit (15–25 Seiten, 1 Semester, meist ohne Empirie)
- Studienarbeit / Projektarbeit (20–40 Seiten, Praxis-/Methodenbezug, Empirie optional)
- Bachelorarbeit (30–60 Seiten, Abschlussarbeit, Empirie empfohlen)
- Masterarbeit (60–100 Seiten, Abschlussarbeit, Empirie erwartet)

### 2.2 Hochschule / Universität

Frei-Text-Feld. Beispiel: „TU München", „HS Fresenius", „FernUni Hagen".

### 2.3 Fach / Studiengang

Frei-Text-Feld. Beispiel: „BWL", „Wirtschaftsinformatik", „Psychologie", „Rechtswissenschaft".

### 2.4 Lehrstuhl / Betreuung (optional)

Frei-Text, kann leer bleiben.

### 2.5 Zitierstil

Frage: „Welchen Zitierstil schreibt dein Lehrstuhl vor?"

Optionen (mit Empfehlung basierend auf Fach aus 2.3):
- Harvard (Standard in BWL, Wirtschaftswissenschaften, Naturwissenschaften)
- APA 7 (Standard in Psychologie, Pädagogik, Sozialwissenschaften)
- Deutsche Zitierweise / Fußnoten (Rechtswissenschaft, Geschichte, Theologie)
- Chicago (Author-Date oder Notes-Bibliography, Geisteswissenschaften)
- MLA 9 (Literatur- und Sprachwissenschaft)

**Wenn der User unsicher ist:** Empfehle den Fach-Default und weise darauf hin, dass die Formatvorgabe des Lehrstuhls oder der Hochschule Vorrang hat. Verweise auf `_foundation/zitierstile.md` für Details.

### 2.6 Sprache

Default: Deutsch. Bei englischer Arbeit nachfragen — das beeinflusst Writer und Reviewer.

### 2.7 Seitenumfang

Frage: „Welcher Seitenumfang ist vorgegeben? (z. B. '30–50 Seiten' oder '40 Seiten +/- 10 %')"

Default-Empfehlung passend zum Arbeitstyp (vgl. `_foundation/arbeitstypen.md` Tabelle). Der User kann überschreiben.

### 2.8 Abgabedatum

Frage: „Wann ist die Abgabe? (YYYY-MM-DD)"

Wichtig für Zeitplanung in Phase 1.

### 2.9 Empirie geplant?

Frage: „Planst du eine eigene empirische Erhebung (Interviews, Fragebogen, Beobachtung, Experiment)?"

Optionen:
- Nein — rein literaturbasiert
- Ja, qualitativ (Interviews, Fokusgruppen, Beobachtung)
- Ja, quantitativ (Fragebogen, Sekundärdatenanalyse, Experiment)
- Ja, Mixed Methods

Bei „Ja" nachfragen: ungefähre Stichprobengröße (für Zeitplanung und Review-Kriterien).

### 2.10 Forschungsfrage (optional)

Frage: „Hast du schon eine vorläufige Forschungsfrage?"

Kann leer bleiben — wird in Phase 1 entwickelt.

---

## TEIL 3: META-BLOCK SCHREIBEN

Nach der Abfrage den Meta-Block in `04-fortschritt/Fortschritt.md` oben in der Datei anlegen oder aktualisieren:

```markdown
# Fortschritt

## Meta

- **Arbeitstyp:** [Hausarbeit / Seminararbeit / Studienarbeit / Bachelorarbeit / Masterarbeit]
- **Hochschule:** [Name]
- **Fach / Studiengang:** [Name]
- **Lehrstuhl / Betreuung:** [Name oder —]
- **Zitierstil:** [Harvard / APA 7 / Deutsche Zitierweise / Chicago / MLA 9]
- **Sprache:** [Deutsch / Englisch / ...]
- **Seitenumfang:** [z. B. 40–50 Seiten laut Hochschulvorgabe]
- **Abgabedatum:** YYYY-MM-DD
- **Empirie geplant:** [Nein / Qualitativ: Interviews n=X / Quantitativ: n=X / Mixed Methods]
- **Forschungsfrage:** [vorläufig oder —]
- **Letzte Aktualisierung:** YYYY-MM-DD

## Status

_Onboarding abgeschlossen. Weiter mit Phase 1: Planung._

## Kapitel

_Wird in Phase 1 befüllt._

## Zeitplanung

_Wird in Phase 1 angelegt._

## Offene Punkte

_keine_
```

Falls die Datei schon existiert: Meta-Block oben einfügen/aktualisieren, bestehende Abschnitte unverändert lassen.

---

## TEIL 4: ZUSAMMENFASSUNG UND NÄCHSTE SCHRITTE

Am Ende zeige eine kompakte Übersicht:

```
STUDIENARBEIT — Onboarding abgeschlossen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

System-Check:
✅ Ordner             korrekt ausgewählt
✅ Internet           aktiv
✅ Google-Account     vorhanden
✅ Sub-Skills         7/7 gefunden
✅ Foundation         7/7 Dateien vorhanden
✅ Python             3.11.2

Meta-Daten (in Fortschritt.md gespeichert):
📘 Arbeitstyp:        Bachelorarbeit
🏛  Hochschule:        [...]
📚 Fach:              BWL
✒  Zitierstil:        Harvard
📅 Abgabedatum:       2026-09-15
🔬 Empirie:           Ja, qualitativ (n=8)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Alles bereit. Starte mit Phase 1 — Planung:
  „Ich möchte eine Bachelorarbeit zu [Thema] planen."
```

Falls kritische Checks (❌) fehlschlagen:
```
→ Bitte behebe die markierten Probleme, bevor du startest.
   Danach kannst du den Check erneut ausführen.
```

## Automatische Reparatur

Biete dem User an, behebbare Probleme automatisch zu lösen:
- Ordnerstruktur erstellen → Ordner anlegen
- `Fortschritt.md` erstellen → Initiale Datei mit Meta-Block anlegen

Frage vor jeder automatischen Aktion um Erlaubnis.

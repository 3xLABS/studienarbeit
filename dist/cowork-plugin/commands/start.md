---
description: Studienarbeiten-Pipeline starten — System-Check und Phaseneinstieg
---

# Studienarbeiten-Pipeline starten

Der User möchte mit der Studienarbeiten-Pipeline beginnen. Gehe so vor:

1. Rufe den `studienarbeit-onboarding`-Skill auf. Er prüft die Voraussetzungen (Ordnerstruktur, Sub-Skills, Internetzugang) und fragt **Arbeitstyp** (Hausarbeit, Seminararbeit, Studienarbeit, Bachelorarbeit, Masterarbeit) und Meta-Daten (Hochschule, Fach, Zitierstil, Seitenumfang, Abgabedatum, Empirie ja/nein) ab. Er schreibt diese in den Meta-Block von `04-fortschritt/Fortschritt.md`.
2. Wenn das Onboarding sauber durchläuft und noch keine `02-quellen/Forschungsfrage.md` existiert, rufe direkt den `studienarbeit-planung`-Skill auf.
3. Wenn bereits eine Forschungsfrage existiert, lies `04-fortschritt/Fortschritt.md`, erkenne den Arbeitstyp aus dem Meta-Block und erkläre dem User, in welcher Phase er ist und welcher Skill als Nächstes dran wäre.

Pipeline-Reihenfolge:
`studienarbeit-onboarding → -planung → -recherche → -quellenauswertung → -writer → -reviewer → -ueberarbeitung → -finalisierung`.

Wenn der User direkt eine bestimmte Phase ansprechen will (z. B. "Kapitel 3 schreiben"), springe in den entsprechenden Phasen-Skill.

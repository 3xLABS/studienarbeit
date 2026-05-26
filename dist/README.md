# Distribution-Artefakte

Vorgefertigte Cowork-Pakete für die Studienarbeiten-Pipeline. Beide Varianten begleiten Hausarbeiten (10 Seiten) bis Masterarbeiten (100 Seiten).

## Was hier liegt

| Datei / Ordner | Was es ist | Wann nutzen |
|---|---|---|
| `studienarbeit-pipeline.plugin` | Cowork-Plugin (ZIP) mit allen Skills + `/start`-Command + `_foundation/`-Wissensbasis | Empfohlen für Cowork. Installation per Klick auf die Datei → "Save plugin". |
| `studienarbeit.skill` | Einzelner Master-Skill (ZIP) mit allen Phasen und Foundation-Wissen als `references/` | Wenn du nur eine einzige `.skill` installieren willst statt eines Plugins. |
| `cowork-plugin/` | Quellordner des Plugins (nicht-gezippt) | Inspektion, eigene Anpassungen. |
| `master-skill/` | Quellordner des Master-Skills (nicht-gezippt) | Inspektion und Anpassung. |

## Installation

### Variante A: Plugin (empfohlen)

1. `studienarbeit-pipeline.plugin` herunterladen
2. In den Cowork-Chat ziehen oder doppelklicken
3. "Save plugin" klicken

Cowork lädt alle Skills (`studienarbeit-pipeline`, `studienarbeit-onboarding`, `-planung`, `-recherche`, `-quellenauswertung`, `-writer`, `-reviewer`, `-ueberarbeitung`, `-finalisierung`, `humanizer`), den `/start`-Command und die geteilte Wissensbasis (`_foundation/`).

### Variante B: Einzelner Skill

1. `studienarbeit.skill` herunterladen
2. In Cowork ziehen → "Save skill"

Cowork lädt einen einzigen Skill `studienarbeit`, der per `references/` zwischen den Phasen routet. Die Foundation-Dateien sind unter `references/foundation-*.md` enthalten.

## Plugin vs. Master-Skill

- **Plugin (10 Skills + Command + Foundation):** Jede Phase hat einen eigenen Skill mit eigenen Trigger-Phrasen. Cowork wählt automatisch den passenden Skill je nach Anfrage. Genauere Triggerung, modularer.
- **Master-Skill (1 Skill mit references):** Ein einziger Skill, der alle Phasen und das Foundation-Wissen als Referenzdateien enthält und sie selbst routet. Schlankere Plugin-Liste.

Beide Varianten unterstützen alle fünf Arbeitstypen (Hausarbeit, Seminararbeit, Studienarbeit, Bachelorarbeit, Masterarbeit) und produzieren am Ende dieselbe abgabefertige `studienarbeit_final.docx`.

## Pakete selbst neu bauen

```bash
# Plugin
cd dist/cowork-plugin
zip -r ../studienarbeit-pipeline.plugin . -x "*.DS_Store" "*/.DS_Store"

# Master-Skill
cd dist/master-skill/studienarbeit
zip -r ../../studienarbeit.skill . -x "*.DS_Store" "*/.DS_Store"
```

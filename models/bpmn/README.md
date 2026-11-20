# BPMN models

Exported images of the team's BPMN models. The source model files are not available, so only the images are included.

| File | Content |
|---|---|
| `assembly-line-bpmn.png` | Full line: flashing with firmware check and retry loop, socket → silicon mat → housing → buttons, EOL test and validation gates, packing, scrap path |
| `flashing-subprocess-bpmn.png` | Flashing / FKT: place controller → start flashing → 20 s timer → check result |
| `buttons-subprocess-bpmn.png` | Buttons / AS40: place light guides → place correct buttons → activate press |

Mapping to AnyLogic blocks: [docs/assembly-line.md](../../docs/assembly-line.md).

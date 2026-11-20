# Assembly line

[← back to README](../README.md)

## Scenario

NEMO 2026 Disruptive Scenario 2, *"5.0 Solution for Manufacturing Automation"*, is owned by Marquardt and Lucian Blaga University of Sibiu. The public programme booklet describes it as an automotive factory with a multi-station production line, partially manual operations, fragmented material handling and limited real-time visibility. Variable cycle times, unbalanced workloads and bottlenecks lead to idle time and inefficient use of resources ([NEMO 2026 Programme Booklet](https://nemo.omilab.org/nemo/2026/docs/NEMO2026_Programme_Booklet.pdf)).

Working Group 2 represented the line station by station. Three observations shaped the rest of the work (presentation, slide 3):

- **Station-by-station flow:** downstream operations depend on upstream release.
- **Bottlenecks do not stay local:** a slow station starves everything after it.
- **The operator matters:** manual work, stress and variant confusion are part of the system design.

## Three representations of the same line

The line exists in this project at three levels of formality. The names differ slightly between them, so the table below gives the mapping. **The AnyLogic names are authoritative for all simulation results.**

| Scene2Model card (slide 3) | BPMN task (`models/bpmn/`) | AnyLogic block | Time (baseline) | Resource (baseline) |
|---|---|---|---|---|
| Flashing / FKT | *Flashing* (sub-process: place controller → start flashing → **20 s passed** → check result) | `FlashingStart` → `queue` → `WaitForFlashing` | 2 s + 20 s | `FlashingExpert` (1) |
| — | *Is firmware correct?* | `Success` (SelectOutput) | 95% pass | — |
| — | *Was faulty X times?* / *Reroute controller* | `RetryFlashing` → `WaitForFlashing2` → `Success4` | 6 s + 20 s; 60% re-enter, 40% scrap | `FlashingExpert` |
| AS10 – Socket | *Place Socket* | `SocketStation` | 1.5 s | `SocketOperator` (1) |
| AS20 – Mat | *Place Silicon Mat* | `SiliconMatStation` | 1.5 s | `SiliconMatOperator` (1) |
| AS30 – Housing | *Place Housing* | `BaseStation` | 1.5 s | `BaseOperator` (1) |
| AS40 – Buttons | *Buttons* (sub-process: place light guides → place correct buttons → activate press) | `ButtonsStation` | 6 s | `ButtonsOperator` (2) |
| EOL tester | *Perform EOL Testing* / *Did test succeed?* | `EOLTesting` → `Success2` | 5 s; 95% pass | `Tester` (1) |
| VET / validation | *Validate Product* / *Did validation succeed?* | `Validation` → `Success3` | 4 s; 95% pass | `Validator` (1) |
| Packing | *Pack the Product* | `Packing` | 6 s | `Packer` (1) |
| Finished goods | *Product Finished* | `FinishedProduct` (Sink) | — | — |
| — | *Reroute product to bin* / *Product scraped* | `Scrap` (Sink) | — | — |

Notes on the mapping:

- **Presses.** The line includes presses: the Buttons BPMN sub-process ends with *activate press*, and the Buttons scene shows *Press 2*. The AnyLogic models do not represent presses as separate blocks. Their time is part of the Buttons station.
- **Housing.** The AnyLogic block for housing placement is called `BaseStation` and its operator `BaseOperator`; the utilisation chart calls it *Base Placer*.
- **Order of the final checks.** Both the BPMN and the models run **EOL test before validation (VET)**.
- **Station count.** The presentation speaks of *10 stations*. The models contain eight processing stations (Flashing, Socket, Mat, Housing, Buttons, EOL, Validation, Packing), a retry-flashing station and the flashing wait, plus finished-goods and scrap sinks.
- **Station times** are deterministic modelling values set by the team during the camp. They are not published factory measurements.

## Figures

- Scene2Model board: [`images/scene2model/scene2model-assembly-line.png`](../images/scene2model/scene2model-assembly-line.png)
- BPMN: [`models/bpmn/`](../models/bpmn/)

# Optimisation scenarios

[← back to README](../README.md)

## Scenarios

| | Baseline (`NEMO.alp`) | Optimised (`NEMO_Reworked.alp`) |
|---|---|---|
| Flashing lanes | 1 | **4** (`selectOutput5`, 25% each; failed re-flashes return to the lane selector) |
| Flashing experts | 1 | **3** |
| Socket / Mat / Housing | 3 dedicated operators | **1 shared `MultiOperator`** |
| Buttons | 2 operators × 6 s | 1 operator × 12 s |
| All other stations and quality gates | unchanged | unchanged |

### 1. Parallel flashing — implemented and evaluated

*"Running flashing lanes in parallel so the 20 s wait no longer creates the bottleneck"* (slide 8). With four lanes, the flashing stage can release up to about four controllers per 20 s instead of one.

### 2. Shared multi-skilled operator — implemented and evaluated

The presentation lists *"resource pools: operators as a constrained, shareable capacity"* among what the twin captures (slide 8). In the optimised model, AS10 Socket, AS20 Mat and AS30 Housing all draw on one `MultiOperator` pool. The chart calls it *Assembly Operator*. In the baseline these three operators were each only ≈ 7% utilised; the shared operator reaches ≈ 85%. This is a first, static version of the **adaptive workforce** idea in OASYS. Dynamic, demand-driven reassignment is not modelled.

## Results

| | Baseline | Optimised |
|---|---|---|
| Time between finished units (slide 11) | ≈ 24 s | ≈ 13.3 s |
| Throughput (derived) | ≈ 150 units/h | ≈ 271 units/h |
| Bottleneck | Flashing | Buttons |

Details and reproduction: [results/results-summary.md](../results/results-summary.md).

## Note on the Buttons station

The presentation lists *"a second Buttons operator relieving the slowest manual station"* as an optimisation (slide 8). The model files saved after the camp do not contain this change:

- `NEMO.alp` (baseline): `ButtonsOperator` capacity **2**, `ButtonsStation` 6 s.
- `NEMO_Reworked.alp` (optimised): `ButtonsOperator` capacity **1**, `ButtonsStation` 12 s.

The reported 13.3 s corresponds exactly to the optimised file as saved: 12 s ÷ (0.95 × 0.95) ≈ 13.3 s, with Buttons at 100% utilisation (also on slide 11). The improvement documented here is therefore credited to **parallel flashing plus the shared operator pool**. A second Buttons operator remains a scenario for future work. A what-if in the Python replication (not run in AnyLogic) suggests it would reduce the time between finished units to about 6.6 s, with Buttons still the constraint.

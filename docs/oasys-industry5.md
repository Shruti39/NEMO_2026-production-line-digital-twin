# OASYS — Operator-aware Assembly SYStem (proposed concept)

[← back to README](../README.md)

> **Status:** concept presented at NEMO 2026 (slides 12–18). No component below has been implemented in code, except the static shared-operator pool in the optimised AnyLogic model.

*"Optimization got us a faster assembly line. The operator is still on their own."* The simulation gave the team a line with higher capacity and more balanced resource utilisation. OASYS asks the next question: how can the line also become **human-centric, resilient and adaptive**? It is framed as *"a human-centric resilience layer for automotive assembly lines"* and *"a closed loop that senses pressure, decides where support is needed and acts before performance deteriorates."*

## Three components

### 1. Human Digital Twin

| Data collection | Output | Action |
|---|---|---|
| Consented wearable and workstation signals: stress, cycle-time variance, working and break time | A regression model predicting dips in performance, i.e. a strain-risk indicator | Smarter work and break schedules; dynamic breaks when workforce is available |

*"A decision signal: not a worker score."* The purpose is to manage operator strain, not to rank or monitor individuals.

### 2. Adaptive workforce

Operators become one multi-skilled, shareable pool instead of being locked to a station, and assignment follows demand. Expected benefits: absorbing demand highs and lows without overtime chaos, and no operator left under-utilised.
*Implementation status:* a single shared operator for three stations is simulated; assignment that adapts to demand, absences or bottlenecks is proposed.

### 3. AI-enabled guidance

Step-level visual guidance at complex, variant-heavy operations, primarily button placement. Expected benefits: lower scrap, less mental strain, faster onboarding. *"Knowledge lives in the station, not in one person."*
*Implementation status:* proposed. No computer-vision, AR or guidance software exists in this project.

## Possible AI roles (slide 17)

| Role | Predicts / does | Example use in OASYS |
|---|---|---|
| Classification | Is the operator or station in a normal or high-risk condition? | trigger support |
| Regression | Future cycle time, throughput, performance deterioration | Human Digital Twin output |
| Forecasting | Future demand, workload, production pressure (time-series models) | plan staffing |
| Decision model | Rotation, micro-breaks, extra support, AR guidance | close the loop |

## Responsible AI and worker privacy

The presentation commits to consented signals and to *"a decision signal, not a worker score."* Any real implementation would additionally need:

- **Consent and purpose limitation:** explicit, revocable opt-in; data used only for strain management and support, never for performance appraisal or discipline.
- **Data minimisation and aggregation:** station-level or anonymised indicators wherever possible; physiological data treated as sensitive health-related data under GDPR, with a data-protection impact assessment.
- **Worker participation:** co-design with operators and their representatives (in Germany, for example, works-council co-determination on monitoring technology).
- **Human in the loop:** recommendations (breaks, rotation, support) are suggestions to supervisors and operators, not automatic sanctions.
- **Transparency:** operators can see what is measured, what the model recommends and why.

These points are the authors' considerations for future work, not features of the current project.

## Link to Industry 5.0

The European Commission describes Industry 5.0 as complementing Industry 4.0 by orienting research and innovation towards a **sustainable, human-centric and resilient** European industry ([EC](https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/industry-50_en); [Breque et al., 2021](https://research-and-innovation.ec.europa.eu/knowledge-publications-tools-and-data/publications/all-publications/industry-50_en)). The CoDEMO project behind NEMO 2026 uses the same three dimensions: green, resilient, human-oriented ([OMiLAB — CoDEMO](https://omilab.org/activities/codemo/)).

| Dimension | Expected OASYS contribution (slide 18) | Evidence so far |
|---|---|---|
| Human-centric | Reduced cognitive load at the station; earlier relief before overload sets in; AR guidance | concept |
| Resilience | Absorbs demand spikes; handles variant changes; covers absences; faster bottleneck recovery | partly indicated: the shared operator pool raised throughput in simulation |
| Sustainability | Less scrap and rework; fewer wasted labour-hours; lower energy per good unit | concept; not modelled |

All contributions in this table are hypotheses to be tested, not measured outcomes.

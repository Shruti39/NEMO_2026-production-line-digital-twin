# Independent replication (cross-check)

`replicate.py` is a small SimPy re-implementation of the two AnyLogic models. It was written after the camp for this repository and has two purposes:

1. to **interpret** the indicator reported as "Throughput: 24 s → 13.3 s", and
2. to let readers without an AnyLogic licence **check** the reported numbers.

It is **not** the digital twin, and it was not part of the team's camp work. Where the `.alp` files leave a parameter at its AnyLogic default, the script uses the same default: arrival rate 1/s, `Delay` capacity 1, resource-pool capacity 1.

```bash
pip install simpy
python replicate.py               # 10 seeds
python replicate.py --seeds 20    # used for results/results-summary.md
```

Output for 20 seeds (20 000 s horizon, 2 000 s warm-up): [`../../results/replication-output.txt`](../../results/replication-output.txt).

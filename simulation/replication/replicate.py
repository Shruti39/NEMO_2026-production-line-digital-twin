"""
Independent cross-check of the two AnyLogic models (NOT the digital twin itself).

This script re-implements the block structure and parameters read from
`simulation/anylogic/baseline/NEMO.alp` and
`simulation/anylogic/optimised/NEMO_Reworked.alp` in SimPy, so that the
performance indicator reported in the team presentation can be interpreted
and checked without an AnyLogic licence.

Assumptions mirror AnyLogic defaults where the .alp files leave a parameter
unset:
  * Source: arrival rate 1 unit / second (AnyLogic default) -> the line is
    saturated and its output rate equals its bottleneck capacity.
  * Delay blocks ("WaitForFlashing*"): capacity 1 (AnyLogic default).
  * Resource pools: capacity 1 unless set explicitly in the model.
  * All processing times are deterministic, as in the models.
  * Queues are unbounded (maximumCapacity = true in the models).

Usage:
    pip install simpy
    python replicate.py            # 10 seeds per scenario
    python replicate.py --seeds 30 --horizon 50000
"""
import argparse
import random
import statistics

import simpy

FLASH_OP_S = 2.0        # FlashingStart* service
FLASH_WAIT_S = 20.0     # WaitForFlashing* delay
RETRY_OP_S = 6.0        # RetryFlashing service
P_FLASH_OK = 0.95       # Success
P_RETRY_OK = 0.60       # Success4 (otherwise scrapped)
P_EOL_OK = 0.95         # Success2
P_VALID_OK = 0.95       # Success3

SCENARIOS = {
    #            flash lanes, flashing experts, buttons operators, buttons time, shared pool for socket/mat/housing
    "baseline":  dict(lanes=1, experts=1, buttons_ops=2, buttons_s=6.0,  shared_pool=False),
    "optimised": dict(lanes=4, experts=3, buttons_ops=1, buttons_s=12.0, shared_pool=True),
}


def simulate(cfg, horizon, warmup, seed):
    rng = random.Random(seed)
    env = simpy.Environment()

    expert = simpy.Resource(env, cfg["experts"])
    lanes = [simpy.Resource(env, 1) for _ in range(cfg["lanes"])]
    retry_wait = simpy.Resource(env, 1)
    if cfg["shared_pool"]:
        multi = simpy.Resource(env, 1)  # MultiOperator in NEMO_Reworked.alp
        socket = mat = housing = multi
    else:
        socket, mat, housing = (simpy.Resource(env, 1) for _ in range(3))
    buttons = simpy.Resource(env, cfg["buttons_ops"])
    tester, validator, packer = (simpy.Resource(env, 1) for _ in range(3))

    busy = {}
    finished = []

    def service(res, t, key=None):
        with res.request() as req:
            yield req
            start = env.now
            yield env.timeout(t)
            if key and start >= warmup:
                busy[key] = busy.get(key, 0.0) + t

    def unit():
        # Flashing with retry loop
        while True:
            lane = rng.choice(lanes)  # selectOutput5: equal probabilities
            yield from service(expert, FLASH_OP_S, "flashing_expert")
            yield from service(lane, FLASH_WAIT_S)
            if rng.random() < P_FLASH_OK:
                break
            yield from service(expert, RETRY_OP_S, "flashing_expert")
            yield from service(retry_wait, FLASH_WAIT_S)
            if rng.random() >= P_RETRY_OK:
                return  # scrap
        shared = "assembly_operator" if cfg["shared_pool"] else None
        yield from service(socket, 1.5, shared or "socket_operator")
        yield from service(mat, 1.5, shared or "silicon_mat_operator")
        yield from service(housing, 1.5, shared or "base_housing_operator")
        yield from service(buttons, cfg["buttons_s"], "buttons_operator")
        yield from service(tester, 5.0)
        if rng.random() >= P_EOL_OK:
            return  # scrap
        yield from service(validator, 4.0)
        if rng.random() >= P_VALID_OK:
            return  # scrap
        yield from service(packer, 6.0)
        finished.append(env.now)

    def source():
        while True:
            env.process(unit())
            yield env.timeout(1.0)

    env.process(source())
    env.run(until=horizon)

    span = horizon - warmup
    done = [t for t in finished if t >= warmup]
    caps = {"flashing_expert": cfg["experts"], "buttons_operator": cfg["buttons_ops"]}
    util = {k: v / span / caps.get(k, 1) for k, v in busy.items()}
    return span / len(done), 3600.0 * len(done) / span, util


def mean_ci(xs):
    m = statistics.mean(xs)
    if len(xs) < 2:
        return m, 0.0
    return m, 1.96 * statistics.stdev(xs) / len(xs) ** 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--horizon", type=float, default=20000.0, help="simulated seconds")
    ap.add_argument("--warmup", type=float, default=2000.0, help="simulated seconds")
    args = ap.parse_args()

    for name, cfg in SCENARIOS.items():
        runs = [simulate(cfg, args.horizon, args.warmup, s) for s in range(1, args.seeds + 1)]
        tbu, ci_t = mean_ci([r[0] for r in runs])
        tph, ci_h = mean_ci([r[1] for r in runs])
        print(f"\n[{name}]  {args.seeds} seeds, {args.horizon:.0f} s horizon, {args.warmup:.0f} s warm-up")
        print(f"  mean time between finished units : {tbu:6.1f} s  (±{ci_t:.1f}, 95% CI)")
        print(f"  throughput                       : {tph:6.0f} units/h (±{ci_h:.0f})")
        for k in sorted(runs[0][2]):
            m, ci = mean_ci([r[2][k] for r in runs])
            print(f"  utilisation {k:<22}: {m:5.2f}  (±{ci:.2f})")


if __name__ == "__main__":
    main()

# nova_miner

The library available to miner code inside the sandbox. It ships in the sandbox
image at `site-packages/nova_miner`.

## Contents

- `utils.oracle` — `Oracle.score()` requests Boltz-2 affinity predictions over the
  broker's unix socket; `combine()` reduces one prediction to the NOVA score.
- `utils.molecules` — SMILES lookup, heavy-atom counts, MACCS entropy, chemical
  identity grouping.
- `utils.reactions` — reaction count and validity.
- `combinatorial_db` — the reaction database and SMILES construction from `rxn:` names.

## Scoring

```python
import os
from nova_miner.utils.oracle import Oracle, combine
from nova_miner.utils.molecules import get_heavy_atom_count

oracle = Oracle(os.environ["ORACLE_SOCKET"])
rows = oracle.score(targets=[target_sequence], smiles=[smiles])
score = combine(rows[0]["scores"][0], get_heavy_atom_count(smiles))
```

Higher is better. `combine` returns `-inf` where the oracle returned no prediction.
One request covers every (molecule, target) pair, so pass all targets at once.

For inexpensive screening, `Oracle.score` also accepts an optional `boltz2`
mapping. Supported keys are `recycling_steps`, `sampling_steps`,
`diffusion_samples`, their `_affinity` counterparts, and `step_scale`. The
broker validates and bounds every value before forwarding it. Omission selects
the canonical configuration; the validator always omits this mapping for final
scoring.

## Runtime

The sandbox has no network and no GPU: `ORACLE_SOCKET` is the only route out, and
the broker stamps each request with the run's identity. Logging is the standard
library's — configure handlers in your entrypoint to see it.

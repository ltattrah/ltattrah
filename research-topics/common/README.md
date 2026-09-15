# Shared tooling

Small pieces every topic's `experiments/` code imports so that provenance and reproduction conventions are identical across the portfolio.

- `provenance.py` – records git commit, Python and OS versions, CPU, seed, and a configuration hash for every run, and writes a `run.json` next to the raw outputs.
- `requirements.txt` – the common Python analysis stack. Each topic adds its own `experiments/requirements.txt` for engine clients, network tools, or study frameworks.

Usage from a topic folder:

```python
import sys; sys.path.insert(0, '../../common')
from provenance import Run

with Run(out_dir='runs', config=cfg, seed=cfg['seed']) as run:
    ...  # write raw outputs into run.dir
```

#!/usr/bin/env python3
"""Create or cleanly reset the Task 22 simulation from immutable fixtures."""
import argparse
from pathlib import Path
import yaml
from adaptive_backtest import init, root

p=argparse.ArgumentParser(); p.add_argument('--backtest-id', required=True); p.add_argument('--reset', action='store_true'); a=p.parse_args()
r=root(a.backtest_id)
if not (r/'config.yaml').exists() or not (r/'replay_evidence.yaml').exists():
    raise SystemExit('create the versioned config.yaml and replay_evidence.yaml for this id before initialization')
config=yaml.safe_load((r/'config.yaml').read_text())
r=init(a.backtest_id, config, reset=a.reset)
print(f'initialized {r}')

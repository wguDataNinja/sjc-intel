#!/usr/bin/env python3
import argparse
from adaptive_backtest import run_week
p=argparse.ArgumentParser(); p.add_argument('--backtest-id',required=True); p.add_argument('--week-start',required=True); p.add_argument('--week-end',required=True); p.add_argument('--dry-run',action='store_true'); a=p.parse_args()
r=run_week(a.backtest_id,a.week_start,a.week_end,a.dry_run); print(f"{r['run_id']}: {len(r['findings'])} findings, {len(r['evaluator']['accepted'])} accepted")

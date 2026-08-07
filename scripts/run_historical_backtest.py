#!/usr/bin/env python3
import argparse
from adaptive_backtest import run_backtest
p=argparse.ArgumentParser(); p.add_argument('--backtest-id',required=True); p.add_argument('--start',required=True); p.add_argument('--end',required=True); a=p.parse_args()
print(run_backtest(a.backtest_id,a.start,a.end))

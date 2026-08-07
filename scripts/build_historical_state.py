#!/usr/bin/env python3
import argparse
from adaptive_backtest import root, state_for, dump, day
p=argparse.ArgumentParser(); p.add_argument('--backtest-id',required=True); p.add_argument('--as-of',required=True); a=p.parse_args()
r=root(a.backtest_id); state=state_for(r, day(a.as_of)); dump(r/'visible_state'/f'{a.as_of}.yaml',state); print(f'visible state written: {r}/visible_state/{a.as_of}.yaml')

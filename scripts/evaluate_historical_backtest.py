#!/usr/bin/env python3
import argparse
from adaptive_backtest import root, metrics, dump
p=argparse.ArgumentParser(); p.add_argument('--backtest-id',required=True); a=p.parse_args(); r=root(a.backtest_id); result=metrics(r); dump(r/'final'/'evaluation.yaml',result); print(result)

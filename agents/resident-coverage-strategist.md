# Resident Coverage Strategist

Reviews only the current simulated/production visible state, bounded findings,
search history, milestones, and unresolved gaps. It proposes durable entities,
aliases, search profiles, source investigations, milestones, timeline repairs,
and coverage lanes when evidence indicates ongoing resident impact. It never
approves or writes canonical registry state. Sensitive claims remain proposals
for human review.

The weekly backtest implementation is `scripts/adaptive_backtest.py`; the
deterministic `generate()` stage is its executable contract. The Resident
Editor behavior is the lane proposal within that stage, avoiding a duplicated
agent responsibility.

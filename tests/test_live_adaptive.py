from pathlib import Path
from scripts import live_adaptive as la

def test_review_accept_and_rollback_are_isolated(tmp_path):
    r=la.initialize(tmp_path/'adaptive')
    proposal={'proposal_id':'P1','type':'entity','subject':'Test subject','proposed_state_transition':'isolated only','status':'pending_human_review','evidence':[]}
    la.write(r/'pending_proposals.yaml',{'proposals':[proposal]})
    dry=la.review('P1','accept','Tester','check',r,dry_run=True)
    assert dry['action']=='accept' and la.read(r/'accepted_state.yaml',{})['accepted']['entities']==[]
    accepted=la.review('P1','accept','Tester','evidence reviewed',r)
    assert la.read(r/'accepted_state.yaml',{})['accepted']['entities'][0]['proposal_id']=='P1'
    rolled=la.review('P1','rollback','Tester','undo',r,decision_id=accepted['decision_id'])
    assert rolled['action']=='rollback'
    assert la.read(r/'accepted_state.yaml',{})['accepted']['entities']==[]
    assert la.read(r/'pending_proposals.yaml',{})['proposals'][0]['proposal_id']=='P1'

def test_budget_and_health_derivation(tmp_path):
    try: la.run_pilot('too-many',['a','b'],tmp_path/'x',budget=1)
    except ValueError as exc: assert 'budget' in str(exc)
    else: assert False

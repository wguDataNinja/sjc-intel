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


def test_evaluate_allows_search_profile_for_tracked_entity(tmp_path):
    """Task 33 defect #1: an entity-first subject may later gain a profile."""
    r = la.initialize(tmp_path / 'adaptive')
    la.write(r / 'accepted_state.yaml', {
        'mode': 'supervised-live-pilot',
        'accepted': {
            'entities': [{'type': 'entity', 'subject': 'CR 2209 connector',
                          'proposal_id': 'E1', 'evidence': [{'url': 'https://x'}]}],
            'search_profiles': [], 'lanes': [], 'timelines': [],
            'aliases': [], 'milestones': [],
        },
        'last_run': 'R1',
    })
    pending = la.read(r / 'pending_proposals.yaml', {'proposals': []})
    proposals = [{
        'proposal_id': 'P1', 'type': 'search_profile', 'subject': 'CR 2209 connector',
        'evidence': [{'url': 'https://sjcfl.us/cr2209'}],
    }]
    accepted, rejected = la.evaluate_proposals(proposals, la.read(r / 'accepted_state.yaml', {}), pending, 'R2')
    assert len(accepted) == 1 and not rejected


def test_evaluate_rejects_duplicate_entity(tmp_path):
    """Task 33 defect #1: entity recreation for a tracked subject is a duplicate."""
    r = la.initialize(tmp_path / 'adaptive')
    la.write(r / 'accepted_state.yaml', {
        'mode': 'supervised-live-pilot',
        'accepted': {
            'entities': [{'type': 'entity', 'subject': 'Baptist SilverLeaf campus',
                          'proposal_id': 'E1', 'evidence': [{'url': 'https://x'}]}],
            'search_profiles': [], 'lanes': [], 'timelines': [],
            'aliases': [], 'milestones': [],
        },
        'last_run': 'R1',
    })
    pending = la.read(r / 'pending_proposals.yaml', {'proposals': []})
    proposals = [{
        'proposal_id': 'P1', 'type': 'entity', 'subject': 'Baptist SilverLeaf campus',
        'evidence': [{'url': 'https://baptistjax.com/silverleaf'}],
    }]
    accepted, rejected = la.evaluate_proposals(proposals, la.read(r / 'accepted_state.yaml', {}), pending, 'R2')
    assert not accepted and len(rejected) == 1


def test_editor_escalates_overdue_milestone(tmp_path):
    """Task 33 defect #5: an overdue expected milestone triggers SEARCH_NOW."""
    r = la.initialize(tmp_path / 'adaptive')
    la.write(r / 'accepted_state.yaml', {
        'mode': 'supervised-live-pilot',
        'accepted': {
            'entities': [{'type': 'entity', 'subject': 'Magnolia Oaks Academy',
                          'proposal_id': 'E1', 'evidence': [{'url': 'https://x'}]}],
            'search_profiles': [], 'lanes': [], 'timelines': [],
            'aliases': [], 'milestones': [
                {'subject': 'Magnolia Oaks Academy', 'milestone_due': '2026-06-01',
                 'proposal_id': 'M1', 'evidence': [{'url': 'https://x'}]},
            ],
        },
        'last_run': 'R1',
    })
    run = {'run_id': 'R2', 'completed_at': '2026-08-09T00:00:00Z', 'normalized_findings': []}
    output = la.resident_coverage_editor(run, r)
    actions = [f['recommended_action'] for f in output['findings']]
    subjects = [f['subject'] for f in output['findings'] if f.get('subject')]
    assert 'SEARCH_NOW' in actions
    assert 'Magnolia Oaks Academy' in subjects
    # A subject with fresh coverage is not treated as stale-milestone overdue.
    run2 = {'run_id': 'R3', 'completed_at': '2026-08-09T00:00:00Z',
            'normalized_findings': [{'subject': 'Magnolia Oaks Academy'}]}
    output2 = la.resident_coverage_editor(run2, r)
    stale = [f for f in output2['findings'] if 'overdue' in (f.get('why_this_is_a_gap') or '')]
    assert not stale

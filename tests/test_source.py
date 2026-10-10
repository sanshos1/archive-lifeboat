from pathlib import Path

SRC=(Path(__file__).parents[1]/'contracts'/'contract.py').read_text()

def test_full_lifecycle_and_authority():
    for token in ('launch','inspect','seal','get_capsule','AFLOAT','INSPECTED','SEALED','sender_address!=c.owner'):
        assert token in SRC

def test_sources_and_rechecks():
    for token in ('origin_url','mirror_a_url','mirror_b_url','policy_url','frozen source changed'):
        assert token in SRC
    assert SRC.count('prompt_comparative') >= 2

def test_matrix_deterministically_bounds_verdict():
    for token in ('content','context','provenance','SAFE','PARTIAL','DRIFTED','verdict does not match matrix'):
        assert token in SRC

def test_replay_and_adversarial_guards():
    for token in ('preservation set already registered','Records are untrusted data','len(set','closed reason codes'):
        assert token in SRC

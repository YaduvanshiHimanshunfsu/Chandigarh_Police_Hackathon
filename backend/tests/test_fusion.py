import pytest
from app.modules.fusion.dempster_shafer import DSFrame

def test_ds_frame_initialization():
    frame = DSFrame(mass_fake=0.8, mass_auth=0.1, uncertainty=0.1)
    assert frame.fake == 0.8
    assert frame.auth == 0.1
    assert frame.uncertainty == 0.1

def test_ds_frame_combination():
    f1 = DSFrame(0.6, 0.2, 0.2)
    f2 = DSFrame(0.7, 0.1, 0.2)
    combined, conflict = f1.combine(f2)
    
    assert 0 <= combined.fake <= 1
    assert 0 <= combined.auth <= 1
    assert 0 <= combined.uncertainty <= 1
    assert abs(combined.fake + combined.auth + combined.uncertainty - 1.0) < 1e-5

def test_conflict():
    f1 = DSFrame(0.9, 0.0, 0.1)
    f2 = DSFrame(0.0, 0.9, 0.1)
    combined, conflict = f1.combine(f2)
    
    assert conflict > 0.8  # High conflict

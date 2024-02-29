import pytest
from ophyd.sim import make_fake_device
from i10_bluesky.devices.detectorSlits import DetectorSlits

@pytest.fixture
def fake_detector_slits():
    FakeDetectorSlits = make_fake_device(DetectorSlits)
    fake_detector_slits: DetectorSlits= FakeDetectorSlits(name="detector slits")
    return fake_detector_slits


def test_detector_slits_creation(fake_detector_slits: DetectorSlits):
    fake_detector_slits.wait_for_connection()


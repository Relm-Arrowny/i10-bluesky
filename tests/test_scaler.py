import pytest
from ophyd.sim import make_fake_device

from i10_bluesky.devices.scalerCard import ScaleCard


@pytest.fixture
def fake_scaler():
    FakeScaleCard = make_fake_device(ScaleCard)
    fake_scaler: ScaleCard = FakeScaleCard(name="detector slits")
    return fake_scaler


def test_scaler_creation(fake_scaler: ScaleCard):
    fake_scaler.wait_for_connection()

import asyncio
from unittest.mock import Mock, call

import pytest
from ophyd_async.core import (
    DeviceCollector,
    set_sim_put_proceeds,
    set_sim_value,
)

from i10_bluesky.devices.rasor.detectorSlits import DetectorSlits

pytestmark = pytest.mark.asyncio

A_BIT = 0.001


@pytest.fixture
async def simSlits():
    async with DeviceCollector(sim=True):
        simSlits = DetectorSlits("BLxxI-MO-TABLE", "ds")
        # Signals connected here

    aSlits = ["dsd", "dsu"] 
    assert simSlits.dsd.name == "ds-dsd"

    set_sim_value(simSlits.dsd.units, "mm")
    set_sim_value(simSlits.dsd.precision, 3)
    set_sim_value(simSlits.dsd.velocity, 1)

    yield simSlits

def fake_motor(start:float, end:float, step:float):
    for newPosition in range(start,end,step):
        yield newPosition



async def test_motor_moving_well(simSlits: DetectorSlits) -> None:
    set_sim_put_proceeds(simSlits.dsd.setpoint, False)
    s = simSlits.dsd.set(0.55)
    watcher = Mock()
    s.watch(watcher)
    done = Mock()
    s.add_callback(done)
    await asyncio.sleep(A_BIT)
    assert watcher.call_count == 1
    assert watcher.call_args == call(
        name="ds-dsd",
        current=0.0,
        initial=0.0,
        target=0.55,
        unit="mm",
        precision=3,
        time_elapsed=pytest.approx(0.0, abs=0.05),
    )
    watcher.reset_mock()
    assert 0.55 == await simSlits.dsd.setpoint.get_value()
    assert not s.done
    await asyncio.sleep(0.1)
    set_sim_value(simSlits.dsd.readback, 0.1)
    assert watcher.call_count == 1
    assert watcher.call_args == call(
        name="ds-dsd",
        current=0.1,
        initial=0.0,
        target=0.55,
        unit="mm",
        precision=3,
        time_elapsed=pytest.approx(0.1, abs=0.05),
    )
    set_sim_put_proceeds(simSlits.dsd.setpoint, True)
    await asyncio.sleep(A_BIT)
    assert s.done
    done.assert_called_once_with(s)

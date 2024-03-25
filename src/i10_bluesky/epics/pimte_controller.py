import asyncio
from typing import Optional, Set

from ophyd_async.core import AsyncStatus, DetectorControl, DetectorTrigger
from ophyd_async.epics.areadetector.drivers.ad_base import (
    DEFAULT_GOOD_STATES,
    DetectorState,
    start_acquiring_driver_and_ensure_status,
)
from ophyd_async.epics.areadetector.utils import ImageMode, stop_busy_record

from i10_bluesky.epics.drivers.pimte1_driver import Pimte1Driver, TriggerMode

TRIGGER_MODE = {
    DetectorTrigger.internal: TriggerMode.internal,
    DetectorTrigger.constant_gate: TriggerMode.ext_trigger,
    DetectorTrigger.variable_gate: TriggerMode.ext_trigger,
}


class PimteController(DetectorControl):
    def __init__(
        self,
        driver: Pimte1Driver,
        good_states: Set[DetectorState] = set(DEFAULT_GOOD_STATES),
    ) -> None:
        self.driver = driver
        self.good_states = good_states

    def get_deadtime(self, exposure: float) -> float:
        return 0.001

    def _process_setting(self):
        self.driver.initialize.set(1)

    def set_temperature(self, temperature: float) -> None:
        self.driver.temperture.set(temperature)
        self._process_setting()

    def set_speed(self, speed: int) -> None:
        self.driver.speed.set(speed)
        self._process_setting()

    async def arm(
        self,
        num: int,
        trigger: DetectorTrigger = DetectorTrigger.internal,
        exposure: Optional[float] = None,
    ) -> AsyncStatus:
        await asyncio.gather(
            self.driver.trigger_mode.set(TRIGGER_MODE[trigger]),
            self.driver.num_images.set(999_999 if num == 0 else num),
            self.driver.image_mode.set(ImageMode.multiple),
        )
        return await start_acquiring_driver_and_ensure_status(
            self.driver, good_states=self.good_states
        )

    async def disarm(self):
        await stop_busy_record(self.driver.acquire, False, timeout=1)

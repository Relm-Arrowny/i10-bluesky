import asyncio
from typing import Optional, set

from ophyd_async.core import AsyncStatus, DetectorControl, DetectorTrigger
from ophyd_async.epics.areadetector.drivers.ad_base import (
    DEFAULT_GOOD_STATES,
    DetectorState,
    start_acquiring_driver_and_ensure_status,
)
from ophyd_async.epics.areadetector.utils import ImageMode, stop_busy_record

from i10_bluesky.epics.drivers.pimte1_driver import Pimte1Driver, SpeedMode, TriggerMode

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

    def _process_setting(self) -> None:
        self.driver.initialize.set(1)

    async def setTemperature(self, temperature: float) -> None:
        await self.driver.setTemperture.set(temperature)
        self._process_setting()

    async def setSpeed(self, speed: SpeedMode) -> None:
        await self.driver.setTemperture.set(speed)
        self._process_setting()

    async def arm(
        self,
        num: int = 1,
        exposure: Optional[float] = None,
        trigger: DetectorTrigger = DetectorTrigger.internal,
    ) -> AsyncStatus:

        if exposure is None:
            exposure = await asyncio.create_task(self.driver.acquire_time.get_value())

        await asyncio.gather(
            self.driver.trigger_mode.set(TRIGGER_MODE[trigger]),
            self.driver.acquire_time.set(exposure),
            self.driver.num_images.set(999_999 if num == 0 else num),
            self.driver.image_mode.set(ImageMode.multiple),
        )

        return await start_acquiring_driver_and_ensure_status(
            self.driver, good_states=self.good_states
        )

    async def disarm(self):
        await stop_busy_record(self.driver.acquire, False, timeout=1)

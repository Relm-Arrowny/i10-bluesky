import asyncio

from bluesky import plan_stubs as bps
from bluesky import preprocessors as bpp
from bluesky.utils import Msg, short_uid
from ophyd_async.core import DetectorTrigger, StandardDetector, TriggerInfo

from i10_bluesky.devices.pimteAD import HDFStatsPimte
from i10_bluesky.epics.drivers.pimte1_driver import Pimte1Driver

"""
    AdPlan store the state of an area detector and its associated functions.


"""


class AdPlan:
    def __init__(self, det: StandardDetector) -> None:
        self.exposure: float = 0.002
        self.trigger: DetectorTrigger = DetectorTrigger.internal
        self.n_img: int = 1
        self.det: HDFStatsPimte = det
        self.deadtime: float = self.det.controller.get_deadtime(self.exposure)

    """
        Bare min to take an image using prepare plan with full detector control
    """

    def takeImg(
        self,
        exposure: float = None,
        n_img: int = None,
        det_trig: DetectorTrigger = None,
    ):
        self._updateDetInfo(exposure, n_img, det_trig)
        grp = short_uid("prepare")

        @bpp.stage_decorator([self.det])
        @bpp.run_decorator()
        def innerTakeImg():
            yield from bps.declare_stream(self.det, name="primary")
            yield from bps.kickoff(self.det, group=grp, wait=True)
            yield from bps.prepare(self.det, self._getTriggerInfo, group=grp, wait=True)
            # yield from bps.complete(self.det, group = grp, wait = True)
            yield from bps.wait(
                group=grp
            )  # wait within the bps plan seem to have no effect hence wait here
            return (yield from bps.complete(self.det, group=grp, wait=True))

        return (yield from innerTakeImg())

    def _updateDetInfo(
        self,
        exposure: float = None,
        n_img: int = None,
        det_trig: DetectorTrigger = None,
    ) -> None:
        if exposure is not None:
            self.exposure = exposure
            self.deadtime = self.det.controller.get_deadtime(self.exposure)
        if n_img is not None:
            self.n_img = n_img
        if det_trig is not None:
            self.det_trig = det_trig

    def _getTriggerInfo(self) -> TriggerInfo:
        return TriggerInfo(self.n_img, self.trigger, self.deadtime, self.exposure)

    def setTemp(self, temp):
        asyncio.create_task(self.det.controller.set_temperature(temp))
        yield Msg("read", self.det.drv.read_backtemperture)

    def setAdcSpeed(self, speed: Pimte1Driver.SpeedMode):
        asyncio.create_task(self.det.controller.set_speed(speed))
        yield Msg("read", self.det.drv.speed)

    """
        Static function for trigger with changable count time
    """

    def tiggerImg(dets: StandardDetector, value: int):
        yield Msg("set", dets.drv.acquire_time, value)

        @bpp.stage_decorator([dets])
        @bpp.run_decorator()
        def innerTiggerImg():
            return (yield from bps.trigger_and_read([dets]))

        return (yield from innerTiggerImg())

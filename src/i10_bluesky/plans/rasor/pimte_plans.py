from bluesky.utils import Msg
from ophyd_async.core import DetectorTrigger, StandardDetector, TriggerInfo


class AdPlan:
    def __init__(self, det: StandardDetector) -> None:
        self.exposure: float = 0.002
        self.trigger: DetectorTrigger = DetectorTrigger.internal
        self.n_img: int = 1
        self.det: StandardDetector = det
        self.deadtime: float = self.det.controller.get_deadtime(self.exposure)

    def takeImg(
        self,
        exposure: float = None,
        n_img: int = None,
        det_trig: DetectorTrigger = None,
    ) -> Msg:
        self._updateDetInfo(exposure, n_img, det_trig)
        return AdPlan.tiggerImg(self.det, self._getTriggerInfo())

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

    def tiggerImg(det: StandardDetector, value: TriggerInfo):
        yield Msg("stage", det)
        yield Msg("prepare", det, value)
        yield Msg("unstage", det)

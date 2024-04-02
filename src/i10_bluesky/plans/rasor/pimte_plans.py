from bluesky.utils import Msg
from ophyd_async.core import StandardDetector, TriggerInfo


class AdPlan:
    def __init__(self) -> None:
        pass

    def takeImg(det: StandardDetector, value: TriggerInfo):
        yield Msg("prepare", det, value)


"""
@dataclass(frozen=True)
class TriggerInfo:
    #: Number of triggers that will be sent
    num: int
    #: Sort of triggers that will be sent
    trigger: DetectorTrigger
    #: What is the minimum deadtime between triggers
    deadtime: float
    #: What is the maximum high time of the triggers
    livetime: float"""

from enum import Enum

from ophyd_async.epics.areadetector.drivers.ad_base import ADBase
from ophyd_async.epics.areadetector.utils import ad_rw


class TriggerMode(str, Enum):
    internal = "Free Run"
    ext_trigger = "Ext Trigger"
    bulb_mode = "Bulb Mode"


class Pimte1Driver(ADBase):
    def __init__(self, prefix: str) -> None:
        self.trigger_mode = ad_rw(TriggerMode, prefix + "TriggerMode")
        self.initialize = ad_rw(int, prefix + "Initialize")
        self.temperture = ad_rw(float, prefix + "SetTemperature")
        self.speed = ad_rw(int, prefix + "SpeedSelection")
        super().__init__(prefix)

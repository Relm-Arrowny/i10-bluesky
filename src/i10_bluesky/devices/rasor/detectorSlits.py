from ophyd_async.core import Device
from ophyd_async.epics.motion.motor import Motor


class DetectorSlits(Device):

    def __init__(self, prefix: str, name="") -> None:
        self.dsu = Motor(prefix + "-01:TRANS")
        self.dsd = Motor(prefix + "-02:TRANS")
        super().__init__(name=name)

"""
from ophyd import Component, Device, EpicsMotor


class DetectorSlits(Device):
    dsu = Component(EpicsMotor, "-01:TRANS")
    dsd = Component(EpicsMotor, "-02:TRANS")
"""

from ophyd_async.core import Device
from ophyd_async.epics.motion.motor import Motor


class DetectorSlits(Device):

    def __init__(self, prefix: str, name="") -> None:
        self.dsu = Motor(prefix + "-01:TRANS")
        self.dsd = Motor(prefix + "-02:TRANS")
        super().__init__(name=name)


"""
class Slits(StandardReadable):
    # basic slits class

    def __init__(self, prefix: str, suffix: str, name: str = "") -> None:
        # Define some signals
        self.value = epics_signal_r(float, prefix + suffix)
        # Set name and signals for read() and read_configuration()
        self.set_readable_signals(
            read=[self.value],
            # config=[self.mode],
        )
        super().__init__(name=name)
"""

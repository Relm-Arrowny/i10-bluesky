from ophyd import Component, Device, EpicsMotor, EpicsSignalRO


class DetectorSlits(Device):
    dsu = Component(EpicsMotor, "dsu")
    dsd = Component(EpicsMotor, "dsd")
    


#Try but async not yet suport fake_fake_device
"""


from ophyd_async.core import StandardReadable
from ophyd_async.epics.signal.signal import epics_signal_r
class slits(StandardReadable):
#basic slits class

    def __init__(self, prefix: str, suffix: str, name:str ="") -> None:
        # Define some signals
        self.value = epics_signal_r(float, prefix + suffix)
        # Set name and signals for read() and read_configuration()
        self.set_readable_signals(
            read=[self.value],
            #config=[self.mode],
        )
        super().__init__(name=name)

"""


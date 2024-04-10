from ophyd import Component, Device, EpicsSignal


class ScaleCard(Device):
    for i in range(1, 2):
        macr17 = Component(EpicsSignal, ":SCALER1.S' + str(i) + '")


"""
class Scaler(StandardReadable):
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

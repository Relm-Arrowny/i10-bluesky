from ophyd import Component, Device, EpicsSignal


class ScaleCard(Device):
    for i in range(1,33):
        exec('macr' + str(i) + ' =  Component(EpicsSignal, ":SCALER1.S' + str(i) +'")')

# from enum import Enum

# from bluesky import preprocessors as bpp
# from bluesky.callbacks.fitting import PeakStats
# from bluesky.plan_stubs import abs_set
# from bluesky.plans import scan
# from dodal.common.types import MsgGenerator
# from dodal.devices.i10.slits import I10Slits
# from ophyd_async.core import StandardReadable
# from ophyd_async.epics.motor import Motor


# class PeakPosition(int, Enum):
#     COM = 2
#     CEN = 3


# def scan_and_move(
#     det: StandardReadable,
#     motor: Motor,
#     start: float,
#     end: float,
#     num: int,
#     loc: PeakPosition = PeakPosition.CEN,
# ) -> MsgGenerator:
#     ps = yield from find_peak_centre(
#         motor=motor, det=det, start=start, end=end, num=num
#     )
#     yield from abs_set(motor, ps["stats"][loc], wait=True)


# def find_peak_centre(
#     det: StandardReadable, motor: Motor, start: float, end: float, num: int
# ) -> MsgGenerator:
#     ps = PeakStats(f"{motor.name}", f"{det.name}")

#     yield from bpp.subs_wrapper(
#         scan([det], motor, start, end, num=num),
#         ps,
#     )
#     return ps

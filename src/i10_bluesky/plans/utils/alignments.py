from enum import Enum

from bluesky import preprocessors as bpp
from bluesky.callbacks.fitting import PeakStats
from bluesky.plan_stubs import abs_set
from bluesky.plans import scan
from dodal.common.types import MsgGenerator
from ophyd_async.core import StandardReadable
from ophyd_async.epics.motor import Motor
from p99_bluesky.plans.fast_scan import fast_scan_1d


class PeakPosition(int, Enum):
    COM = 2
    CEN = 3


def scan_and_move_cen(
    det: StandardReadable,
    motor: Motor,
    start: float,
    end: float,
    num: int,
    loc: PeakPosition = PeakPosition.CEN,
) -> MsgGenerator:
    ps = PeakStats(f"{motor.name}", f"{det.name}")

    yield from bpp.subs_wrapper(
        scan([det], motor, start, end, num=num),
        ps,
    )
    yield from abs_set(motor, ps["stats"][loc], wait=True)


def fast_scan_and_move_cen(
    det: StandardReadable,
    motor: Motor,
    start: float,
    end: float,
    motor_speed: float | None = None,
    loc: PeakPosition = PeakPosition.CEN,
) -> MsgGenerator:
    ps = PeakStats(f"{motor.name}", f"{det.name}")

    yield from bpp.subs_wrapper(
        fast_scan_1d(
            dets=[det], motor=motor, start=start, end=end, motor_speed=motor_speed
        ),
        ps,
    )
    yield from abs_set(motor, ps["stats"][loc], wait=True)

from collections.abc import Callable
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


def scan_and_move_cen(funcs) -> Callable:
    def inner(**kwargs):
        ps = PeakStats(
            f"{kwargs['motor'].name}",
            f"{kwargs['det'].name}",
            calc_derivative_and_stats=True,
        )

        yield from bpp.subs_wrapper(
            funcs(**kwargs),
            ps,
        )
        yield from abs_set(kwargs["motor"], ps["stats"][kwargs["loc"]], wait=True)

    return inner


@scan_and_move_cen
def step_scan_and_move_cen(
    det: StandardReadable,
    motor: Motor,
    start: float,
    end: float,
    num: int,
    loc: PeakPosition = PeakPosition.CEN,
) -> MsgGenerator:
    return scan([det], motor, start, end, num=num)


@scan_and_move_cen
def fast_scan_and_move_cen(
    det: StandardReadable,
    motor: Motor,
    start: float,
    end: float,
    motor_speed: float | None = None,
    loc: PeakPosition = PeakPosition.CEN,
) -> MsgGenerator:
    return fast_scan_1d([det], motor, start, end, motor_speed=motor_speed)

from dodal.beamlines.beamline_utils import device_instantiation, get_directory_provider
from dodal.beamlines.beamline_utils import set_beamline as set_utils_beamline
from dodal.log import set_beamline as set_log_beamline
from dodal.utils import get_beamline_name

from i10_bluesky.devices.pimteAD import HDFStatsPimte

BL = get_beamline_name("BL10I")
set_log_beamline(BL)
set_utils_beamline(BL)


def pimte(
    wait_for_connection: bool = True, fake_with_ophyd_sim: bool = False
) -> HDFStatsPimte:
    return device_instantiation(
        HDFStatsPimte,
        "pimte",
        "-EA-PILAT-01:",
        wait_for_connection,
        fake_with_ophyd_sim,
        directory_provider=get_directory_provider(),
    )

from typing import Sequence

from bluesky.protocols import Hints
from ophyd_async.core import DirectoryProvider, SignalR, StandardDetector
from ophyd_async.core.async_status import AsyncStatus
from ophyd_async.epics.areadetector.drivers import ADBaseShapeProvider
from ophyd_async.epics.areadetector.writers import HDFWriter, NDFileHDF

from i10_bluesky.epics.drivers.pimte1_driver import Pimte1Driver
from i10_bluesky.epics.pimte_controller import PimteController


class HDFStatsPimte(StandardDetector):
    _controller: PimteController
    _writer: HDFWriter

    def __init__(
        self,
        prefix: str,
        directory_provider: DirectoryProvider,
        name: str,
        config_sigs: Sequence[SignalR] = (),
        **scalar_sigs: str,
    ):
        self.drv = Pimte1Driver(prefix + "CAM:")
        self.hdf = NDFileHDF(prefix + "HDF5:")
        # self.stats = NDPluginStats(prefix + "STAT:")
        # taken from i22 but this does nothing atm

        super().__init__(
            PimteController(self.drv),
            HDFWriter(
                self.hdf,
                directory_provider,
                lambda: self.name,
                ADBaseShapeProvider(self.drv),
                sum="StatsTotal",
                **scalar_sigs,
            ),
            config_sigs=config_sigs,
            name=name,
        )

    @AsyncStatus.wrap
    async def trigger(self) -> None:
        """Arm the detector and wait for it to finish."""
        indices_written = await self.writer.get_indices_written()
        written_status = await self.controller.arm(num=2)
        await written_status
        end_observation = indices_written + 1

        async for index in self.writer.observe_indices_written(
            self._frame_writing_timeout
        ):
            if index >= end_observation:
                break

    @property
    def hints(self) -> Hints:
        return self.writer.hints

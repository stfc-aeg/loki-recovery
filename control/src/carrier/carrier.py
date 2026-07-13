from loki.adapter import LokiCarrier_1v0, DeviceHandler
import logging

class LokiCarrier_self_test (LokiCarrier_1v0):
    def __init__(self, **kwargs):
        self._logger = logging.getLogger('LOKI-based Carrier')

        # Must currently be set to ~something~ due to bug
        self._default_clock_config = 'ZL30266_LOKI_Nosync_500MHz_218MHz.mfg'
        kwargs.setdefault('clkgen_base_dir', './clkgen/')


        # MUST call the superclass init LAST
        super(LokiCarrier_self_test, self).__init__(**kwargs)
        self._logger.info('LOKI super init complete')

    def _gen_app_paramtree(self):
        # This custom parameter tree function must be overridden, even if it is empty for now
        custom_pt = {
        }
        return custom_pt
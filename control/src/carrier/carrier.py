from loki.adapter import LokiCarrier_1v0, DeviceHandler
import logging
import time

class LokiCarrier_self_test (LokiCarrier_1v0):
    def __init__(self, **kwargs):
        self._logger = logging.getLogger('LOKI-based Carrier')

        # Must currently be set to ~something~ due to bug
        self._default_clock_config = 'ZL30266_LOKI_Nosync_500MHz_218MHz.mfg'
        kwargs.setdefault('clkgen_base_dir', './clkgen/')

        kwargs.setdefault('pin_config_is_input_leds_enable', False) 

        # MUST call the superclass init LAST
        super(LokiCarrier_self_test, self).__init__(**kwargs)
        self._logger.info('LOKI super init complete')

        self.leds_enable()

    def _gen_app_paramtree(self):
        # This custom parameter tree function must be overridden, even if it is empty for now
        custom_pt = {
            'run_LEDs' : (None, lambda var: self.LED_pattern(["led0", "led1", "led2", "led3", "led2", "led1", "led0" ]))
        }
        return custom_pt
    
    def LED_pattern(self, LED_list):
        #turns all 4 LEDs off
        for LED in range(4):
           self.leds_set_led("led"+str(LED), 0)
           #In the oder specified in LED_list flashes each LED on then off 
        for LED in LED_list:
           self.leds_set_led(LED, 1)
           time.sleep(1)
           self.leds_set_led(LED, 0)
           

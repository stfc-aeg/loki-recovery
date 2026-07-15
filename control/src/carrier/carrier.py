from loki.adapter import LokiCarrier_1v0, DeviceHandler
import logging
import time

class LokiCarrier_self_test (LokiCarrier_1v0):
    def __init__(self, **kwargs):
        self._logger = logging.getLogger('LOKI-based Carrier')

        # Must currently be set to ~something~ due to bug
        self._default_clock_config = 'ZL30266_LOKI_Nosync_500MHz_218MHz.mfg'
        kwargs.setdefault('clkgen_base_dir', './clkgen/')

        # Bodged fix to enable LEDs should be removed at a later date
        kwargs.setdefault('pin_config_is_input_leds_enable', False) 

        # Sets a default order of LEDs to flash
        self.LED_trigger = False
        self.LED_list = ["led0", "led1", "led2", "led3", "led2", "led1", "led0" ]

        # MUST call the superclass init LAST
        super(LokiCarrier_self_test, self).__init__(**kwargs)
        self._logger.info('LOKI super init complete')

        self.leds_enable()

    # Function held in parameter tree, used to run LED pattern
    def set_LED_trigger(self, blank):
        self.LED_trigger = True

    # Function held in parameter tree, sanatises inputed list of LEDs and makes it the used list
    def set_LED_list(self, array):
        if type(array) != list:
            logging.error("inputted type is not list")
            raise TypeError("inputted type is not list")
        for LED in array:
            if not LED in self._leds_namelist:
                raise ValueError('Inputted value is not one of '+ str(self._leds_namelist)+ ": " +str(LED)+ " is the bad input") 
        
        self.LED_list = array

    def _gen_app_paramtree(self):
        # This custom parameter tree function must be overridden, even if it is empty for now
        custom_pt = {
            'run_LEDs' : (None, self.set_LED_trigger),
            'LED_list' : (lambda: self.LED_list, self.set_LED_list)
        }
        return custom_pt
    
    def LED_pattern(self, LED_list):
        # turns all 4 LEDs off
        for LED in range(4):
           self.leds_set_led("led"+str(LED), 0)
           # In the oder specified in LED_list flashes each LED on then off 
        for LED in LED_list:
           self.leds_set_led(LED, 1)
           time.sleep(1)
           self.leds_set_led(LED, 0)

    # Starts a background loop
    def _start_io_loops(self, options):
        super(LokiCarrier_self_test, self)._start_io_loops(options)

        self.add_thread("LEDs thread", self.LED_loop)
        self.watchdog_add_thread("LEDs thread", 30, lambda: logging.error("!!!! LED loop has failed or a pattern > 30 seconds long has been run !!!!"))

    # When LED_trigger==True runs the LED pattern and then sets LED_trigger to false
    def LED_loop(self):
        while not self.TERMINATE_THREADS:
            self.watchdog_kick()
            if self.LED_trigger:
                self.LED_pattern(self.LED_list)
                self.LED_trigger = False
            time.sleep(1)


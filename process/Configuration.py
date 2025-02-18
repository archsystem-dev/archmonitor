"""
Configuration.py
"""

import threading
import time

from process.configuration.change_argb_mode import change_argb_mode
from process.configuration.change_combo_collection import change_combo_collection
from process.configuration.change_pwm_steps import change_pwm_steps
from process.configuration.load_argb import load_argb
from process.configuration.load_cooling import load_cooling
from process.configuration.load_default_parameters import load_default_parameters
from process.configuration.load_theme import load_theme

# -------------------------------------------------------------

def hex_to_rgb(h):
    """
    :param h:
    :return:
    """

    h = h[1:]

    rgb = []
    for i in (0, 2, 4):
        decimal = int(h[i:i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)


def rgb_to_hex(rgb):
    """
    :param rgb:
    :return:
    """
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


class Configuration:
    """
    Class Configuration
    """

    def __init__(self, testing=False):

        self.breaker = False
        self.testing = testing
        self.modules = {}

        # -------------------------------------------------------------

        self.temperature_thd = None

        # -------------------------------------------------------------

        self.current_theme = {}

        # -------------------------------------------------------------

    def define_modules(self, modules):
        self.modules = modules

    def load_default_parameters(self):
        load_default_parameters(self)

    def load_theme(self, theme_name):
        load_theme(self, theme_name)

    def load_argb(self):
        load_argb(self)

    def load_cooling(self):
        load_cooling(self)

    def change_pwm_steps(self, steps):
        change_pwm_steps(self, steps)

    def change_combo_collection(self, keys, values, target):
        change_combo_collection(self, keys, values, target)

    def change_argb_mode(self, target):
        change_argb_mode(self, target)

    def generate(self):
        """
        generate()
        """

        configuration_uniqid = self.modules["archgui"].activate(
            model="configuration",
            title="Configuration")

        self.modules["archgui"].define_main(configuration_uniqid)

        self.load_default_parameters()

        self.load_theme(self.modules["data"].default["theme"])
        self.load_argb()
        self.load_cooling()

    # ----------------------------------------------------------------------------------------
    # Preview
    # ----------------------------------------------------------------------------------------

    def preview(self, theme, cooling):
        """
        :param theme:
        :param cooling:
        """

        self.modules["preview"].load_theme(theme)

        self.modules["preview"].print_preview_startup()
        self.modules["preview"].print_preview_in_use_off()
        self.modules["preview"].print_preview_in_use_on()
        self.modules["preview"].print_preview_standby_on()
        self.modules["preview"].print_preview_standby_off()

        self.modules["preview"].load_cooling(cooling)
        self.modules["preview"].print_preview_cooling()

    # ----------------------------------------------------------------------------------------
    # temperature
    # ----------------------------------------------------------------------------------------

    def temperature(self):
        """
        temperature()
        """

        while True:

            temp = self.modules["mpu"].get_result("temperature", "temp")

            if temp is not None:

                items = [
                    {
                        "item": "sensor_1_temp",
                        "mode": "replace",
                        "value": str(temp["sensor_1"]) + "°"
                    }, {
                        "item": "sensor_2_temp",
                        "mode": "replace",
                        "value": str(temp["sensor_2"]) + "°"
                    }, {
                        "item": "sensor_3_temp",
                        "mode": "replace",
                        "value": str(temp["sensor_3"]) + "°"
                    }
                ]

                self.modules["archgui"].update(items=items)

            time.sleep(1)

    # ----------------------------------------------------------------------------------------
    # run
    # ----------------------------------------------------------------------------------------

    def run(self):
        """
        run()
        """

        self.generate()
        self.preview(
            self.modules["data"].themes[self.modules["data"].default["theme"]],
            self.modules["data"].cooling
        )

        temperature_thd = threading.Thread(
            target=self.temperature,
            daemon=True)
        temperature_thd.start()

    # ----------------------------------------------------------------------------------------
    # stop
    # ----------------------------------------------------------------------------------------

    def stop(self):
        """
        stop()
        """

        self.breaker = True

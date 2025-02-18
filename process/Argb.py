"""
Argb.py
"""

import time
import signal
import numpy

from process.argb.fixe import fixe
from process.argb.mode_pulse import mode_pulse
from process.argb.mode_pulse_three_colors import mode_pulse_three_colors
from process.argb.mode_pulse_two_colors import mode_pulse_two_colors
from process.argb.mode_switch_three_colors import mode_switch_three_colors
from process.argb.mode_switch_two_colors import mode_switch_two_colors
from process.argb.off import off

from mpunified.MPUPrcWAC import MPUPrcWAC


def write_2812(spi, data):
    """
    :param spi:
    :param data:
    """

    d = numpy.array(data).ravel()
    tx = numpy.zeros(len(d) * 4, dtype=numpy.uint8)
    for ibit in range(4):
        tx[3 - ibit::4] = ((d >> (2 * ibit + 1)) & 1) * 0x60 + ((d >> (2 * ibit + 0)) & 1) * 0x06 + 0x88

    spi.xfer(tx.tolist(), int(4 / 1.25e-6))


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


class Argb(MPUPrcWAC):
    """
    Class Argb
    """

    def __init__(self, pipe):
        super().__init__(pipe)

        self.breaker = False
        self.testing = False

        # -------------------------------------------------------------

        self.default = {}
        self.argb ={}

        self.lock = False
        self.argb_in_running = None
        self.argb_selected = None

        # -------------------------------------------------------------

        self.mode = None
        self.color = None
        self.intensity_min = 0
        self.speed = 0

        # -------------------------------------------------------------

        self.phase = 0
        self.sequence = 0

        self.it = 0
        self.tr = 0
        self.tg = 0
        self.tb = 0

        self.dif_tr = 0
        self.dif_tg = 0
        self.dif_tb = 0

        # ----------------------------------------------------------------

        self.start_collect()

        # -------------------------------------------------------------

        if not self.testing:

            try:
                import spidev

                self.spi = spidev.SpiDev()
                self.spi.open(0, 0)
                self.spi.max_speed_hz = 250000
                self.spi.mode = 0
                
            except Exception as err:
                self.testing = True
                print("import spidev")
                print(f"Unexpected {err=}, {type(err)=}")

    def signal_handler(self, _, __):
        """
        :param self:
        :param _:
        :param __:
        """
        self.breaker = True

    def run(self):
        """
        run()
        """

        self.argb_in_running = self.default["argb"]
        self.argb_selected = self.default["argb"]

        while True:

            if self.breaker:
                break

            if self.argb_in_running != self.argb_selected:
                self.set_mode()

            if not self.lock:
                self.exec_mode()

            else:

                time.sleep(0.1)
                while True:
                    if not self.lock:
                        break
                    time.sleep(0.1)

    def set_mode(self):
        """
        set_mode()
        """

        self.lock = True

        time.sleep(0.1)

        self.mode = self.argb[self.argb_selected]["mode"]
        self.intensity_min = self.argb[self.argb_selected]["intensity_min"]
        self.speed = self.argb[self.argb_selected]["speed"]

        self.color = {
            "color_1": self.argb[self.argb_selected]["color_1"],
            "color_2": self.argb[self.argb_selected]["color_2"],
            "color_3": self.argb[self.argb_selected]["color_3"]
        }

        self.phase = 0
        self.sequence = 0

        color = self.compute_color("color_1")

        self.it = 100
        self.tr = color[0]
        self.tg = color[1]
        self.tb = color[2]

        self.argb_in_running = self.argb_selected
        self.lock = False

    def exec_mode(self):
        """
        exec_mode()
        """
        if self.mode == "off":
            self.off()
        if self.mode == "fixe":
            self.fixe()
        if self.mode == "pulse":
            self.mode_pulse()
        if self.mode == "pulse_two_colors":
            self.mode_pulse_two_colors()
        if self.mode == "pulse_three_colors":
            self.mode_pulse_three_colors()
        if self.mode == "switch_two_colors":
            self.mode_switch_two_colors()
        if self.mode == "switch_three_colors":
            self.mode_switch_three_colors()

    def compute_color(self, color_key):
        """
        Calcule la couleur RGB en fonction de l'intensité donnée.
        """
        return hex_to_rgb(self.color[color_key])

    def update_leds(self):
        """
        Met à jour les LEDs avec la couleur actuelle.
        """
        fi = [[int(self.tr * (self.it / 100)), int(self.tg * (self.it / 100)), int(self.tb * (self.it / 100))]] * self.argb["number"]
        if not self.testing:
            write_2812(self.spi, fi)

    def off(self):
        off(self)

    def fixe(self):
        fixe(self)

    def mode_pulse(self):
        mode_pulse(self)

    def mode_pulse_two_colors(self):
        mode_pulse_two_colors(self)

    def mode_pulse_three_colors(self):
        mode_pulse_three_colors(self)

    def mode_switch_two_colors(self):
        mode_switch_two_colors(self)

    def mode_switch_three_colors(self):
        mode_switch_three_colors(self)


def argb_run(pipe):
    """
    :param pipe:
    """
    argb = Argb(pipe)
    signal.signal(signal.SIGINT, argb.signal_handler)
    argb.run()

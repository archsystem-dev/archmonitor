"""
Argb.py
"""

import time
import signal
import numpy

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


def rgb_to_hex(rgb):
    """
    :param rgb:
    :return:
    """
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


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

    def exec_mode(self):
        """
        exec_mode()
        """
        if self.mode == "off":
            self.mode_off()
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

    def mode_off(self):
        """
        Affiche une seule couleur fixe sans variation.
        """
        self.tr, self.tg, self.tb = self.compute_color("color_1")
        self.update_leds()

        # Gestion du timing des mises à jour
        time.sleep(1 / (self.argb[self.argb_in_running]["speed"] * 10))

    def fixe(self):
        """
        Affiche une seule couleur fixe sans variation.
        """
        self.tr, self.tg, self.tb = self.compute_color("color_1")
        self.update_leds()

        # Gestion du timing des mises à jour
        time.sleep(1 / (self.argb[self.argb_in_running]["speed"] * 10))

    def mode_pulse(self):
        """
        Gère une seule couleur avec une variation progressive d’intensité.
        """

        phase_it_down = [0]
        phase_it_up = [1]

        self.tr, self.tg, self.tb = self.compute_color("color_1")

        self.update_leds()

        # Augmentation ou baisse de l'intensité
        if self.phase in phase_it_up:
            self.it += 1

        if self.phase in phase_it_down:
            self.it -= 1

        # Transition de phase
        if self.it == 100 or self.it == self.intensity_min:
            self.sequence = 0
            if self.phase == 0:
                self.phase = 1
            else:
                self.phase = 0
        else:
            self.sequence += 1

        # Gestion du timing des mises à jour
        time.sleep(1 / (self.argb[self.argb_in_running]["speed"] * 10))

    def mode_pulse_two_colors(self):

        color = None
        phase_it_down = [0, 2]
        phase_it_up = [1, 3]

        if self.phase in [1, 3]:

            if self.phase == 1:
                color = self.compute_color("color_2")
            if self.phase == 3:
                color = self.compute_color("color_1")

            if self.sequence == 0:
                self.dif_tr = (max(color[0], self.tr) - min(color[0], self.tr)) / (100 - self.intensity_min)
                self.dif_tg = (max(color[1], self.tg) - min(color[1], self.tg)) / (100 - self.intensity_min)
                self.dif_tb = (max(color[2], self.tb) - min(color[2], self.tb)) / (100 - self.intensity_min)

            if color[0] > self.tr:
                self.tr += self.dif_tr
            elif color[0] < self.tr:
                self.tr -= self.dif_tr

            if color[1] > self.tg:
                self.tg += self.dif_tg
            elif color[1] < self.tg:
                self.tg -= self.dif_tg

            if color[2] > self.tb:
                self.tb += self.dif_tb
            elif color[2] < self.tb:
                self.tb -= self.dif_tb

            if self.sequence == self.intensity_min - 1:
                self.tr = color[0]
                self.tg = color[1]
                self.tb = color[2]

        self.update_leds()

        # Augmentation ou baisse de l'intensité
        if self.phase in phase_it_up:
            self.it += 1

        if self.phase in phase_it_down:
            self.it -= 1

        # Transition de phase
        if self.it == 100 or self.it == self.intensity_min:
            self.sequence = 0
            if self.phase < 3:
                self.phase += 1
            else:
                self.phase = 0
        else:
            self.sequence += 1

        # Gestion du timing des transitions
        time.sleep(1 / (self.argb[self.argb_in_running]["speed"] * 10))


    def mode_pulse_three_colors(self):

        color = None
        phase_it_down = [0, 2, 4]
        phase_it_up = [1, 3, 5]

        if self.phase in [1, 3, 5]:

            if self.phase == 1:
                color = self.compute_color("color_2")
            if self.phase == 3:
                color = self.compute_color("color_3")
            if self.phase == 5:
                color = self.compute_color("color_1")

            if self.sequence == 0:
                self.dif_tr = (max(color[0], self.tr) - min(color[0], self.tr)) / (100 - self.intensity_min)
                self.dif_tg = (max(color[1], self.tg) - min(color[1], self.tg)) / (100 - self.intensity_min)
                self.dif_tb = (max(color[2], self.tb) - min(color[2], self.tb)) / (100 - self.intensity_min)

            if color[0] > self.tr:
                self.tr += self.dif_tr
            elif color[0] < self.tr:
                self.tr -= self.dif_tr

            if color[1] > self.tg:
                self.tg += self.dif_tg
            elif color[1] < self.tg:
                self.tg -= self.dif_tg

            if color[2] > self.tb:
                self.tb += self.dif_tb
            elif color[2] < self.tb:
                self.tb -= self.dif_tb

            if self.sequence == self.intensity_min - 1:
                self.tr = color[0]
                self.tg = color[1]
                self.tb = color[2]

        self.update_leds()

        # Augmentation ou baisse de l'intensité
        if self.phase in phase_it_up:
            self.it += 1

        if self.phase in phase_it_down:
            self.it -= 1

        # Transition de phase
        if self.it == 100 or self.it == self.intensity_min:
            self.sequence = 0
            if self.phase < 5:
                self.phase += 1
            else:
                self.phase = 0
        else:
            self.sequence += 1

        # Gestion du timing des transitions
        time.sleep(1 / (self.argb[self.argb_in_running]["speed"] * 10))

    def mode_switch_two_colors(self):

        color = None

        if self.phase == 0:
            color = self.compute_color("color_2")
        if self.phase == 1:
            color = self.compute_color("color_1")

        if self.sequence == 0:
            self.dif_tr = (max(color[0], self.tr) - min(color[0], self.tr)) / ((100 - self.speed) * 10)
            self.dif_tg = (max(color[1], self.tg) - min(color[1], self.tg)) / ((100 - self.speed) * 10)
            self.dif_tb = (max(color[2], self.tb) - min(color[2], self.tb)) / ((100 - self.speed) * 10)

        if color[0] > self.tr:
            self.tr += self.dif_tr
        elif color[0] < self.tr:
            self.tr -= self.dif_tr

        if color[1] > self.tg:
            self.tg += self.dif_tg
        elif color[1] < self.tg:
            self.tg -= self.dif_tg

        if color[2] > self.tb:
            self.tb += self.dif_tb
        elif color[2] < self.tb:
            self.tb -= self.dif_tb

        if self.sequence == ((100 - self.speed) * 10):
            self.tr = color[0]
            self.tg = color[1]
            self.tb = color[2]

        self.update_leds()

        # Transition de phase
        if self.sequence == ((100 - self.speed) * 10):
            self.sequence = 0
            if self.phase == 0:
                self.phase = 1
            else:
                self.phase = 0

        else:
            self.sequence += 1

        # Gestion du timing des transitions
        time.sleep(1 / (self.argb[self.argb_in_running]["speed"] * 10))

    def mode_switch_three_colors(self):

        color = None

        if self.phase == 0:
            color = self.compute_color("color_2")
        if self.phase == 1:
            color = self.compute_color("color_3")
        if self.phase == 2:
            color = self.compute_color("color_1")

        if self.sequence == 0:
            self.dif_tr = (max(color[0], self.tr) - min(color[0], self.tr)) / ((100 - self.speed) * 10)
            self.dif_tg = (max(color[1], self.tg) - min(color[1], self.tg)) / ((100 - self.speed) * 10)
            self.dif_tb = (max(color[2], self.tb) - min(color[2], self.tb)) / ((100 - self.speed) * 10)

        if color[0] > self.tr:
            self.tr += self.dif_tr
        elif color[0] < self.tr:
            self.tr -= self.dif_tr

        if color[1] > self.tg:
            self.tg += self.dif_tg
        elif color[1] < self.tg:
            self.tg -= self.dif_tg

        if color[2] > self.tb:
            self.tb += self.dif_tb
        elif color[2] < self.tb:
            self.tb -= self.dif_tb

        if self.sequence == ((100 - self.speed) * 10):
            self.tr = color[0]
            self.tg = color[1]
            self.tb = color[2]

        self.update_leds()

        # Transition de phase
        if self.sequence == ((100 - self.speed) * 10):
            self.sequence = 0
            if self.phase < 2:
                self.phase += 1
            else:
                self.phase = 0

        else:
            self.sequence += 1

        # Gestion du timing des transitions
        time.sleep(1 / (self.argb[self.argb_in_running]["speed"] * 10))


def argb_run(pipe):
    """
    :param pipe:
    """
    argb = Argb(pipe)
    signal.signal(signal.SIGINT, argb.signal_handler)
    argb.run()

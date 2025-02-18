"""
Display.py
"""
import time
import threading

from PIL import Image, ImageFont

from process.display.pre_print_argb import pre_print_argb
from process.display.pre_print_mode import pre_print_mode
from process.display.pre_print_pwm import pre_print_pwm
from process.display.pre_print_standby import pre_print_standby

from process.display.print_active_argb import print_active_argb
from process.display.print_active_mode import print_active_mode
from process.display.print_active_standby import print_active_standby

from process.display.print_degree import print_degree
from process.display.print_pwm import print_pwm
from process.display.print_rpm import print_rpm

class Display:
    """
    Class Display
    """

    def __init__(self, testing=False):

        self.breaker = False
        self.startup = True
        self.testing = testing
        self.modules = {}

        # -------------------------------------------------------------

        self.window = None
        self.figures = None

        self.graph_startup = "graph_startup"
        self.graph_monitor = "graph_monitor"
        self.graph_standby = "graph_standby"

        # -------------------------------------------------------------

        self.dimension = (800, 480)

        self.default = None
        self.gpio = None
        self.theme = None

        self.font = None
        self.images = None

        self.power = 0
        self.mode = None
        self.argb = None

        self.pwm = {
            "soc": None,
            "cpu": None,
            "gpu": None,
            "case": None,
            "pump_1": None,
            "pump_2": None,
        }

        self.rpm = {
            "soc": None,
            "cpu": None,
            "gpu": None,
            "case": None,
            "pump_1": None,
            "pump_2": None,
        }

        self.temp = {
            "soc": 0,
            "sensor_1": 0,
            "sensor_2": 0,
            "sensor_3": 0,
        }

    def define_modules(self, modules):
        """
        :param modules:
        """
        self.modules = modules

    def hex_to_rgb(self, h):
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

    def list_to_tuple(self, ll):
        """
        :param ll:
        :return:
        """
        return tuple(self.list_to_tuple(x) for x in ll) if type(ll) is list else ll

    # ----------------------------------------------------------------------------------------
    # Pre Print Standby
    # ----------------------------------------------------------------------------------------

    def pre_print_argb(self):
        pre_print_argb(self)

    def pre_print_mode(self):
        pre_print_mode(self)

    def pre_print_pwm(self, target):
        pre_print_pwm(self, target)

    def pre_print_standby(self):
        pre_print_standby(self)

    # ----------------------------------------------------------------------------------------
    # Print Active
    # ----------------------------------------------------------------------------------------

    def print_active_argb(self, argb):
        print_active_argb(self, argb)

    def print_active_mode(self, mode):
        print_active_mode(self, mode)

    def print_active_standby(self):
        print_active_standby(self)

    # ----------------------------------------------------------------------------------------
    # Print TXT
    # ----------------------------------------------------------------------------------------

    def print_degree(self, target, degree):
        print_degree(self, target, degree)

    def print_pwm(self, target, value):
        print_pwm(self, target, value)

    def print_rpm(self, target, rpm):
        print_rpm(self, target, rpm)

    # ----------------------------------------------------------------------------------------
    # Generate
    # ----------------------------------------------------------------------------------------

    def generate(self):
        """
        generate()
        """

        self.window = self.modules["archgui"].activate(model="main", title="Archmonitor")
        self.modules["archgui"].define_main(self.window)

        self.figures = {}

        self.modules["archgui"].update(
            uniqid=self.window,
            items=[
                {
                    "item": self.graph_startup,
                    "mode": "show"
                },
                {
                    "item": self.graph_monitor,
                    "mode": "hide"
                },
            ])

        self.modules["archgui"].bind(
            uniqid=self.window,
            binds=[
                {
                    "item": self.graph_monitor,
                    "bind_string": "<Button-1>",
                    "bind_key": " button-1"
                },
                {
                    "item": self.graph_standby,
                    "bind_string": "<Button-1>",
                    "bind_key": " button-1"
                }
            ])

        self.figures["logo"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph_startup,
            location=(10, 10),
            image=self.images["logo"])

        self.modules["archgui"].update(
            uniqid=self.window,
            items=[
                {
                    "item": self.graph_startup,
                    "mode": "show"
                },
                {
                    "item": self.graph_monitor,
                    "mode": "hide"
                },
                {
                    "item": self.graph_standby,
                    "mode": "hide"
                }
            ])

        self.startup = True
        self.figures = {"mode": {}, "argb": {}, "pwm": {}, "temp": {
            "soc": ["startup"],
            "cpu": ["startup"],
            "gpu": ["startup"],
            "case": ["startup"],
        }, "rpm": {
            "soc": ["startup"],
            "cpu": ["startup"],
            "gpu": ["startup"],
            "case": ["startup"],
            "pump_1": ["startup"],
            "pump_2": ["startup"],
        }, "standby": {}, "background": self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph_monitor,
            location=(10, 10),
            image=self.images["background"])}

        self.pre_print_argb()
        self.pre_print_mode()
        self.pre_print_standby()

        for target in self.pwm:
            self.pre_print_pwm(target)

    # ----------------------------------------------------------------------------------------
    # Reveal
    # ----------------------------------------------------------------------------------------

    def reveal(self):
        """
        reveal()
        """

        startup_count = 0
        display_pre_active = True

        time.sleep(2)

        while True:

            if self.breaker:
                break

            if self.startup:
                startup_count += 1

            if startup_count > 10 and self.startup:

                power = self.modules["mpu"].get_result("listener", "power")

                items=[
                    {
                        "item": self.graph_startup,
                        "mode": "hide"
                    }
                ]

                if power:
                    items.append({
                        "item": self.graph_monitor,
                        "mode": "show"
                    })
                    items.append({
                        "item": self.graph_standby,
                        "mode": "hide"
                    })
                else:
                    items.append({
                        "item": self.graph_monitor,
                        "mode": "hide"
                    })
                    items.append({
                        "item": self.graph_standby,
                        "mode": "show"
                    })

                self.modules["archgui"].update(
                    uniqid=self.window,
                    items=items)

                mode = self.modules["mpu"].get_result("listener", "mode")

                if mode != self.mode:
                    self.print_active_mode(mode)
                    self.mode = mode

                # --------------------------------

                argb = self.modules["mpu"].get_result("listener", "argb")

                if argb != self.argb:
                    self.print_active_argb(argb)
                    self.argb = argb

                # --------------------------------

                self.startup = False

            elif self.startup is False:

                power = self.modules["mpu"].get_result("listener", "power")

                if power != self.power:

                    self.modules["archgui"].graph_send_figure_to_back(
                        uniqid=self.window,
                        graph=self.graph_standby,
                        figure=self.figures["standby"]["on"])

                    self.modules["archgui"].graph_bring_figure_to_front(
                        uniqid=self.window,
                        graph=self.graph_monitor,
                        figure=self.figures["standby"]["off"])

                    if power:
                        items = [{
                            "item": self.graph_monitor,
                            "mode": "show"
                        },{
                            "item": self.graph_standby,
                            "mode": "hide"
                        }]

                        self.modules["archgui"].graph_send_figure_to_back(
                            uniqid=self.window,
                            graph=self.graph_monitor,
                            figure=self.figures["background"])
                    else:
                        items = [{
                            "item": self.graph_monitor,
                            "mode": "hide"
                        },{
                            "item": self.graph_standby,
                            "mode": "show"
                        }]

                    self.modules["archgui"].update(
                        uniqid=self.window,
                        items=items)

                    self.power = power

                if self.power:

                    pwm = self.modules["mpu"].get_result("listener", "pwm")

                    if pwm is not None:
                        for target in self.pwm:

                            if isinstance(pwm[target], int):
                                pwm_divided = int(pwm[target] * float(len(self.figures["pwm"][target]["off"]) / 100))
                                if pwm_divided != self.pwm[target]:
                                    self.print_pwm(target, pwm_divided)

                    # --------------------------------

                    rpm = self.modules["mpu"].get_result("listener", "rpm")

                    if rpm is not None:
                        for target in self.rpm:

                            if isinstance(rpm[target], int):
                                if rpm[target] != self.rpm[target]:
                                    self.print_rpm(target, rpm[target])
                                    self.rpm[target] = rpm[target]

                    # --------------------------------

                    temp = self.modules["mpu"].get_result("listener", "temp")

                    if temp is not None:
                        for target in self.temp:
                            self.print_degree(target, temp[target])
                            self.temp[target] = temp[target]


                if display_pre_active:
                    self.print_active_argb(self.default["argb"])
                    self.print_active_mode(self.default["mode"])
                    display_pre_active = False

            time.sleep(0.1)

    # ----------------------------------------------------------------------------------------
    # run
    # ----------------------------------------------------------------------------------------

    def run(self):
        """
        run()
        """

        self.default = self.modules["data"].default
        self.gpio = self.modules["data"].gpio
        self.theme = self.modules["data"].themes[self.default["theme"]]

        theme_dir = self.modules["data"].script_dir + "/themes/" + self.default["theme"] + "/"

        self.images = {
            "background": Image.open(theme_dir + self.theme["images"]["background"]),
            "logo": Image.open(theme_dir + self.theme["images"]["logo"]),
            "standby":{
                "off": Image.open(theme_dir + self.theme["images"]["standby_off"]),
                "on": Image.open(theme_dir + self.theme["images"]["standby_on"])
            },
            "argb": {},
            "mode": {},
            "pwm_step": {
                "off": [],
                "on": []
            }
        }

        for i in ["a", "b", "c", "d", "e", "f"]:
            argb = {
                "off": Image.open(theme_dir + self.theme["images"]["argb_" + i + "_off"]),
                "on": Image.open(theme_dir + self.theme["images"]["argb_" + i + "_on"])
            }
            self.images["argb"][i] = argb

        for i in ["silent", "performance"]:
            mode = {
                "off": Image.open(theme_dir + self.theme["images"]["mode_" + i + "_off"]),
                "on": Image.open(theme_dir + self.theme["images"]["mode_" + i + "_on"]),
            }
            self.images["mode"][i] = mode

        pwm_step_off = []
        pwm_step_on = []

        for i in range(1, self.theme["global"]["pwm_steps"] + 1, 1):
            pwm_step_off.append(Image.open(theme_dir + self.theme["images"]["pwm_step_" + str(i) + "_off"]))
            pwm_step_on.append(Image.open(theme_dir + self.theme["images"]["pwm_step_" + str(i) + "_on"]))

        self.images["pwm_step"]["off"] = pwm_step_off
        self.images["pwm_step"]["on"] = pwm_step_on

        self.font = {"temp": {}, "rpm": {}}

        for temp in ["soc", "cpu", "gpu", "case"]:
            self.font["temp"][temp] = ImageFont.truetype(
                theme_dir + self.theme["temp"][temp]["f"],
                self.theme["temp"][temp]["s"])

        for rpm in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
            self.font["rpm"][rpm] = ImageFont.truetype(
                theme_dir + self.theme["rpm"][rpm]["f"],
                self.theme["rpm"][rpm]["s"])

        # -------------------------------------------------------------

        self.generate()

        reveal = threading.Thread(
            target=self.reveal,
            daemon=True)
        reveal.start()

    # ----------------------------------------------------------------------------------------
    # stop
    # ----------------------------------------------------------------------------------------

    def stop(self):
        """
        stop()
        """

        self.breaker = True

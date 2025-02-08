"""
Configuration.py
"""

import threading
import time

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
        """
        :param modules:
        """
        self.modules = modules

    def load_default_parameters(self):
        """
        load_default_parameters()
        """

        items = [
            {
                "item": "parameters_theme",
                "mode": "replace",
                "value": list(self.modules["data"].themes),
                "default_value": self.modules["data"].default["theme"]
            }, {
                "item": "parameters_mode",
                "mode": "replace",
                "value": ["silent", "performance"],
                "default_value": self.modules["data"].default["mode"]
            }, {
                "item": "parameters_argb",
                "mode": "replace",
                "value": ["a", "b", "c", "d", "e", "f"],
                "default_value": self.modules["data"].default["argb"]
            }
        ]

        self.modules["archgui"].update(items=items)

    def load_theme(self, theme_name):
        """
        :param theme_name:
        """

        theme = self.modules["data"].themes[theme_name]
        self.current_theme = theme
        self.change_pwm_steps(theme["global"]["pwm_steps"])

        items = [
            {
                "item": "theme_name",
                "mode": "replace",
                "value": theme_name,
            },
            {
                "item": "theme_select",
                "mode": "replace",
                "value": list(self.modules["data"].themes),
                "default_value": self.modules["data"].default["theme"]
            }, {
                "item": "theme_background_color",
                "mode": "replace",
                "value": theme["global"]["background_color"]
            }, {
                "item": "theme_pwm_steps",
                "mode": "replace",
                "value": self.modules["data"].pwm_steps_values,
                "default_value": theme["global"]["pwm_steps"]
            }, {
                "item": "theme_pwm_steps_orientation",
                "mode": "replace",
                "value": self.modules["data"].pwm_steps_orientation_value,
                "default_value": theme["global"]["pwm_steps_orientation"]
            }, {
                "item": "theme_logo",
                "mode": "replace",
                "value": theme["images"]["logo"]
            }, {
                "item": "theme_background",
                "mode": "replace",
                "value": theme["images"]["background"]
            }, {
                "item": "theme_standby_off",
                "mode": "replace",
                "value": theme["images"]["standby_off"]
            }, {
                "item": "theme_standby_on",
                "mode": "replace",
                "value": theme["images"]["standby_on"]
            }
        ]

        # ---------------------------------------------------
        # Theme Images
        # ---------------------------------------------------

        for i in ["argb", "mode", "pwm", "rpm", "temp"]:

            jj = []

            if i == "argb":
                jj = ["a", "b", "c", "d", "e", "f"]

            if i == "mode":
                jj = ["silent", "performance"]

            for j in jj:
                items.append({
                    "item": "theme_" + i + "_" + j + "_off",
                    "mode": "replace",
                    "value": theme["images"][i + "_" + j + "_off"]
                })
                items.append({
                    "item": "theme_" + i + "_" + j + "_on",
                    "mode": "replace",
                    "value": theme["images"][i + "_" + j + "_on"]
                })

        for step in range(theme["global"]["pwm_steps"]):
            items.append({
                "item": "theme_pwm_step_" + str(step + 1) + "_off",
                "mode": "replace",
                "value": theme["images"]["pwm_step_" + str(step + 1) + "_off"]
            })
            items.append({
                "item": "theme_pwm_step_" + str(step + 1) + "_on",
                "mode": "replace",
                "value": theme["images"]["pwm_step_" + str(step + 1) + "_on"]
            })

        # ---------------------------------------------------
        # Theme Fonts
        # ---------------------------------------------------

        font_size = []
        for s in range(31):
            font_size.append(s + 10)

        for i in ["rpm", "temp"]:
            for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
                if j in theme[i]:
                    for k in ["f", "s", "h", "w", "bgc", "c"]:
                        if k == "s":
                            items.append({
                                "item": "theme_" + i + "_" + j + "_" + k,
                                "mode": "replace",
                                "value": font_size,
                                "default_value": theme[i][j][k]
                            })
                        else:
                            items.append({
                                "item": "theme_" + i + "_" + j + "_" + k,
                                "mode": "replace",
                                "value": theme[i][j][k]
                            })

        # ---------------------------------------------------
        # Theme Positions
        # ---------------------------------------------------

        for i in ["argb", "mode", "pwm", "rpm", "temp"]:

            jj = []

            if i == "argb":
                jj = ["a", "b", "c", "d", "e", "f"]

            if i == "mode":
                jj = ["silent", "performance"]

            if i in ["pwm", "rpm"]:
                jj = ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]

            if i == "temp":
                jj = ["soc", "cpu", "gpu", "case"]

            for j in jj:
                items.append({
                    "item": "theme_" + i + "_" + j + "_x",
                    "mode": "replace",
                    "value": theme[i][j]["x"]
                })
                items.append({
                    "item": "theme_" + i + "_" + j + "_y",
                    "mode": "replace",
                    "value": theme[i][j]["y"]
                })

        self.modules["archgui"].update(items=items)

    def load_argb(self):
        """
        load_argb()
        """

        items = [{
            "item": "argb_number_led",
            "mode": "replace",
            "value": self.modules["data"].number_argb_values,
            "default_value": self.modules["data"].argb["number"]
        }]

        for i in self.modules["data"].argb_app:
            items.append({
                "item": "argb_" + i + "_mode",
                "mode": "replace",
                "value": self.modules["data"].argb_mode,
                "default_value": self.modules["data"].argb[i]["mode"]
            })
            items.append({
                "item": "argb_" + i + "_color_1",
                "mode": "replace",
                "value": self.modules["data"].argb[i]["color_1"]
            })
            items.append({
                "item": "argb_" + i + "_color_2",
                "mode": "replace",
                "value": self.modules["data"].argb[i]["color_2"]
            })
            items.append({
                "item": "argb_" + i + "_color_3",
                "mode": "replace",
                "value": self.modules["data"].argb[i]["color_3"]
            })
            items.append({
                "item": "argb_" + i + "_intensity_min",
                "mode": "replace",
                "value": self.modules["data"].intensity_min_values,
                "default_value": self.modules["data"].argb[i]["intensity_min"]
            })
            items.append({
                "item": "argb_" + i + "_speed",
                "mode": "replace",
                "value": self.modules["data"].speed_values,
                "default_value": self.modules["data"].argb[i]["speed"]
            })

        self.modules["archgui"].update(items=items)

        for i in self.modules["data"].argb_app:
            self.change_argb_mode("argb_" + i + "_mode")

    def load_cooling(self):
        """
        load_cooling()
        """

        items = []
        for i in ["silent", "performance"]:

            for j in ["cpu", "gpu", "case"]:
                items.append({
                    "item": "cooling_" + i + "_" + j + "_pwm_min",
                    "mode": "replace",
                    "value": self.modules["data"].pwm_values,
                    "default_value": self.modules["data"].cooling[i][j]["pwm_min"]
                })
                items.append({
                    "item": "cooling_" + i + "_" + j + "_pwm_max",
                    "mode": "replace",
                    "value": self.modules["data"].pwm_values,
                    "default_value": self.modules["data"].cooling[i][j]["pwm_max"]
                })
                items.append({
                    "item": "cooling_" + i + "_" + j + "_temp_base",
                    "mode": "replace",
                    "value": self.modules["data"].temp_base_values,
                    "default_value": self.modules["data"].cooling[i][j]["temp_base"]
                })
                items.append({
                    "item": "cooling_" + i + "_" + j + "_temp_max",
                    "mode": "replace",
                    "value": self.modules["data"].temp_max_values,
                    "default_value": self.modules["data"].cooling[i][j]["temp_max"]
                })

            for j in ["pump_1", "pump_2"]:
                items.append({
                    "item": "cooling_" + i + "_" + j + "_pwm",
                    "mode": "replace",
                    "value": self.modules["data"].pwm_values,
                    "default_value": self.modules["data"].cooling[i][j]["pwm"]
                })

        self.modules["archgui"].update(items=items)

        # --------------------------------------------------------------------

        self.modules["mpu"].set_var("temperature", {
            "gpio": self.modules["data"].gpio
        })

        # --------------------------------------------------------------------

        items = []

        for i in ["1", "2", "3"]:
            items.append({
                "item": "sensor_" + i + "_target",
                "mode": "replace",
                "value": self.modules["data"].gpio["sensor_" + i]
            })
            items.append({
                "item": "sensor_" + i + "_value",
                "mode": "replace",
                "value": ["cpu", "gpu", "case"],
                "default_value": self.modules["data"].gpio["sensors"][i]
            })

        for i in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
            items.append({
                "item": "gpio_tach_" + i,
                "mode": "replace",
                "value": self.modules["data"].tach_values,
                "default_value": self.modules["data"].gpio["pin"]["tach"][i]
            })

        for i in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
            items.append({
                "item": "gpio_pca_" + i,
                "mode": "replace",
                "value": self.modules["data"].pca_values,
                "default_value": self.modules["data"].gpio["pin"]["pca"][i]
            })

        self.modules["archgui"].update(items=items)

    def change_pwm_steps(self, steps):
        """
        :param steps:
        """

        if steps == self.modules["data"].pwm_steps_values[1]:
            pwm_steps_20 = "show"
        else:
            pwm_steps_20 = "hide"

        items = [{
            "item": "tab_theme_pwm_steps_20",
            "mode": pwm_steps_20
        }]

        self.modules["archgui"].update(items=items)

    def change_combo_collection(self, keys, values, target):
        """
        :param keys:
        :param values:
        :param target:
        """

        collection = []
        for key in keys:
            collection.append(self.modules["archgui"].get_item(key))

        missing = values[0]
        for value in values:
            if value not in collection:
                missing = value

        value = self.modules["archgui"].get_item(target)

        i = 0
        for key in keys:
            if target != key:
                if value == collection[i]:
                    self.modules["archgui"].update([
                        {
                            "item": key,
                            "mode": "replace",
                            "default_value": missing
                        }])
            i += 1

    def change_argb_mode(self, target):
        """
        :param target:
        """

        value = self.modules["archgui"].get_item(target)

        target = target.replace("argb_", "")
        target = target.replace("_mode", "")

        keys = [
            "argb_" + target + "_color_1",
            "argb_" + target + "_color_2",
            "argb_" + target + "_color_3",
            "argb_" + target + "_color_1b",
            "argb_" + target + "_color_2b",
            "argb_" + target + "_color_3b",
            "argb_" + target + "_speed",
            "argb_" + target + "_intensity_min"
        ]

        items = []
        if value == "Off":
            for key in keys:
                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": True
                })

        if value == "Fixe":
            for key in keys:

                if key in ["argb_" + target + "_color_1", "argb_" + target + "_color_1b"]:
                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": False
                    })
                else:
                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": True
                    })

        if value == "Pulse":
            for key in keys:

                if key in [
                    "argb_" + target + "_color_2", "argb_" + target + "_color_2b",
                    "argb_" + target + "_color_3", "argb_" + target + "_color_3b"
                ]:

                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": True
                    })

                else:
                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": False
                    })

        if value == "Pulse Two Colors":
            for key in keys:
                if key in ["argb_" + target + "_color_3", "argb_" + target + "_color_3b"]:

                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": True
                    })

                else:
                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": False
                    })

        if value == "Pulse Three Colors":
            for key in keys:
                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": False
                })

        if value == "Switch Two Colors":
            for key in keys:
                if key in [
                    "argb_" + target + "_color_3", "argb_" + target + "_color_3b",
                    "argb_" + target + "_intensity_min"
                ]:

                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": True
                    })

                else:
                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": False
                    })

        if value == "Switch Three Colors":
            for key in keys:
                if key in "argb_" + target + "_intensity_min":

                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": True
                    })

                else:
                    items.append({
                        "item": key,
                        "mode": "disabled",
                        "value": False
                    })

        self.modules["archgui"].update(items)

    def generate(self):
        """
        generate()
        """

        configuration_uniqid = self.modules["archgui"].open(
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

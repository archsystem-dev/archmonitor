"""
Class Events
"""

import os
import shutil
import time
import json


def cp_file(script_dir, theme_origin, theme_final, file_path):
    """
    :param script_dir:
    :param theme_origin:
    :param theme_final:
    :param file_path:
    :return:
    """

    if not os.path.isdir(script_dir + "/themes/" + theme_final):
        os.mkdir(script_dir + "/themes/" + theme_final)

    filename, ext = os.path.splitext(os.path.basename(file_path))
    filename = filename + ext

    if theme_origin != theme_final:
        if "/" in file_path:
            shutil.copyfile(
                file_path,
                script_dir + "/themes/" + theme_final + "/" + filename)
        else:
            shutil.copyfile(
                script_dir + "/themes/" + theme_origin + "/" + filename,
                script_dir + "/themes/" + theme_final + "/" + filename)
    else:
        if "/" in file_path:
            shutil.copyfile(
                file_path,
                script_dir + "/themes/" + theme_final + "/" + filename)

    return filename


class Events:
    """
    Class Events
    """

    def __init__(self):

        self.windows = None
        self.window = None
        self.model = None

        # -------------------------------

        self.figure = None

        # -------------------------------

    def generate_preview(self, modules, theme_select):
        """
        :param modules:
        :param theme_select:
        """

        theme = {
                "name": theme_select,
                "global": {},
                "images": {},
                "argb": {},
                "mode": {},
                "pwm": {},
                "rpm": {},
                "temp": {},
            }

        for i in modules["configuration"].current_theme["global"]:
            theme["global"][i] = self.model.get_item("theme_" + i)

        for i in modules["configuration"].current_theme["images"]:
            theme["images"][i] = self.model.get_item("theme_" + i)

        # Position

        for i in modules["configuration"].current_theme["argb"]:
            theme["argb"][i] = {}
            for j in ["x", "y"]:
                theme["argb"][i][j] = int(self.model.get_item("theme_argb_" + i + "_" + j))

        for i in modules["configuration"].current_theme["mode"]:
            theme["mode"][i] = {}
            for j in ["x", "y"]:
                theme["mode"][i][j] = int(self.model.get_item("theme_mode_" + i + "_" + j))

        for i in modules["configuration"].current_theme["pwm"]:
            theme["pwm"][i] = {}
            for j in ["x", "y"]:
                theme["pwm"][i][j] = int(self.model.get_item("theme_pwm_" + i + "_" + j))

        for i in modules["configuration"].current_theme["rpm"]:
            theme["rpm"][i] = {}
            for j in ["x", "y", "s"]:
                theme["rpm"][i][j] = int(self.model.get_item("theme_rpm_" + i + "_" + j))

            theme["rpm"][i]["w"] = 60
            theme["rpm"][i]["h"] = 20

            theme["rpm"][i]["f"] = self.model.get_item("theme_rpm_" + i + "_f")
            theme["rpm"][i]["bgc"] = self.model.get_item("theme_rpm_" + i + "_bgc")
            theme["rpm"][i]["c"] = self.model.get_item("theme_rpm_" + i + "_c")

        for i in modules["configuration"].current_theme["temp"]:
            theme["temp"][i] = {}
            for j in ["x", "y", "s"]:
                theme["temp"][i][j] = int(self.model.get_item("theme_temp_" + i + "_" + j))

            theme["temp"][i]["f"] = self.model.get_item("theme_temp_" + i + "_f")
            theme["temp"][i]["w"] = 40
            theme["temp"][i]["h"] = 20
            theme["temp"][i]["bgc"] = self.model.get_item("theme_temp_" + i + "_bgc")
            theme["temp"][i]["c"] = self.model.get_item("theme_temp_" + i + "_c")

        cooling = {}

        for i in ["silent", "performance"]:
            cooling[i] = {}
            for j in ["cpu", "gpu", "case", "pump_1", "pump_2"]:
                cooling[i][j] = {}

                if j in ["cpu", "gpu", "case"]:
                    for k in ["pwm_min", "pwm_max", "temp_base", "temp_max"]:
                        cooling[i][j][k] = self.model.get_item("cooling_" + i + "_" + j + "_" + k)

                if j in ["pump_1", "pump_2"]:
                    cooling[i][j]["pwm"] = self.model.get_item("cooling_" + i + "_" + j + "_pwm")

        modules["configuration"].preview(theme, cooling)

    def events(self, event, modules, values):
        """
        :param event:
        :param modules:
        :param values:
        """

        if event == "theme_pwm_steps":
            value = self.model.get_item("theme_pwm_steps")
            modules["configuration"].change_pwm_steps(value)

        # ------------------------------------------------------------------------

        if event in modules["data"].sensors_keys:
            modules["configuration"].change_combo_collection(
                modules["data"].sensors_keys,
                modules["data"].sensors_values,
                event
            )

        # ------------------------------------------------------------------------

        if event in modules["data"].tach_keys:
            modules["configuration"].change_combo_collection(
                modules["data"].tach_keys,
                modules["data"].tach_values,
                event
            )

        # ------------------------------------------------------------------------

        if event in modules["data"].pca_keys:
            modules["configuration"].change_combo_collection(
                modules["data"].pca_keys,
                modules["data"].pca_values,
                event
            )

        # ------------------------------------------------------------------------

        if event in modules["data"].argb_keys:
            modules["configuration"].change_argb_mode(event)

        # ------------------------------------------------------------------------

        if event == "theme_load":

            theme_name = self.model.get_item("theme_select")

            theme = modules["data"].themes[theme_name]
            cooling = modules["data"].cooling

            modules["configuration"].load_theme(theme_name)
            modules["configuration"].preview(
                    theme,
                    cooling
                )

            time.sleep(1)

            themes = list(modules["data"].themes.keys())
            themes.remove(theme_name)

            new_themes = [theme_name]
            new_themes.extend(themes)

            modules["archgui"].update(items=[{
                "item": "theme_select",
                "mode": "replace",
                "value": new_themes,
                "default_value": theme_name
            }])

        # ------------------------------------------------------------------------

        if event == "generate_preview":
            self.generate_preview(
                modules,
                self.model.get_item("theme_select"))

        # ------------------------------------------------------------------------

        if event == "generate_save":

            modules["data"].default = {
                "theme": self.model.get_item("parameters_theme"),
                "mode": self.model.get_item("parameters_mode"),
                "argb": self.model.get_item("parameters_argb")
            }

            # -----------------------------------------------------------------------------

            modules["data"].argb = {
                "number": self.model.get_item("argb_number_led")
            }

            for i in ["a", "b", "c", "d", "e", "f", "standby"]:
                modules["data"].argb[i] = {}
                for j in ["mode", "color_1", "color_2", "color_3", "intensity_min", "speed"]:
                    value = self.model.get_item("argb_" + i + "_" + j)
                    if j in ["intensity_min", "speed"]:
                        value = int(value)
                    modules["data"].argb[i][j] = value

            # -----------------------------------------------------------------------------

            modules["data"].cooling = {
                "soc": {
                    "pwm_min": 40,
                    "pwm_max": 100,
                    "temp_base": 20,
                    "temp_max": 40
                }
            }

            for i in ["silent", "performance"]:
                modules["data"].cooling[i] = {}

                for j in ["cpu", "gpu", "case", "pump_1", "pump_2"]:
                    modules["data"].cooling[i][j] = {}

                    if j in ["cpu", "gpu", "case"]:
                        for k in ["pwm_min", "pwm_max", "temp_base", "temp_max"]:
                            modules["data"].cooling[i][j][k] = int(self.model.get_item("cooling_" + i + "_" + j + "_" + k))

                    if j in ["pump_1", "pump_2"]:
                        modules["data"].cooling[i][j]["pwm"] = int(self.model.get_item("cooling_" + i + "_" + j + "_pwm"))

            # -----------------------------------------------------------------------------

            modules["data"].gpio["sensors"]["1"] = self.model.get_item("sensor_1_value")
            modules["data"].gpio["sensors"]["2"] = self.model.get_item("sensor_2_value")
            modules["data"].gpio["sensors"]["3"] = self.model.get_item("sensor_3_value")

            for i in ["tach", "pca"]:
                for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
                    modules["data"].gpio["pin"][i][j] = int(self.model.get_item("gpio_" + i + "_" + j))

            # -----------------------------------------------------------------------------
            # -----------------------------------------------------------------------------

            theme_select = self.model.get_item("theme_select")
            theme_name = self.model.get_item("theme_name")

            theme_logo = cp_file(
                modules["data"].script_dir,
                theme_select,
                theme_name,
                self.model.get_item("theme_logo")
            )

            theme_background = cp_file(
                modules["data"].script_dir,
                theme_select,
                theme_name,
                self.model.get_item("theme_background")
            )

            theme_standby_off = cp_file(
                modules["data"].script_dir,
                theme_select,
                theme_name,
                self.model.get_item("theme_standby_off")
            )

            theme_standby_on = cp_file(
                modules["data"].script_dir,
                theme_select,
                theme_name,
                self.model.get_item("theme_standby_on")
            )

            theme = {
                "name": self.model.get_item("theme_name"),
                "global": {
                    "background_color": self.model.get_item("theme_background_color"),
                    "pwm_steps": self.model.get_item("theme_pwm_steps"),
                    "pwm_steps_orientation": self.model.get_item("theme_pwm_steps_orientation")
                },
                "images": {
                    "logo": theme_logo,
                    "background": theme_background,
                    "standby_off": theme_standby_off,
                    "standby_on": theme_standby_on
                },
                "argb": {},
                "mode": {},
                "pwm": {},
                "rpm": {},
                "temp": {}
            }

            for i in ["a", "b", "c", "d", "e", "f"]:
                for j in ["off", "on"]:
                    image = cp_file(
                        modules["data"].script_dir,
                        theme_select,
                        theme_name,
                        self.model.get_item("theme_argb_" + i + "_" + j)
                    )
                    theme["images"]["argb_" + i + "_" + j] = image

            for i in ["silent", "performance"]:
                for j in ["off", "on"]:
                    image = cp_file(
                        modules["data"].script_dir,
                        theme_select,
                        theme_name,
                        self.model.get_item("theme_mode_" + i + "_" + j)
                    )
                    theme["images"]["mode_" + i + "_" + j] = image

            for i in range(1, 21, 1):
                for j in ["off", "on"]:
                    image = cp_file(
                        modules["data"].script_dir,
                        theme_select,
                        theme_name,
                        self.model.get_item("theme_pwm_step_" + str(i) + "_" + j)
                    )
                    theme["images"]["pwm_step_" + str(i) + "_" + j] = image

            # -----------------------------------------------------------------------------

            for i in ["a", "b", "c", "d", "e", "f"]:
                theme["argb"][i] = {}
                for j in ["x", "y"]:
                    theme["argb"][i][j] = int(self.model.get_item("theme_argb_" + i + "_" + j))

            for i in ["silent", "performance"]:
                theme["mode"][i] = {}
                for j in ["x", "y"]:
                    theme["mode"][i][j] = int(self.model.get_item("theme_mode_" + i + "_" + j))

            for i in ["pwm", "rpm"]:
                theme[i] = {}
                for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
                    theme[i][j] = {}
                    if i == "pwm":
                        for k in ["x", "y"]:
                            theme[i][j][k] = int(self.model.get_item("theme_" + i + "_" + j + "_" + k))

                    if i == "rpm":
                        for k in ["x", "y", "w", "h", "f", "bgc", "c", "s"]:
                            value = self.model.get_item("theme_" + i + "_" + j + "_" + k)

                            if k == "f":
                                value = cp_file(
                                    modules["data"].script_dir,
                                    theme_select,
                                    theme_name,
                                    value
                                )
                            elif k in ["x", "y", "w", "h", "s"]:
                                value = int(value)

                            theme[i][j][k] = value

            for i in ["soc", "cpu", "gpu", "case"]:
                theme["temp"][i] = {}
                for j in ["x", "y", "w", "h", "f", "bgc", "c", "s"]:

                    value = self.model.get_item("theme_temp_" + i + "_" + j)

                    if j == "f":
                        value = cp_file(
                            modules["data"].script_dir,
                            theme_select,
                            theme_name,
                            value
                        )
                    elif j in ["x", "y", "w", "h", "s"]:
                        value = int(value)

                    theme["temp"][i][j] = value

            # -----------------------------------------------------------------------------
            # -----------------------------------------------------------------------------

            while True:
                if os.path.isdir(modules["data"].script_dir + "/themes/" + theme_name):
                    with open(modules["data"].script_dir + "/themes/" + theme_name + "/theme.json", "w") as file:
                        file.write(json.dumps(theme, indent=4))
                    break
                time.sleep(1)

            # -----------------------------------------------------------------------------
            # -----------------------------------------------------------------------------

            modules["data"].save_data()

            # -----------------------------------------------------------------------------
            # -----------------------------------------------------------------------------

            modules["data"].load_themes()

            modules["configuration"].load_theme(theme_name)
            modules["configuration"].preview(
                    theme,
                    modules["data"].cooling
                )

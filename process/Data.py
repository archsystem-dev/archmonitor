"""
Data.py
"""
import os
import sys
import json

class Data:
    """
    Class Data
    """

    def __init__(self, script_dir, testing=False, sensors_detection=False):

        self.breaker = None
        self.script_dir = script_dir
        self.testing = testing
        self.modules = {}

        # -------------------------------------------------------------

        self.default = {}
        self.argb = {}
        self.cooling = {}
        self.gpio = {}
        self.themes = {}

        # -------------------------------------------------------------

        self.dir_sensors = "/sys/bus/w1/devices/"

        # -------------------------------------------------------------

        self.base = {
            "argb": {
                "number": 18,
                "a": {
                    "mode": "fixe",
                    "color_1": "#6e6ef0",
                    "color_2": "#6ef06e",
                    "color_3": "#fcba03",
                    "intensity_min": 40,
                    "speed": 10
                },
                "b": {
                    "mode": "pulse",
                    "color_1": "#6e6ef0",
                    "color_2": "#6ef06e",
                    "color_3": "#fcba03",
                    "intensity_min": 40,
                    "speed": 10
                },
                "c": {
                    "mode": "pulse_two_colors",
                    "color_1": "#6e6ef0",
                    "color_2": "#6ef06e",
                    "color_3": "#fcba03",
                    "intensity_min": 40,
                    "speed": 10
                },
                "d": {
                    "mode": "pulse_three_colors",
                    "color_1": "#6e6ef0",
                    "color_2": "#6ef06e",
                    "color_3": "#fcba03",
                    "intensity_min": 40,
                    "speed": 10
                },
                "e": {
                    "mode": "switch_two_colors",
                    "color_1": "#6e6ef0",
                    "color_2": "#6ef06e",
                    "color_3": "#fcba03",
                    "intensity_min": 40,
                    "speed": 10
                },
                "f": {
                    "mode": "switch_three_colors",
                    "color_1": "#6e6ef0",
                    "color_2": "#6ef06e",
                    "color_3": "#fcba03",
                    "intensity_min": 40,
                    "speed": 10
                },
                "standby": {
                    "mode": "off",
                    "color_1": "#6e6ef0",
                    "color_2": "#6ef06e",
                    "color_3": "#fcba03",
                    "intensity_min": 40,
                    "speed": 10
                }
            },
            "cooling": {
                "soc": {
                    "pwm_min": 40,
                    "pwm_max": 100,
                    "temp_base": 20,
                    "temp_max": 40
                },
                "silent": {
                    "cpu": {
                        "pwm_min": 30,
                        "pwm_max": 60,
                        "temp_base": 20,
                        "temp_max": 35
                    },
                    "gpu": {
                        "pwm_min": 30,
                        "pwm_max": 60,
                        "temp_base": 20,
                        "temp_max": 35
                    },
                    "case": {
                        "pwm_min": 30,
                        "pwm_max": 60,
                        "temp_base": 20,
                        "temp_max": 35
                    },
                    "pump_1": {
                        "pwm": 80
                    },
                    "pump_2": {
                        "pwm": 80
                    }
                },
                "performance": {
                    "cpu": {
                        "pwm_min": 60,
                        "pwm_max": 90,
                        "temp_base": 20,
                        "temp_max": 30
                    },
                    "gpu": {
                        "pwm_min": 60,
                        "pwm_max": 90,
                        "temp_base": 20,
                        "temp_max": 30
                    },
                    "case": {
                        "pwm_min": 60,
                        "pwm_max": 90,
                        "temp_base": 20,
                        "temp_max": 30
                    },
                    "pump_1": {
                        "pwm": 100
                    },
                    "pump_2": {
                        "pwm": 100
                    }
                }
            },
            "gpio": {
                "sensor_1": "Sensor N/A",
                "sensor_2": "Sensor N/A",
                "sensor_3": "Sensor N/A",
                "sensors": {
                    "1": "cpu",
                    "2": "gpu",
                    "3": "case"
                },
                "pin": {
                    "power": 26,
                    "start": 24,
                    "pwm_lock": 23,
                    "tach": {
                        "soc": 13,
                        "cpu": 27,
                        "gpu": 22,
                        "case": 5,
                        "pump_1": 6,
                        "pump_2": 17
                    },
                    "pca": {
                        "soc": 0,
                        "cpu": 1,
                        "gpu": 2,
                        "case": 3,
                        "pump_1": 4,
                        "pump_2": 5
                    }
                }
            },
            "default": {
                "theme": "archsystem",
                "mode": "silent",
                "argb": "a"
            }
        }

        self.structure = {
            "argb": {
                "number": int,
                "a": {
                    "mode": str,
                    "color_1": str,
                    "color_2": str,
                    "color_3": str,
                    "intensity_min": int,
                    "speed": int
                },
                "b": {
                    "mode": str,
                    "color_1": str,
                    "color_2": str,
                    "color_3": str,
                    "intensity_min": int,
                    "speed": int
                },
                "c": {
                    "mode": str,
                    "color_1": str,
                    "color_2": str,
                    "color_3": str,
                    "intensity_min": int,
                    "speed": int
                },
                "d": {
                    "mode": str,
                    "color_1": str,
                    "color_2": str,
                    "color_3": str,
                    "intensity_min": int,
                    "speed": int
                },
                "e": {
                    "mode": str,
                    "color_1": str,
                    "color_2": str,
                    "color_3": str,
                    "intensity_min": int,
                    "speed": int
                },
                "f": {
                    "mode": str,
                    "color_1": str,
                    "color_2": str,
                    "color_3": str,
                    "intensity_min": int,
                    "speed": int
                },
                "standby": {
                    "mode": str,
                    "color_1": str,
                    "color_2": str,
                    "color_3": str,
                    "intensity_min": int,
                    "speed": int
                }
            },
            "cooling": {
                "soc": {
                    "pwm_min": int,
                    "pwm_max": int,
                    "temp_base": int,
                    "temp_max": int
                },
                "silent": {
                    "cpu": {
                        "pwm_min": int,
                        "pwm_max": int,
                        "temp_base": int,
                        "temp_max": int
                    },
                    "gpu": {
                        "pwm_min": int,
                        "pwm_max": int,
                        "temp_base": int,
                        "temp_max": int
                    },
                    "case": {
                        "pwm_min": int,
                        "pwm_max": int,
                        "temp_base": int,
                        "temp_max": int
                    },
                    "pump_1": {
                        "pwm": int
                    },
                    "pump_2": {
                        "pwm": int
                    }
                },
                "performance": {
                    "cpu": {
                        "pwm_min": int,
                        "pwm_max": int,
                        "temp_base": int,
                        "temp_max": int
                    },
                    "gpu": {
                        "pwm_min": int,
                        "pwm_max": int,
                        "temp_base": int,
                        "temp_max": int
                    },
                    "case": {
                        "pwm_min": int,
                        "pwm_max": int,
                        "temp_base": int,
                        "temp_max": int
                    },
                    "pump_1": {
                        "pwm": int
                    },
                    "pump_2": {
                        "pwm": int
                    }
                }
            },
            "gpio": {
                "sensor_1": str,
                "sensor_2": str,
                "sensor_3": str,
                "sensors": {
                    "1": str,
                    "2": str,
                    "3": str
                },
                "pin": {
                    "power": int,
                    "start": int,
                    "pwm_lock": int,
                    "tach": {
                        "soc": int,
                        "cpu": int,
                        "gpu": int,
                        "case": int,
                        "pump_1": int,
                        "pump_2": int
                    },
                    "pca": {
                        "soc": int,
                        "cpu": int,
                        "gpu": int,
                        "case": int,
                        "pump_1": int,
                        "pump_2": int
                    }
                }
            },
            "default": {
                "theme": str,
                "mode": str,
                "argb": str
            },
            "theme": {
                "name": str,
                "global": {
                    "background_color": str,
                    "pwm_steps": int,
                    "pwm_steps_orientation": str
                },
                "images": {
                    "logo": str,
                    "background": str,
                    "standby_off": str,
                    "standby_on": str,
                    "argb_a_off": str,
                    "argb_a_on": str,
                    "argb_b_off": str,
                    "argb_b_on": str,
                    "argb_c_off": str,
                    "argb_c_on": str,
                    "argb_d_off": str,
                    "argb_d_on": str,
                    "argb_e_off": str,
                    "argb_e_on": str,
                    "argb_f_off": str,
                    "argb_f_on": str,
                    "mode_silent_off": str,
                    "mode_silent_on": str,
                    "mode_performance_off": str,
                    "mode_performance_on": str,
                    "pwm_step_1_off": str,
                    "pwm_step_1_on": str,
                    "pwm_step_2_off": str,
                    "pwm_step_2_on": str,
                    "pwm_step_3_off": str,
                    "pwm_step_3_on": str,
                    "pwm_step_4_off": str,
                    "pwm_step_4_on": str,
                    "pwm_step_5_off": str,
                    "pwm_step_5_on": str,
                    "pwm_step_6_off": str,
                    "pwm_step_6_on": str,
                    "pwm_step_7_off": str,
                    "pwm_step_7_on": str,
                    "pwm_step_8_off": str,
                    "pwm_step_8_on": str,
                    "pwm_step_9_off": str,
                    "pwm_step_9_on": str,
                    "pwm_step_10_off": str,
                    "pwm_step_10_on": str,
                    "pwm_step_11_off": str,
                    "pwm_step_11_on": str,
                    "pwm_step_12_off": str,
                    "pwm_step_12_on": str,
                    "pwm_step_13_off": str,
                    "pwm_step_13_on": str,
                    "pwm_step_14_off": str,
                    "pwm_step_14_on": str,
                    "pwm_step_15_off": str,
                    "pwm_step_15_on": str,
                    "pwm_step_16_off": str,
                    "pwm_step_16_on": str,
                    "pwm_step_17_off": str,
                    "pwm_step_17_on": str,
                    "pwm_step_18_off": str,
                    "pwm_step_18_on": str,
                    "pwm_step_19_off": str,
                    "pwm_step_19_on": str,
                    "pwm_step_20_off": str,
                    "pwm_step_20_on": str
                },
                "argb": {
                    "a": {
                        "x": int,
                        "y": int
                    },
                    "b": {
                        "x": int,
                        "y": int
                    },
                    "c": {
                        "x": int,
                        "y": int
                    },
                    "d": {
                        "x": int,
                        "y": int
                    },
                    "e": {
                        "x": int,
                        "y": int
                    },
                    "f": {
                        "x": int,
                        "y": int
                    }
                },
                "mode": {
                    "silent": {
                        "x": int,
                        "y": int
                    },
                    "performance": {
                        "x": int,
                        "y": int
                    }
                },
                "pwm": {
                    "soc": {
                        "x": int,
                        "y": int
                    },
                    "cpu": {
                        "x": int,
                        "y": int
                    },
                    "gpu": {
                        "x": int,
                        "y": int
                    },
                    "case": {
                        "x": int,
                        "y": int
                    },
                    "pump_1": {
                        "x": int,
                        "y": int
                    },
                    "pump_2": {
                        "x": int,
                        "y": int
                    }
                },
                "rpm": {
                    "soc": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    },
                    "cpu": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    },
                    "gpu": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    },
                    "case": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    },
                    "pump_1": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    },
                    "pump_2": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    }
                },
                "temp": {
                    "soc": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    },
                    "cpu": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    },
                    "gpu": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    },
                    "case": {
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int,
                        "f": str,
                        "bgc": str,
                        "c": str,
                        "s": int
                    }
                }
            }
        }

        self.sensors_keys = [
            "sensor_1_value",
            "sensor_2_value",
            "sensor_3_value"
        ]

        self.tach_keys = [
            "gpio_tach_soc",
            "gpio_tach_cpu",
            "gpio_tach_gpu",
            "gpio_tach_case",
            "gpio_tach_pump_1",
            "gpio_tach_pump_2"
        ]

        self.pca_keys = [
            "gpio_pca_soc",
            "gpio_pca_cpu",
            "gpio_pca_gpu",
            "gpio_pca_case",
            "gpio_pca_pump_1",
            "gpio_pca_pump_2"
        ]

        self.argb_keys = [
            "argb_a_mode",
            "argb_b_mode",
            "argb_c_mode",
            "argb_d_mode",
            "argb_e_mode",
            "argb_f_mode",
            "argb_standby_mode"
        ]

        # -------------------------------------------------------------

        self.pwm_steps_values = [10, 20]
        self.pwm_steps_orientation_value = ["left_to_right", "bottom_to_top"]

        self.argb_mode = ["off", "fixe", "pulse",
                          "pulse_two_colors",
                          "pulse_three_colors",
                          "switch_two_colors",
                          "switch_three_colors"]

        self.argb_app = ["a", "b", "c", "d", "e", "f", "standby"]

        self.number_argb_values = list(range(10, 32, 2))
        self.intensity_min_values = list(range(40, 90, 10))
        self.speed_values = list(range(10, 90, 10))

        self.sensors_values = ["cpu", "gpu", "case"]
        self.pwm_values = list(range(0, 110, 10))
        self.temp_base_values = list(range(15, 40, 5))
        self.temp_max_values = list(range(30, 45, 5))

        self.tach_values = [5, 6, 13, 17, 22, 27]
        self.pca_values = [0, 1, 2, 3, 4, 5]

        # -------------------------------------------------------------

        self.load_files()
        self.load_themes()

        if not testing and not sensors_detection:
            self.check_sensors()

        # -------------------------------------------------------------

    def define_modules(self, modules):
        """
        :param modules:
        """
        self.modules = modules


    def approval(self, structure: str, data):
        """
        :param data:
        :param structure:
        :return:
        """

        return self.check(self.structure[structure], data)

    def check(self, structure, data):
        """
        :param data:
        :param structure:
        :return:
        """

        for key, expected_type in structure.items():

            if key not in data:
                return False

            if isinstance(expected_type, dict):
                if not isinstance(data[key], dict):
                    return False
                if not self.check(expected_type, data[key]):
                    return False
            else:
                if not isinstance(data[key], expected_type):
                    return False

                if key == "pwm_steps" and data[key] not in self.pwm_steps_values:
                    return False

                if key == "pwm_steps_orientation" and data[key] not in self.pwm_steps_orientation_value:
                    return False

        return True

    def load_files(self):
        """
        load_files()
        """

        # Chargement des différentes configurations
        self.default = self.load_config("default")
        self.argb = self.load_config("argb")
        self.cooling = self.load_config("cooling")
        self.gpio = self.load_config("gpio")
        self.save_data()

    def save_data(self):
        """
        save_data()
        """

        with open(self.script_dir + "/config/argb.json", "w") as file:
            file.write(json.dumps(self.argb, indent=4))

        with open(self.script_dir + "/config/cooling.json", "w") as file:
            file.write(json.dumps(self.cooling, indent=4))

        with open(self.script_dir + "/config/default.json", "w") as file:
            file.write(json.dumps(self.default, indent=4))

        with open(self.script_dir + "/config/gpio.json", "w") as file:
            file.write(json.dumps(self.gpio, indent=4))


    def load_config(self, name):
        """
        load_config()
        """

        file_path = self.script_dir + "/config/" + name + ".json"

        if os.path.isfile(file_path):
            with open(file_path, "r") as raw:
                config = json.load(raw)
                if self.approval(name, config):
                    return config

        default_config = self.base[name]
        with open(file_path, "w") as new_file:
            json.dump(default_config, new_file, indent=4)

        return default_config

    def load_themes(self):
        """
        load_themes()
        """

        dir_themes = self.script_dir + "/themes/"
        themes_path = [f.path for f in os.scandir(dir_themes) if f.is_dir()]

        if not len(themes_path) > 0:
            self.themes_error(0)

        for theme_path in themes_path:
            theme_dir = theme_path.replace(dir_themes, "")
            theme_json_path = os.path.join(theme_path, "theme.json")

            if not os.path.isfile(theme_json_path):
                continue

            with open(theme_json_path, "r") as theme_config:
                theme = json.load(theme_config)

            if self.approval("theme", theme):

                image_missing = 0
                for image in theme["images"]:
                    theme_image_path = os.path.join(theme_path, theme["images"][image])

                    if not os.path.isfile(theme_image_path):
                        image_missing += 1
                        break

                if image_missing == 0:
                    with open(theme_path + "/theme.json", "r") as theme_config:
                        self.themes[theme_dir] = json.load(theme_config)

        if not len(self.themes) > 0:
            self.themes_error(1)

        if self.default["theme"] not in self.themes:
            self.themes_error(2)


    def themes_error(self, err):
        """
        themes_error()
        """

        if err == 0:
            print("Chargement impossible, aucun theme détecté.")

        if err == 1:
            print("Chargement impossible, aucun theme valide détecté.")

        if err == 2:
            print("Chargement impossible, le theme par default n'est pas valide.")

        self.stop()
        sys.exit(0)
        
    def check_sensors(self):
        """
        check_sensors()
        """
        if os.path.isdir(self.dir_sensors):

            for i in range(1, 4, 1):
                if not os.path.isdir(self.dir_sensors + self.gpio["sensor_" + str(i)]):
                    print(f"La sonde {i} est manquante : " + self.gpio["sensor_" + str(i)])
                    print("Relance le script 'sensors.py'")
                    sys.exit(0)

        else:
            print(f"Le dossier: {self.dir_sensors} est introuvable.")
            self.stop()
            sys.exit(0)

    def stop(self):
        """
        stop()
        """
        self.breaker = True

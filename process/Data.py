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

        self.bases = self.load_data("bases")
        self.structures = self.load_data("structures")
        self.keys = self.load_data("keys")
        self.values = self.load_data("values")

        # -------------------------------------------------------------

        self.load_files()
        self.load_themes()

        if not testing and not sensors_detection:
            self.check_sensors()

        # -------------------------------------------------------------

    def define_modules(self, modules):
        self.modules = modules

    def approval(self, structure: str, data):
        return self.check(self.structures[structure], data)

    def check(self, structure, data):

        for key, expected_type in structure.items():

            if key not in data:
                return False

            if isinstance(expected_type, dict):
                if not isinstance(data[key], dict):
                    return False

                if not self.check(expected_type, data[key]):
                    return False

            else:

                if expected_type == "string":
                    expected_type = str

                if expected_type == "integer":
                    expected_type = int

                if not isinstance(data[key], expected_type):
                    return False

        return True

    def load_files(self):
        self.default = self.load_config("default")
        self.argb = self.load_config("argb")
        self.cooling = self.load_config("cooling")
        self.gpio = self.load_config("gpio")
        self.save_data()

    def save_data(self):

        with open(self.script_dir + "/config/argb.json", "w") as file:
            file.write(json.dumps(self.argb, indent=4))

        with open(self.script_dir + "/config/cooling.json", "w") as file:
            file.write(json.dumps(self.cooling, indent=4))

        with open(self.script_dir + "/config/default.json", "w") as file:
            file.write(json.dumps(self.default, indent=4))

        with open(self.script_dir + "/config/gpio.json", "w") as file:
            file.write(json.dumps(self.gpio, indent=4))

    def load_data(self, name):

        file_path = self.script_dir + "/process/data/" + name + ".json"

        with open(file_path, "r") as raw:
            data = json.load(raw)
            return data

    def load_config(self, name):

        file_path = self.script_dir + "/config/" + name + ".json"

        if os.path.isfile(file_path):
            with open(file_path, "r") as raw:
                config = json.load(raw)
                if self.approval(name, config):
                    return config

        default_config = self.bases[name]
        with open(file_path, "w") as new_file:
            new_file.write(json.dumps(default_config, indent=4))

        return default_config

    def load_themes(self):

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

        if err == 0:
            print("Chargement impossible, aucun theme détecté.")

        if err == 1:
            print("Chargement impossible, aucun theme valide détecté.")

        if err == 2:
            print("Chargement impossible, le theme par default n'est pas valide.")

        self.stop()
        sys.exit(0)
        
    def check_sensors(self):

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
        self.breaker = True

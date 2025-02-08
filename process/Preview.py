"""
Preview.py
"""

import os

from PIL import Image, ImageDraw, ImageFont


def rgb_to_hex(rgb):
    """
    :param rgb:
    :return:
    """
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# -------------------------------------------------------------------------
# / Converti une List en Tuple
# -------------------------------------------------------------------------


def list_to_tuple(ll):
    """
    :param ll:
    :return:
    """
    return tuple(list_to_tuple(x) for x in ll) if type(ll) is list else ll


class Preview:
    """
    Class Preview
    """

    def __init__(self, testing=False):

        self.breaker = False
        self.testing = testing
        self.modules = {}

        # -------------------------------------------------------------

        self.window = None

        self.graph_theme_startup = "graph_theme_startup"
        self.graph_theme_in_use_off = "graph_theme_in_use_off"
        self.graph_theme_in_use_on = "graph_theme_in_use_on"
        self.graph_theme_standby_off = "graph_theme_in_standby_off"
        self.graph_theme_standby_on = "graph_theme_in_standby_on"

        self.graph_cooling_silent = "graph_cooling_silent"
        self.graph_cooling_performance = "graph_cooling_performance"

        # -------------------------------------------------------------

        self.dimension = (800, 480)

        # -------------------------------------------------------------

        self.theme = None
        self.theme_images = {}
        self.theme_figures = {
            "startup": {},
            "in_use_off": {},
            "in_use_on": {},
            "standby_off": {},
            "standby_on": {},
            "cooling_silent": {},
            "cooling_performance": {}
        }

        self.cooling = None
        self.cooling_images = {
            "static": {},
            "dynamic": {}
        }
        self.cooling_figures = {
            "static": {},
            "dynamic": {
                "silent": {},
                "performance": {}
            }
        }

    def define_modules(self, modules):
        """
        :param modules:
        """
        self.modules = modules

    def load_theme(self, theme):
        """
        load_theme()
        """
        self.theme = theme
        self.load_theme_images()

    def load_theme_images(self):
        """
        load_theme_images()
        """

        self.theme_images = {}

        for image in self.theme["images"]:

            path = ""
            if "/" not in self.theme["images"][image]:
                path = self.modules["data"].script_dir + "/themes/" + self.theme["name"] + "/"

            if os.path.isfile(path + self.theme["images"][image]):
                self.theme_images[image] = Image.open(path + self.theme["images"][image])

        text_prev = {
            "rpm": "2500",
            "temp": "30"
        }

        for text in ["rpm", "temp"]:
            for target in self.theme[text]:

                path = ""
                if "/" not in self.theme[text][target]["f"]:
                    path = self.modules["data"].script_dir + "/themes/" + self.theme["name"] + "/"

                font = ImageFont.truetype(
                    path + self.theme[text][target]["f"],
                    self.theme[text][target]["s"]
                )

                bgc_color = self.theme[text][target]["bgc"]
                if isinstance(self.theme[text][target]["bgc"],  list):
                    bgc_color = rgb_to_hex(self.theme[text][target]["bgc"])

                c_color = self.theme[text][target]["c"]
                if isinstance(self.theme[text][target]["c"],  list):
                    c_color = rgb_to_hex(self.theme[text][target]["c"])

                canvas = Image.new(
                    "RGBA",
                    (self.theme[text][target]["w"], self.theme[text][target]["h"]),
                    color=list_to_tuple(bgc_color))

                image = ImageDraw.Draw(canvas)
                image.text(
                    (0, 0),
                    text_prev[text],
                    font=font,
                    text_color=c_color
                )

                self.theme_images[text + "_" + target] = canvas

    def print_preview_startup(self):
        """
        print_preview_startup()
        """
        for figure in self.theme_figures["startup"]:
            self.modules["archgui"].graph_delete_figure(
                graph=self.graph_theme_startup,
                figure=self.theme_figures["startup"][figure])

        if "logo" in self.theme_images:
            self.theme_figures["startup"]["logo"] = self.modules["archgui"].graph_draw_image(
                graph=self.graph_theme_startup,
                location=(10, 10),
                image=self.theme_images["logo"]
            )

    def print_preview_in_use_off(self):
        """
        print_preview_in_use_off()
        """
        for figure in self.theme_figures["in_use_off"]:
            self.modules["archgui"].graph_delete_figure(
                graph=self.graph_theme_in_use_off,
                figure=self.theme_figures["in_use_off"][figure])

        if "background" in self.theme_images:

            fn = "background"
            self.theme_figures["in_use_off"][fn] = self.modules["archgui"].graph_draw_image(
                graph=self.graph_theme_in_use_off,
                location=(10, 10),
                image=self.theme_images["background"])

        for i in ["a", "b", "c", "d", "e", "f"]:

            if "argb_" + i + "_off" in self.theme_images:

                fn = "argb_" + i
                self.theme_figures["in_use_off"][fn] = self.modules["archgui"].graph_draw_image(
                    graph=self.graph_theme_in_use_off,
                    location=(
                        self.theme["argb"][i]["x"],
                        self.theme["argb"][i]["y"]
                    ),
                    image=self.theme_images["argb_" + i + "_off"])

        for i in ["silent", "performance"]:

            if "mode_" + i + "_off" in self.theme_images:

                fn = "mode_" + i
                self.theme_figures["in_use_off"][fn] = self.modules["archgui"].graph_draw_image(
                    graph=self.graph_theme_in_use_off,
                    location=(
                        self.theme["mode"][i]["x"],
                        self.theme["mode"][i]["y"]
                    ),
                    image=self.theme_images["mode_" + i + "_off"])

        for i in range(self.theme["global"]["pwm_steps"]):
            for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:

                x = self.theme["pwm"][j]["x"]
                for k in range(i):
                    if "pwm_step_" + str(k + 1) + "_off" in self.theme_images:
                        x += self.theme_images["pwm_step_" + str(k + 1) + "_off"].width

                if "pwm_step_" + str(i + 1) + "_off" in self.theme_images:

                    fn = "pwm_" + j + "_" + str(i + 1)
                    self.theme_figures["in_use_off"][fn] = self.modules["archgui"].graph_draw_image(
                        graph=self.graph_theme_in_use_off,
                        location=(x, self.theme["pwm"][j]["y"]),
                        image=self.theme_images["pwm_step_" + str(i + 1) + "_off"])

        for i in ["rpm", "temp"]:
            for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
                if i + "_" + j in self.theme_images:

                    fn = i + "_" + j + "_" + i
                    self.theme_figures["in_use_off"][fn] = self.modules["archgui"].graph_draw_image(
                        graph=self.graph_theme_in_use_off,
                        location=(
                            self.theme[i][j]["x"],
                            self.theme[i][j]["y"]
                        ),
                        image=self.theme_images[i + "_" + j])

    def print_preview_in_use_on(self):
        """
        print_preview_in_use_on()
        """
        for figure in self.theme_figures["in_use_on"]:
            self.modules["archgui"].graph_delete_figure(
                graph=self.graph_theme_in_use_on,
                figure=self.theme_figures["in_use_on"][figure])

        if "background" in self.theme_images:

            fn = "background"
            self.theme_figures["in_use_on"][fn] = self.modules["archgui"].graph_draw_image(
                graph=self.graph_theme_in_use_on,
                location=(10, 10),
                image=self.theme_images["background"])

        for i in ["a", "b", "c", "d", "e", "f"]:

            if "argb_" + i + "_on" in self.theme_images:

                fn = "argb_" + i
                self.theme_figures["in_use_on"][fn] = self.modules["archgui"].graph_draw_image(
                    graph=self.graph_theme_in_use_on,
                    location=(
                        self.theme["argb"][i]["x"],
                        self.theme["argb"][i]["y"]
                    ),
                    image=self.theme_images["argb_" + i + "_on"])

        for i in ["silent", "performance"]:

            if "mode_" + i + "_on" in self.theme_images:

                fn = "mode_" + i
                self.theme_figures["in_use_on"][fn] = self.modules["archgui"].graph_draw_image(
                    graph=self.graph_theme_in_use_on,
                    location=(
                        self.theme["mode"][i]["x"],
                        self.theme["mode"][i]["y"]
                    ),
                    image=self.theme_images["mode_" + i + "_on"])

        for i in range(self.theme["global"]["pwm_steps"]):
            for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:

                x = self.theme["pwm"][j]["x"]
                for k in range(i):
                    if "pwm_step_" + str(k + 1) + "_on" in self.theme_images:
                        x += self.theme_images["pwm_step_" + str(k + 1) + "_on"].width

                if "pwm_step_" + str(i + 1) + "_on" in self.theme_images:
                    fn = "pwm_" + j + "_" + str(i + 1)

                    self.theme_figures["in_use_on"][fn] = self.modules["archgui"].graph_draw_image(
                        graph=self.graph_theme_in_use_on,
                        location=(x, self.theme["pwm"][j]["y"]),
                        image=self.theme_images["pwm_step_" + str(i + 1) + "_on"])

        for i in ["rpm", "temp"]:
            for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:

                if i + "_" + j in self.theme_images:

                    fn = i + "_" + j
                    self.theme_figures["in_use_on"][fn] = self.modules["archgui"].graph_draw_image(
                        graph=self.graph_theme_in_use_on,
                        location=(
                            self.theme[i][j]["x"],
                            self.theme[i][j]["y"]
                        ),
                        image=self.theme_images[i + "_" + j])

    def print_preview_standby_off(self):
        """
        print_preview_standby_off()
        """
        for figure in self.theme_figures["standby_off"]:
            self.modules["archgui"].graph_delete_figure(
                graph=self.graph_theme_standby_off,
                figure=self.theme_figures["standby_off"][figure])

        if "standby_off" in self.theme_images:
            self.theme_figures["standby_off"]["button"] = self.modules["archgui"].graph_draw_image(
                graph=self.graph_theme_standby_off,
                location=(10, 10),
                image=self.theme_images["standby_off"]
            )

    def print_preview_standby_on(self):
        """
        print_preview_standby_on()
        """
        for figure in self.theme_figures["standby_on"]:
            self.modules["archgui"].graph_delete_figure(
                graph=self.graph_theme_standby_on,
                figure=self.theme_figures["standby_on"][figure])

        if "standby_on" in self.theme_images:
            self.theme_figures["standby_on"]["button"] = self.modules["archgui"].graph_draw_image(
                graph=self.graph_theme_standby_on,
                location=(10, 10),
                image=self.theme_images["standby_on"]
            )

    def load_cooling(self, cooling):
        """
        load_cooling()
        """
        self.cooling = cooling
        self.load_cooling_images_static()

    def load_cooling_images_static(self):
        """
        load_cooling_images_static()
        """

        font = ImageFont.truetype(
            self.modules["data"].script_dir + "/resource/RobotoMono-Regular.ttf",
            20
        )

        for i in range(0, 105, 5):
            canvas = Image.new(
                "RGBA",
                (40, 28),
                color=list_to_tuple((00, 00, 00, 255)))

            if i < 10:
                x = 22
            elif i < 100:
                x = 11
            else:
                x = 0

            image = ImageDraw.Draw(canvas)
            image.text(
                (x, 0),
                str(i),
                font=font,
                text_color=(255, 255, 255, 255),
            )

            self.cooling_images["static"][str(i)] = canvas

        # -------------------------------------------------------

        canvas = Image.new(
            "RGBA",
            (60, 28),
            color=list_to_tuple((00, 00, 00, 255)))

        image = ImageDraw.Draw(canvas)
        image.text(
            (0, 0),
            "CPU",
            font=font,
            text_color=(255, 255, 255, 255),
        )

        self.cooling_images["static"]["cpu"] = canvas

        # -------------------------------------------------------

        canvas = Image.new(
            "RGBA",
            (60, 28),
            color=list_to_tuple((00, 00, 00, 255)))

        image = ImageDraw.Draw(canvas)
        image.text(
            (0, 0),
            "GPU",
            font=font,
            text_color=(255, 255, 255, 255),
        )

        self.cooling_images["static"]["gpu"] = canvas

        # -------------------------------------------------------

        canvas = Image.new(
            "RGBA",
            (60, 28),
            color=list_to_tuple((00, 00, 00, 255)))

        image = ImageDraw.Draw(canvas)
        image.text(
            (0, 0),
            "Case",
            font=font,
            text_color=(255, 255, 255, 255),
        )

        self.cooling_images["static"]["case"] = canvas

        # -------------------------------------------------------

        canvas = Image.new(
            "RGBA",
            (80, 28),
            color=list_to_tuple((00, 00, 00, 255)))

        image = ImageDraw.Draw(canvas)
        image.text(
            (0, 0),
            "Pump 1",
            font=font,
            text_color=(255, 255, 255, 255),
        )

        self.cooling_images["static"]["pump_1"] = canvas

        # -------------------------------------------------------

        canvas = Image.new(
            "RGBA",
            (80, 28),
            color=list_to_tuple((00, 00, 00, 255)))

        image = ImageDraw.Draw(canvas)
        image.text(
            (0, 0),
            "Pump 2",
            font=font,
            text_color=(255, 255, 255, 255),
        )

        self.cooling_images["static"]["pump_2"] = canvas

        # -------------------------------------------------------

        x = 80
        j = 0
        y = 340

        for i in range(0, 110, 10):

            self.modules["archgui"].graph_draw_image(
                graph=self.graph_cooling_silent,
                location=(x, y - (j * 28)),
                image=self.cooling_images["static"][str(i)])

            self.modules["archgui"].graph_draw_image(
                graph=self.graph_cooling_performance,
                location=(x, y - (j * 28)),
                image=self.cooling_images["static"][str(i)])

            j += 1

        x += 40
        j = 0

        for i in range(5, 65, 5):

            self.modules["archgui"].graph_draw_image(
                graph=self.graph_cooling_silent,
                location=(x + (j * 50), y),
                image=self.cooling_images["static"][str(i)])

            self.modules["archgui"].graph_draw_image(
                graph=self.graph_cooling_performance,
                location=(x + (j * 50), y),
                image=self.cooling_images["static"][str(i)])

            j += 1

        # -------------------------------------------------------------------

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_silent,
            point_from=(x, y),
            point_to=(720, y),
            color="white",
            width=2
        )

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_performance,
            point_from=(x, y),
            point_to=(720, y),
            color="white",
            width=2
        )

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_silent,
            point_from=(x, y),
            point_to=(x, 60),
            color="white",
            width=2
        )

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_performance,
            point_from=(x, y),
            point_to=(x, 60),
            color="white",
            width=2
        )

        # -------------------------------------------------------------------

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_silent,
            point_from=(x + 20, 395),
            point_to=(x + 60, 395),
            color="red",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_silent,
            location=(x + 60 + 10, 380),
            image=self.cooling_images["static"]["cpu"])

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_performance,
            point_from=(x + 20, 395),
            point_to=(x + 60, 395),
            color="red",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_performance,
            location=(x + 60 + 10, 380),
            image=self.cooling_images["static"]["cpu"])

        # -------------------------------------------------------------------

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_silent,
            point_from=(x + 20, 425),
            point_to=(x + 60, 425),
            color="yellow",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_silent,
            location=(x + 60 + 10, 410),
            image=self.cooling_images["static"]["gpu"])

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_performance,
            point_from=(x + 20, 425),
            point_to=(x + 60, 425),
            color="yellow",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_performance,
            location=(x + 60 + 10, 410),
            image=self.cooling_images["static"]["gpu"])

        # -------------------------------------------------------------------

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_silent,
            point_from=(x + 220, 395),
            point_to=(x + 220 + 40, 395),
            color="green",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_silent,
            location=(x + 220 + 40 + 10, 380),
            image=self.cooling_images["static"]["case"])

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_performance,
            point_from=(x + 220, 395),
            point_to=(x + 220 + 40, 395),
            color="green",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_performance,
            location=(x + 220 + 40 + 10, 380),
            image=self.cooling_images["static"]["case"])

        # -------------------------------------------------------------------

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_silent,
            point_from=(x + 420, 395),
            point_to=(x + 420 + 40, 395),
            color="violet",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_silent,
            location=(x + 420 + 40 + 10, 380),
            image=self.cooling_images["static"]["pump_1"])

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_performance,
            point_from=(x + 420, 395),
            point_to=(x + 420 + 40, 395),
            color="violet",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_performance,
            location=(x + 420 + 40 + 10, 380),
            image=self.cooling_images["static"]["pump_1"])

        # -------------------------------------------------------------------

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_silent,
            point_from=(x + 420, 425),
            point_to=(x + 420 + 40, 425),
            color="cyan",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_silent,
            location=(x + 420 + 40 + 10, 410),
            image=self.cooling_images["static"]["pump_2"])

        self.modules["archgui"].graph_draw_line(
            graph=self.graph_cooling_performance,
            point_from=(x + 420, 425),
            point_to=(x + 420 + 40, 425),
            color="cyan",
            width=12
        )

        self.modules["archgui"].graph_draw_image(
            graph=self.graph_cooling_performance,
            location=(x + 420 + 40 + 10, 410),
            image=self.cooling_images["static"]["pump_2"])

    def print_preview_cooling(self):
        """
        load_cooling_images_dynamic()
        """

        for figure in self.cooling_figures["dynamic"]["silent"]:
            self.modules["archgui"].graph_delete_figure(
                graph=self.graph_cooling_silent,
                figure=self.cooling_figures["dynamic"]["silent"][figure])

        for figure in self.cooling_figures["dynamic"]["performance"]:
            self.modules["archgui"].graph_delete_figure(
                graph=self.graph_cooling_performance,
                figure=self.cooling_figures["dynamic"]["performance"][figure])

        x = 120 + 2
        y = 340

        x_df = 50
        y_df = 28

        x_aj = 30

        y_aj = {
            "cpu": 11,
            "gpu": 14,
            "case": 17,
            "pump_1": 12,
            "pump_2": 15
        }

        color = {
            "cpu": "red",
            "gpu": "yellow",
            "case": "green",
            "pump_1": "violet",
            "pump_2": "cyan"
        }

        for i in ["silent", "performance"]:
            for j in ["cpu", "gpu", "case", "pump_1", "pump_2"]:
                if j in ["pump_1", "pump_2"]:

                    point_from_x = x
                    point_from_y = y - ((self.cooling[i][j]["pwm"] / 10) * y_df) + y_aj[j]

                    point_to_x = x + (12 * x_df) - x_aj
                    point_to_y = y - ((self.cooling[i][j]["pwm"] / 10) * y_df) + y_aj[j]

                    fn = i + "_" + j
                    if i == "silent":
                        self.cooling_figures["dynamic"][i][fn] = self.modules["archgui"].graph_draw_line(
                            graph=self.graph_cooling_silent,
                            point_from=(point_from_x, point_from_y),
                            point_to=(point_to_x, point_to_y),
                            color=color[j],
                            width=2
                        )
                    if i == "performance":
                        self.cooling_figures["dynamic"][i][fn] = self.modules["archgui"].graph_draw_line(
                            graph=self.graph_cooling_performance,
                            point_from=(point_from_x, point_from_y),
                            point_to=(point_to_x, point_to_y),
                            color=color[j],
                            width=2
                        )

                else:

                    point_from_x = x
                    point_from_y = y - ((self.cooling[i][j]["pwm_min"] / 10) * y_df) + y_aj[j]

                    point_to_x = x + ((self.cooling[i][j]["temp_base"] / 5) * x_df) - x_aj
                    point_to_y = y - ((self.cooling[i][j]["pwm_min"] / 10) * y_df) + y_aj[j]

                    fn = i + "_" + j + "_1"
                    if i == "silent":
                        self.cooling_figures["dynamic"][i][fn] = self.modules["archgui"].graph_draw_line(
                            graph=self.graph_cooling_silent,
                            point_from=(point_from_x, point_from_y),
                            point_to=(point_to_x, point_to_y),
                            color=color[j],
                            width=2
                        )
                    if i == "performance":
                        self.cooling_figures["dynamic"][i][fn] = self.modules["archgui"].graph_draw_line(
                            graph=self.graph_cooling_performance,
                            point_from=(point_from_x, point_from_y),
                            point_to=(point_to_x, point_to_y),
                            color=color[j],
                            width=2
                        )

                    point_from_x = point_to_x
                    point_from_y = point_to_y

                    point_to_x = x + ((self.cooling[i][j]["temp_max"] / 5) * x_df) - x_aj
                    point_to_y = y - ((self.cooling[i][j]["pwm_max"] / 10) * y_df) + y_aj[j]

                    fn = i + "_" + j + "_2"
                    if i == "silent":
                        self.cooling_figures["dynamic"][i][fn] = self.modules["archgui"].graph_draw_line(
                            graph=self.graph_cooling_silent,
                            point_from=(point_from_x, point_from_y),
                            point_to=(point_to_x, point_to_y),
                            color=color[j],
                            width=2
                        )
                    if i == "performance":
                        self.cooling_figures["dynamic"][i][fn] = self.modules["archgui"].graph_draw_line(
                            graph=self.graph_cooling_performance,
                            point_from=(point_from_x, point_from_y),
                            point_to=(point_to_x, point_to_y),
                            color=color[j],
                            width=2
                        )

                    point_from_x = point_to_x
                    point_from_y = point_to_y

                    point_to_x = x + (12 * x_df) - x_aj
                    point_to_y = point_to_y

                    fn = i + "_" + j + "_3"
                    if i == "silent":
                        self.cooling_figures["dynamic"][i][fn] = self.modules["archgui"].graph_draw_line(
                            graph=self.graph_cooling_silent,
                            point_from=(point_from_x, point_from_y),
                            point_to=(point_to_x, point_to_y),
                            color=color[j],
                            width=2
                        )
                    if i == "performance":
                        self.cooling_figures["dynamic"][i][fn] = self.modules["archgui"].graph_draw_line(
                            graph=self.graph_cooling_performance,
                            point_from=(point_from_x, point_from_y),
                            point_to=(point_to_x, point_to_y),
                            color=color[j],
                            width=2
                        )

    # ----------------------------------------------------------------------------------------
    # stop
    # ----------------------------------------------------------------------------------------

    def stop(self):
        """
        stop()
        """

        self.breaker = True

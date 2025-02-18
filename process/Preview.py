"""
Preview.py
"""


from process.preview.load_cooling_images_static import load_cooling_images_static
from process.preview.load_theme_images import load_theme_images

from process.preview.print_preview_cooling import print_preview_cooling
from process.preview.print_preview_in_use_off import print_preview_in_use_off
from process.preview.print_preview_in_use_on import print_preview_in_use_on
from process.preview.print_preview_standby_off import print_preview_standby_off
from process.preview.print_preview_standby_on import print_preview_standby_on
from process.preview.print_preview_startup import print_preview_startup


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
        self.modules = modules

    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    def list_to_tuple(self, ll):
        return tuple(self.list_to_tuple(x) for x in ll) if type(ll) is list else ll

    def load_theme(self, theme):
        self.theme = theme
        self.load_theme_images()

    def load_theme_images(self):
        load_theme_images(self)

    def print_preview_startup(self):
        print_preview_startup(self)

    def print_preview_in_use_off(self):
        print_preview_in_use_off(self)

    def print_preview_in_use_on(self):
        print_preview_in_use_on(self)

    def print_preview_standby_off(self):
        print_preview_standby_off(self)

    def print_preview_standby_on(self):
        print_preview_standby_on(self)

    def load_cooling(self, cooling):
        self.cooling = cooling
        self.load_cooling_images_static()

    def load_cooling_images_static(self):
        load_cooling_images_static(self)

    def print_preview_cooling(self):
        print_preview_cooling(self)

    # ----------------------------------------------------------------------------------------
    # stop
    # ----------------------------------------------------------------------------------------

    def stop(self):
        """
        stop()
        """

        self.breaker = True

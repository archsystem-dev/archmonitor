"""
Class Events
"""


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

    def events(self, event, modules, values):
        """
        :param event:
        :param modules:
        :param values:
        """
        if event == 'graph_monitor button-1':

            is_break = False
            x = values["graph_monitor"][0]
            y = values["graph_monitor"][1]

            for i in ["a", "b", "c", "d", "e", "f"]:
                ix = modules["display"].theme["argb"][i]["x"]
                iy = modules["display"].theme["argb"][i]["y"]
                iw = modules["display"].images["argb"][i]["on"].width
                ih = modules["display"].images["argb"][i]["on"].height

                if ix < x < int(ix + iw) and iy < y < int(iy + ih):
                    modules["display"].print_active_argb(i)
                    modules["mpu"].set_var("argb", {"argb_selected": i})
                    is_break = True
                    break

            # ----------------------------------------------------

            if not is_break:
                for i in ["silent", "performance"]:
                    ix = modules["display"].theme["mode"][i]["x"]
                    iy = modules["display"].theme["mode"][i]["y"]
                    iw = modules["display"].images["mode"][i]["on"].width
                    ih = modules["display"].images["mode"][i]["on"].height

                    if ix < x < int(ix + iw) and iy < y < int(iy + ih):
                        modules["mpu"].set_var("listener", {"mode": i})
                        modules["display"].print_active_mode(i)
                        break

        if event == 'graph_standby button-1':
            x = values["graph_standby"][0]
            y = values["graph_standby"][1]

            if 250 < x < 250 + 300 and 90 < y < 90 + 300:
                modules["mpu"].set_var("listener", {"start": True})
                modules["display"].print_active_standby()

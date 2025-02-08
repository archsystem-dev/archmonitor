"""
main.py
"""

import os
import sys
import signal


if __name__ == "__main__":

    argv = sys.argv
    testing = False
    verbose = False

    if len(argv) > 1:
        if "-t" in argv:
            testing = True
        if "-v":
            verbose = True

    # -------------------------------------------------------------------------

    script_dir = os.path.dirname(os.path.realpath(__file__))

    from process.Data import Data
    data = Data(script_dir=script_dir, testing=testing)

    # -------------------------------------------------------------------------

    import archgui
    import mpunified

    from process.Temperature import temperature_run
    from process.Listener import listener_run
    from process.Argb import argb_run
    from process.Display import Display

    # -------------------------------------------------------------------------

    mpu = mpunified.mpu

    mpu.load("temperature", temperature_run)
    mpu.load("listener", listener_run)
    mpu.load("argb", argb_run)

    mpu.bind_transfert("temperature", "listener")

    mpu.set_var("temperature", {"testing": testing, "gpio": data.gpio})

    mpu.set_var("listener", {
        "testing": testing,
        "default": data.default,
        "gpio": data.gpio,
        "cooling": data.cooling})

    mpu.set_var("argb", {
        "testing": testing,
        "default": data.default,
        "argb": data.argb})

    mpu.run("temperature")
    mpu.run("listener")
    mpu.run("argb")

    # -------------------------------------------------------------------------

    display = Display(testing=testing)

    # -------------------------------------------------------------------------

    modules = {
        "mpu": mpu,
        "data": data,
        "archgui": archgui,
        "display": display
    }

    data.define_modules(modules)
    archgui.define_modules(modules)
    display.define_modules(modules)

    def signal_handler(_, __):
        """
        :param _:
        :param __:
        """
        for module in modules:
            modules[module].stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    display.run()
    archgui.run()

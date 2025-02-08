"""
configuration.py
"""

import os
import sys
import signal


if __name__ == "__main__":

    argv = sys.argv
    testing = False

    if len(argv) > 1:
        if "-t" in argv:
            testing = True

    # -------------------------------------------------------------------------

    script_dir = os.path.dirname(os.path.realpath(__file__))

    from process.Data import Data
    data = Data(script_dir=script_dir, testing=testing)

    # -------------------------------------------------------------------------

    import archgui
    import mpunified

    from process.Configuration import Configuration
    from process.Preview import Preview
    from process.Temperature import temperature_run

    configuration = Configuration(testing=testing)
    preview = Preview(testing=testing)

    # -------------------------------------------------------------------------

    mpu = mpunified.mpu
    mpu.load("temperature", temperature_run)
    mpu.set_var("temperature", {"testing": testing, "gpio": data.gpio})
    mpu.run("temperature")

    # -------------------------------------------------------------------------

    modules = {
        "mpu": mpu,
        "data": data,
        "archgui": archgui,
        "configuration": configuration,
        "preview": preview
    }

    # -------------------------------------------------------------------------

    data.define_modules(modules)
    archgui.define_modules(modules)
    configuration.define_modules(modules)
    preview.define_modules(modules)

    # -------------------------------------------------------------------------

    def signal_handler(_, __):
        """
        :param _:
        :param __:
        """
        for module in modules:
            modules[module].stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # -------------------------------------------------------------------------

    configuration.run()
    archgui.run()

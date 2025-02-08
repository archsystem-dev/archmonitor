"""
Temperature.py
"""

import json
import time
import signal

from mpunified.MPUPrc import MPUPrc


def extraction(raw):
    """
    :param raw:
    :return:
    """
    if raw is not None:
        data = raw.split("\n")[1].split(" ")[9]
        return int(float(data[2:]) / 1000)
    else:
        return 0


def read(sensor):
    """
    :param sensor:
    :return:
    """
    try:

        with open("/sys/bus/w1/devices/" + sensor + "/w1_slave") as file:
            raw = file.read()
        return raw

    except Exception as err:
        print("/sys/bus/w1/devices/" + sensor + "/w1_slave")
        print(f"Unexpected {err=}, {type(err)=}")
        return None


class Temperature(MPUPrc):
    """
    Class Temperature
    """

    def __init__(self, pipe):
        super().__init__(pipe)

        self.breaker = False
        self.testing = False

        # -------------------------------------------------------------

        self.testing_force = False
        self.gpio = {}
        self.soc = None

        # -------------------------------------------------------------

        self.pipe_recv()

        # -------------------------------------------------------------

        if not self.testing:
            try:
                import gpiozero
                self.soc = gpiozero.CPUTemperature()

            except Exception as err:
                self.testing = True
                self.testing_force = True
                print("from gpiozero import CPUTemperature")
                print(f"Unexpected {err=}, {type(err)=}")
                print("Passage en mode Testing")

        # -------------------------------------------------------------

        self.temp = {
            "soc": 0,
            "sensor_1": 0,
            "sensor_2": 0,
            "sensor_3": 0
        }

    def return_sensor(self, sensor):
        """
        :param sensor:
        """

        if not self.testing:
            try:
                self.temp[sensor] = int(extraction(read(self.gpio[sensor])))
            except Exception as err:
                print("Extraction Temperature")
                print(f"Unexpected {err=}, {type(err)=}")

        else:
            if self.temp[sensor] == 0:
                self.temp[sensor] = 10
            elif self.temp[sensor] < 35:
                self.temp[sensor] += 1
            elif self.temp[sensor] == 35:
                self.temp[sensor] = 10

    def signal_handler(self, _, __):
        """
        :param self:
        :param _:
        :param __:
        """
        self.breaker = True

    def run(self):
        """
        run()
        """

        if self.testing_force:
            self.testing = True

        while True:

            if self.breaker:
                break

            for i in range(3):
                self.return_sensor("sensor_" + str(i + 1))

            if not self.testing:
                if self.soc is not None:
                    self.temp["soc"] = int(self.soc.temperature)
                else:
                    self.temp["soc"] = 0

            else:
                self.temp["soc"] = int(25)

            self.pipe_send({
                "temp": self.temp
            })

            time.sleep(0.5)


def temperature_run(pipe):
    """
    :param pipe:
    """
    temperature = Temperature(pipe)
    signal.signal(signal.SIGINT, temperature.signal_handler)
    temperature.run()

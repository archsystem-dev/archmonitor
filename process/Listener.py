"""
Listener.py
"""
import time
import signal

from mpunified.MPUPrcWAC import MPUPrcWAC


class Listener(MPUPrcWAC):
    """
    Class Listener
    """

    def __init__(self, pipe):
        super().__init__(pipe)

        self.breaker = False
        self.testing = False

        # -------------------------------------------------------------

        self.pca_pwm_100 = 0xffff

        # -------------------------------------------------------------

        self.default = {}
        self.gpio = {}
        self.cooling = {}

        # -------------------------------------------------------------

        self.mode = None

        # -------------------------------------------------------------

        self.power = False
        self.start = False

        # -------------------------------------------------------------

        self.rpm = {
            "soc": 0,
            "cpu": 0,
            "gpu": 0,
            "case": 0,
            "pump_1": 0,
            "pump_2": 0
        }

        self.temp = {
            "soc": 0,
            "sensor_1": 0,
            "sensor_2": 0,
            "sensor_3": 0,
        }

        self.pwm = {
            "soc": 0,
            "cpu": 0,
            "gpu": 0,
            "case": 0,
            "pump_1": 0,
            "pump_2": 0
        }

        # -------------------------------------------------------------

        self.tach = {
            "soc": 0, "cpu": 0, "gpu": 0, "case": 0,
            "pump_1": 0, "pump_2": 0
        }

        self.tach_divider = {
            "soc": 2, "cpu": 2, "gpu": 2, "case": 2,
            "pump_1": 2, "pump_2": 2
        }

        tach_time = time.time()
        self.tach_time = {
            "soc": tach_time, "cpu": tach_time, "gpu": tach_time, "case": tach_time,
            "pump_1": tach_time, "pump_2": tach_time
        }

        # ----------------------------------------------------------------

        self.start_collect()

        # -------------------------------------------------------------

        if not self.testing:

            try:

                import board
                import pigpio

                from gpiozero import CPUTemperature
                from adafruit_pca9685 import PCA9685

                self.pi = pigpio.pi()
                self.soc = CPUTemperature()

                self.i2c = board.I2C()
                self.pca = PCA9685(self.i2c)
                self.pca.frequency = 60

            except Exception as err:
                self.testing = True
                print("import board")
                print("import pigpio")
                print("import gpiozero")
                print("import adafruit_pca9685")
                print(f"Unexpected {err=}, {type(err)=}")

        # -------------------------------------------------------------

        # Define Start
        if not self.testing:
            self.pi.set_mode(self.gpio["pin"]["start"], pigpio.OUTPUT)
            self.pi.write(self.gpio["pin"]["start"], 0)

        # -------------------------------------------------------------

        # Define PWM lock
        if not self.testing:
            self.pi.set_mode(self.gpio["pin"]["pwm_lock"], pigpio.OUTPUT)
            self.pi.write(self.gpio["pin"]["pwm_lock"], 0)

        # -------------------------------------------------------------

        # Define POWER detection
        if not self.testing:
            self.pi.set_mode(self.gpio["pin"]["power"], pigpio.INPUT)

        # ----------------------------------------------------------------

        # Define PCA PWM
        if not self.testing:
            self.pca.channels[self.gpio["pin"]["pca"]["soc"]].duty_cycle = int(self.pca_pwm_100 / 2)
            self.pca.channels[self.gpio["pin"]["pca"]["cpu"]].duty_cycle = int(self.pca_pwm_100 / 2)
            self.pca.channels[self.gpio["pin"]["pca"]["gpu"]].duty_cycle = int(self.pca_pwm_100 / 2)
            self.pca.channels[self.gpio["pin"]["pca"]["case"]].duty_cycle = int(self.pca_pwm_100 / 2)
            self.pca.channels[self.gpio["pin"]["pca"]["pump_1"]].duty_cycle = int(self.pca_pwm_100 / 2)
            self.pca.channels[self.gpio["pin"]["pca"]["pump_2"]].duty_cycle = int(self.pca_pwm_100 / 2)

        # ----------------------------------------------------------------

        # Define TACH
        if not self.testing:
            self.pi.set_mode(self.gpio["pin"]["tach"]["soc"], pigpio.INPUT)
            self.pi.set_mode(self.gpio["pin"]["tach"]["cpu"], pigpio.INPUT)
            self.pi.set_mode(self.gpio["pin"]["tach"]["gpu"], pigpio.INPUT)
            self.pi.set_mode(self.gpio["pin"]["tach"]["case"], pigpio.INPUT)
            self.pi.set_mode(self.gpio["pin"]["tach"]["pump_1"], pigpio.INPUT)
            self.pi.set_mode(self.gpio["pin"]["tach"]["pump_2"], pigpio.INPUT)

        # ----------------------------------------------------------------

        # Run TACH Callback
        if not self.testing:
            self.pi.callback(self.gpio["pin"]["tach"]["soc"], pigpio.RISING_EDGE, self.cb_soc_rpm)
            self.pi.callback(self.gpio["pin"]["tach"]["cpu"], pigpio.RISING_EDGE, self.cb_cpu_rpm)
            self.pi.callback(self.gpio["pin"]["tach"]["gpu"], pigpio.RISING_EDGE, self.cb_gpu_rpm)
            self.pi.callback(self.gpio["pin"]["tach"]["case"], pigpio.RISING_EDGE, self.cb_case_rpm)
            self.pi.callback(self.gpio["pin"]["tach"]["pump_1"], pigpio.RISING_EDGE, self.cb_pump_1_rpm)
            self.pi.callback(self.gpio["pin"]["tach"]["pump_2"], pigpio.RISING_EDGE, self.cb_pump_2_rpm)

    def start_power(self):
        if not self.testing:
            self.pi.write(self.gpio["pin"]["start"], 1)
            time.sleep(1)
            self.pi.write(self.gpio["pin"]["start"], 0)

    def detect_power(self):
        if not self.testing:
            if self.pi.read(self.gpio["pin"]["power"]):
                self.power = True
            else:
                self.power = False
        else:
            self.power = True

    def pwm_lock(self):
        self.pi.write(self.gpio["pin"]["pwm_lock"], 0)
        
    def pwm_unlock(self):
        self.pi.write(self.gpio["pin"]["pwm_lock"], 1)
        

    def pwm_by_temp(self, mode, target, value=0):
        """
        :param mode:
        :param target:
        :param value:
        :return:
        """

        degree_min = 0

        if target != "pump_1" and target != "pump_2":
            degree_min = 0

        if target == "pump_1" or target == "pump_2":
            pwm = self.cooling[mode][target]["pwm"]

        else:
            
            if target == "soc":
                pwm_min = self.cooling["soc"]["pwm_min"]
                pwm_max = self.cooling["soc"]["pwm_max"]
                temp_max = self.cooling["soc"]["temp_max"]
            else:
                pwm_min = self.cooling[mode][target]["pwm_min"]
                pwm_max = self.cooling[mode][target]["pwm_max"]
                temp_max = self.cooling[mode][target]["temp_max"]

            pwm = pwm_min

            if degree_min < value < temp_max:

                pwm_gap = pwm_max - pwm_min
                degree_gap = temp_max - degree_min
                value_gaped = value - degree_min
                divider = (degree_gap / value_gaped)

                pwm = pwm_min + (pwm_gap / divider)

            elif temp_max <= value:

                pwm = pwm_max

        return int(pwm)

    def cb_soc_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["soc"] += 1

    def cb_cpu_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["cpu"] += 1

    def cb_gpu_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["gpu"] += 1

    def cb_case_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["case"] += 1

    def cb_pump_1_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["pump_1"] += 1

    def cb_pump_2_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["pump_2"] += 1

    def rpm_calc(self, target, tach_time):
        """
        rpm_calc()
        """

        if not self.testing:

            rpm = self.tach[target] / (tach_time - self.tach_time[target])
            rpm *= 60
            rpm = int(rpm / self.tach_divider[target])

            self.tach[target] = 0
            self.tach_time[target] = tach_time

        else:
            if target == "pump_1" or target == "pump_2":
                rpm = int((5000 / 100) * self.pwm[target] / 10) * 10
            else:
                rpm = int((1200 / 100) * self.pwm[target] / 10) * 10

        self.rpm[target] = int(rpm / 50) * 50

    def signal_handler(self, _, __):
        """
        :param self:
        :param _:
        :param __:
        """
        self.pwm_lock()
        self.pi.stop()
        self.breaker = True

    def run(self):
        """
        run()
        """

        self.mode = self.default["mode"]

        if not self.testing:
            self.pwm_unlock()
        

        tach_time = time.time()
        while True:

            if self.breaker:
                break

            self.detect_power()

            if self.start and not self.power:
                self.start_power()
                self.start = False

            # Calc PWM Duty Cycle
            for target in self.pwm:
                if target not in ["pump_1", "pump_2"]:

                    if target == "soc":
                        temp = self.temp[target]
                    else:
                        id = list(self.gpio["sensors"].keys())[list(self.gpio["sensors"].values()).index(target)]
                        temp = self.temp["sensor_" + str(id)]

                    self.pwm[target] = self.pwm_by_temp(
                        self.mode,
                        target,
                        temp)

                else:
                    self.pwm[target] = self.pwm_by_temp(self.mode, target)

            # ------------------------------------------------------

            # Change new PCA PWM Duty Cycle
            if not self.testing:
                for target in self.pwm:
                    self.pca.channels[self.gpio["pin"]["pca"][target]].duty_cycle = \
                        int(self.pca_pwm_100 * (self.pwm[target] / 100))

            # ------------------------------------------------------

            # Calc TACH
            new_tach_time = time.time()
            if new_tach_time - tach_time > 1:
                for target in self.rpm:
                    self.rpm_calc(target, new_tach_time)
                tach_time = new_tach_time

            # ------------------------------------------------------

            self.pipe_send({
                "power": self.power,
                "mode": self.mode,
                "pwm": self.pwm,
                "rpm": self.rpm,
                "temp": self.temp
            })

            time.sleep(0.2)


def listener_run(pipe):
    """
    :param pipe:
    """
    listener = Listener(pipe)
    signal.signal(signal.SIGINT, listener.signal_handler)
    listener.run()

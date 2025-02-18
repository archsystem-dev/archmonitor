import os
import sys
import glob

if __name__ == "__main__":

    argv = sys.argv
    testing = False

    if len(argv) > 1:
        if "-t" in argv:
            testing = True

    script_dir = os.path.dirname(os.path.realpath(__file__))
    from process.Data import Data
    data = Data(script_dir=script_dir, testing=testing, sensors_detection=True)

    dir_sensor = "/sys/bus/w1/devices/"

    if os.path.isdir(dir_sensor):
        raw = glob.glob(dir_sensor + "28*/w1_slave")

        for i in range(3):
            if len(raw) > i:
                id = raw[i].replace(dir_sensor, "")
                id = id.replace("/w1_slave", "")
                data.gpio["sensor_" + str(i + 1)] = id
            else:
                data.gpio["sensor_" + str(i + 1)] = "N/A"

        if len(raw) < 3:
            print("Sonde de température manquante.")
        else:
            data.save_data()
            print("Les sondes ont été ajoutées au fichier de configuration.")

    else:
        for i in range(3):
            data.gpio["sensor_" + str(i + 1)] = "N/A"
        print("Aucune sonde de température trouvée.")

    

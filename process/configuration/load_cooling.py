def load_cooling(configuration):

    items = []
    for i in ["silent", "performance"]:

        for j in ["cpu", "gpu", "case"]:
            items.append({
                "item": "cooling_" + i + "_" + j + "_pwm_min",
                "mode": "replace",
                "value": configuration.modules["data"].values["pwm"],
                "default_value": configuration.modules["data"].cooling[i][j]["pwm_min"]
            })
            items.append({
                "item": "cooling_" + i + "_" + j + "_pwm_max",
                "mode": "replace",
                "value": configuration.modules["data"].values["pwm"],
                "default_value": configuration.modules["data"].cooling[i][j]["pwm_max"]
            })
            items.append({
                "item": "cooling_" + i + "_" + j + "_temp_base",
                "mode": "replace",
                "value": configuration.modules["data"].values["temp_base"],
                "default_value": configuration.modules["data"].cooling[i][j]["temp_base"]
            })
            items.append({
                "item": "cooling_" + i + "_" + j + "_temp_max",
                "mode": "replace",
                "value": configuration.modules["data"].values["temp_max"],
                "default_value": configuration.modules["data"].cooling[i][j]["temp_max"]
            })

        for j in ["pump_1", "pump_2"]:
            items.append({
                "item": "cooling_" + i + "_" + j + "_pwm",
                "mode": "replace",
                "value": configuration.modules["data"].values["pwm"],
                "default_value": configuration.modules["data"].cooling[i][j]["pwm"]
            })

    configuration.modules["archgui"].update(items=items)

    # --------------------------------------------------------------------

    configuration.modules["mpu"].set_var("temperature", {
        "gpio": configuration.modules["data"].gpio
    })

    # --------------------------------------------------------------------

    items = []

    for i in ["1", "2", "3"]:
        items.append({
            "item": "sensor_" + i + "_target",
            "mode": "replace",
            "value": configuration.modules["data"].gpio["sensor_" + i]
        })
        items.append({
            "item": "sensor_" + i + "_value",
            "mode": "replace",
            "value": ["cpu", "gpu", "case"],
            "default_value": configuration.modules["data"].gpio["sensors"][i]
        })

    for i in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
        items.append({
            "item": "gpio_tach_" + i,
            "mode": "replace",
            "value": configuration.modules["data"].values["tach"],
            "default_value": configuration.modules["data"].gpio["pin"]["tach"][i]
        })

    for i in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
        items.append({
            "item": "gpio_pca_" + i,
            "mode": "replace",
            "value": configuration.modules["data"].values["pca"],
            "default_value": configuration.modules["data"].gpio["pin"]["pca"][i]
        })

    configuration.modules["archgui"].update(items=items)
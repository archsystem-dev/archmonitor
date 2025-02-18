def load_theme(configuration, theme_name):
    """
    :param theme_name:
    """

    theme = configuration.modules["data"].themes[theme_name]
    configuration.current_theme = theme
    configuration.change_pwm_steps(theme["global"]["pwm_steps"])

    items = [
        {
            "item": "theme_name",
            "mode": "replace",
            "value": theme_name,
        },
        {
            "item": "theme_select",
            "mode": "replace",
            "value": list(configuration.modules["data"].themes),
            "default_value": configuration.modules["data"].default["theme"]
        }, {
            "item": "theme_background_color",
            "mode": "replace",
            "value": theme["global"]["background_color"]
        }, {
            "item": "theme_pwm_steps",
            "mode": "replace",
            "value": configuration.modules["data"].values["pwm_steps"],
            "default_value": theme["global"]["pwm_steps"]
        }, {
            "item": "theme_pwm_steps_orientation",
            "mode": "replace",
            "value": configuration.modules["data"].values["pwm_steps_orientation"],
            "default_value": theme["global"]["pwm_steps_orientation"]
        }, {
            "item": "theme_logo",
            "mode": "replace",
            "value": theme["images"]["logo"]
        }, {
            "item": "theme_background",
            "mode": "replace",
            "value": theme["images"]["background"]
        }, {
            "item": "theme_standby_off",
            "mode": "replace",
            "value": theme["images"]["standby_off"]
        }, {
            "item": "theme_standby_on",
            "mode": "replace",
            "value": theme["images"]["standby_on"]
        }
    ]

    # ---------------------------------------------------
    # Theme Images
    # ---------------------------------------------------

    for i in ["argb", "mode", "pwm", "rpm", "temp"]:

        jj = []

        if i == "argb":
            jj = ["a", "b", "c", "d", "e", "f"]

        if i == "mode":
            jj = ["silent", "performance"]

        for j in jj:
            items.append({
                "item": "theme_" + i + "_" + j + "_off",
                "mode": "replace",
                "value": theme["images"][i + "_" + j + "_off"]
            })
            items.append({
                "item": "theme_" + i + "_" + j + "_on",
                "mode": "replace",
                "value": theme["images"][i + "_" + j + "_on"]
            })

    for step in range(theme["global"]["pwm_steps"]):
        items.append({
            "item": "theme_pwm_step_" + str(step + 1) + "_off",
            "mode": "replace",
            "value": theme["images"]["pwm_step_" + str(step + 1) + "_off"]
        })
        items.append({
            "item": "theme_pwm_step_" + str(step + 1) + "_on",
            "mode": "replace",
            "value": theme["images"]["pwm_step_" + str(step + 1) + "_on"]
        })

    # ---------------------------------------------------
    # Theme Fonts
    # ---------------------------------------------------

    font_size = []
    for s in range(31):
        font_size.append(s + 10)

    for i in ["rpm", "temp"]:
        for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
            if j in theme[i]:
                for k in ["f", "s", "h", "w", "bgc", "c"]:
                    if k == "s":
                        items.append({
                            "item": "theme_" + i + "_" + j + "_" + k,
                            "mode": "replace",
                            "value": font_size,
                            "default_value": theme[i][j][k]
                        })
                    else:
                        items.append({
                            "item": "theme_" + i + "_" + j + "_" + k,
                            "mode": "replace",
                            "value": theme[i][j][k]
                        })

    # ---------------------------------------------------
    # Theme Positions
    # ---------------------------------------------------

    for i in ["argb", "mode", "pwm", "rpm", "temp"]:

        jj = []

        if i == "argb":
            jj = ["a", "b", "c", "d", "e", "f"]

        if i == "mode":
            jj = ["silent", "performance"]

        if i in ["pwm", "rpm"]:
            jj = ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]

        if i == "temp":
            jj = ["soc", "cpu", "gpu", "case"]

        for j in jj:
            items.append({
                "item": "theme_" + i + "_" + j + "_x",
                "mode": "replace",
                "value": theme[i][j]["x"]
            })
            items.append({
                "item": "theme_" + i + "_" + j + "_y",
                "mode": "replace",
                "value": theme[i][j]["y"]
            })

    configuration.modules["archgui"].update(items=items)
def change_pwm_steps(configuration, steps):
    """
    :param steps:
    """

    if steps == configuration.modules["data"].values["pwm_steps"][1]:
        pwm_steps_20 = "show"
    else:
        pwm_steps_20 = "hide"

    items = [{
        "item": "tab_theme_pwm_steps_20",
        "mode": pwm_steps_20
    }]

    configuration.modules["archgui"].update(items=items)
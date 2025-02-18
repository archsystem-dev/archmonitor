def load_default_parameters(configuration):
    """
    load_default_parameters()
    """

    items = [
        {
            "item": "parameters_theme",
            "mode": "replace",
            "value": list(configuration.modules["data"].themes),
            "default_value": configuration.modules["data"].default["theme"]
        }, {
            "item": "parameters_mode",
            "mode": "replace",
            "value": ["silent", "performance"],
            "default_value": configuration.modules["data"].default["mode"]
        }, {
            "item": "parameters_argb",
            "mode": "replace",
            "value": ["a", "b", "c", "d", "e", "f"],
            "default_value": configuration.modules["data"].default["argb"]
        }
    ]

    configuration.modules["archgui"].update(items=items)
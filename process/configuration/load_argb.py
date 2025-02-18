def load_argb(configuration):
    """
    load_argb()
    """

    items = [{
        "item": "argb_number_led",
        "mode": "replace",
        "value": configuration.modules["data"].values["number_argb"],
        "default_value": configuration.modules["data"].argb["number"]
    }]

    for i in configuration.modules["data"].values["argb_app"]:
        items.append({
            "item": "argb_" + i + "_mode",
            "mode": "replace",
            "value": configuration.modules["data"].values["argb_mode"],
            "default_value": configuration.modules["data"].argb[i]["mode"]
        })
        items.append({
            "item": "argb_" + i + "_color_1",
            "mode": "replace",
            "value": configuration.modules["data"].argb[i]["color_1"]
        })
        items.append({
            "item": "argb_" + i + "_color_2",
            "mode": "replace",
            "value": configuration.modules["data"].argb[i]["color_2"]
        })
        items.append({
            "item": "argb_" + i + "_color_3",
            "mode": "replace",
            "value": configuration.modules["data"].argb[i]["color_3"]
        })
        items.append({
            "item": "argb_" + i + "_intensity_min",
            "mode": "replace",
            "value": configuration.modules["data"].values["intensity_min"],
            "default_value": configuration.modules["data"].argb[i]["intensity_min"]
        })
        items.append({
            "item": "argb_" + i + "_speed",
            "mode": "replace",
            "value": configuration.modules["data"].values["speed"],
            "default_value": configuration.modules["data"].argb[i]["speed"]
        })

    configuration.modules["archgui"].update(items=items)

    for i in configuration.modules["data"].values["argb_app"]:
        configuration.change_argb_mode("argb_" + i + "_mode")
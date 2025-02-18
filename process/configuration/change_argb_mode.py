def change_argb_mode(configuration, target):
    """
    :param target:
    """

    value = configuration.modules["archgui"].get_item(target)

    target = target.replace("argb_", "")
    target = target.replace("_mode", "")

    keys = [
        "argb_" + target + "_color_1",
        "argb_" + target + "_color_2",
        "argb_" + target + "_color_3",
        "argb_" + target + "_color_1b",
        "argb_" + target + "_color_2b",
        "argb_" + target + "_color_3b",
        "argb_" + target + "_speed",
        "argb_" + target + "_intensity_min"
    ]

    items = []
    if value == "Off":
        for key in keys:
            items.append({
                "item": key,
                "mode": "disabled",
                "value": True
            })

    if value == "Fixe":
        for key in keys:

            if key in ["argb_" + target + "_color_1", "argb_" + target + "_color_1b"]:
                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": False
                })
            else:
                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": True
                })

    if value == "Pulse":
        for key in keys:

            if key in [
                "argb_" + target + "_color_2", "argb_" + target + "_color_2b",
                "argb_" + target + "_color_3", "argb_" + target + "_color_3b"
            ]:

                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": True
                })

            else:
                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": False
                })

    if value == "Pulse Two Colors":
        for key in keys:
            if key in ["argb_" + target + "_color_3", "argb_" + target + "_color_3b"]:

                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": True
                })

            else:
                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": False
                })

    if value == "Pulse Three Colors":
        for key in keys:
            items.append({
                "item": key,
                "mode": "disabled",
                "value": False
            })

    if value == "Switch Two Colors":
        for key in keys:
            if key in [
                "argb_" + target + "_color_3", "argb_" + target + "_color_3b",
                "argb_" + target + "_intensity_min"
            ]:

                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": True
                })

            else:
                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": False
                })

    if value == "Switch Three Colors":
        for key in keys:
            if key in "argb_" + target + "_intensity_min":

                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": True
                })

            else:
                items.append({
                    "item": key,
                    "mode": "disabled",
                    "value": False
                })

    configuration.modules["archgui"].update(items)
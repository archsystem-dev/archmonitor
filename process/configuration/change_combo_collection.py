def change_combo_collection(configuration, keys, values, target):
    """
    :param keys:
    :param values:
    :param target:
    """

    collection = []
    for key in keys:
        collection.append(configuration.modules["archgui"].get_item(key))

    missing = values[0]
    for value in values:
        if value not in collection:
            missing = value

    value = configuration.modules["archgui"].get_item(target)

    i = 0
    for key in keys:
        if target != key:
            if value == collection[i]:
                configuration.modules["archgui"].update([
                    {
                        "item": key,
                        "mode": "replace",
                        "default_value": missing
                    }])
        i += 1
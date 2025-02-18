def print_active_argb(display, argb):

    figs = {
        "back": [],
        "front": []
    }

    for i in ["a", "b", "c", "d", "e", "f"]:
        if i == argb:
            figs["back"].append(display.figures["argb"][i]["off"])
            figs["front"].append(display.figures["argb"][i]["on"])
        else:
            figs["front"].append(display.figures["argb"][i]["off"])
            figs["back"].append(display.figures["argb"][i]["on"])

    for fig in figs["back"]:
        display.modules["archgui"].graph_send_figure_to_back(
            uniqid=display.window,
            graph=display.graph_monitor,
            figure=fig)

    for fig in figs["front"]:
        display.modules["archgui"].graph_bring_figure_to_front(
            uniqid=display.window,
            graph=display.graph_monitor,
            figure=fig)
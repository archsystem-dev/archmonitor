def print_active_mode(display, mode):

    figs = {
        "back": [],
        "front": []
    }

    for i in ["silent", "performance"]:
        if i == mode:
            figs["back"].append(display.figures["mode"][i]["off"])
            figs["front"].append(display.figures["mode"][i]["on"])
        else:
            figs["front"].append(display.figures["mode"][i]["off"])
            figs["back"].append(display.figures["mode"][i]["on"])

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
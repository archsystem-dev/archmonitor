def pre_print_argb(display):

    for argb in ["a", "b", "c", "d", "e", "f"]:
        display.figures["argb"][argb] = {
            "on": None,
            "off": None
        }

        display.figures["argb"][argb]["on"] = display.modules["archgui"].graph_draw_image(
            uniqid=display.window,
            graph=display.graph_monitor,
            location=(display.theme["argb"][argb]["x"], display.theme["argb"][argb]["y"]),
            image=display.images["argb"][argb]["on"])

        display.figures["argb"][argb]["off"] = display.modules["archgui"].graph_draw_image(
            uniqid=display.window,
            graph=display.graph_monitor,
            location=(display.theme["argb"][argb]["x"], display.theme["argb"][argb]["y"]),
            image=display.images["argb"][argb]["off"])

        display.modules["archgui"].graph_send_figure_to_back(
            uniqid=display.window,
            graph=display.graph_monitor,
            figure=display.figures["argb"][argb]["on"])
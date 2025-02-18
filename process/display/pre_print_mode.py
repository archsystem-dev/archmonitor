def pre_print_mode(display):

    for mode in ["silent", "performance"]:
        display.figures["mode"][mode] = {
            "on": None,
            "off": None
        }

        display.figures["mode"][mode]["on"] = display.modules["archgui"].graph_draw_image(
            uniqid=display.window,
            graph=display.graph_monitor,
            location=(display.theme["mode"][mode]["x"], display.theme["mode"][mode]["y"]),
            image=display.images["mode"][mode]["on"])

        display.figures["mode"][mode]["off"] = display.modules["archgui"].graph_draw_image(
            uniqid=display.window,
            graph=display.graph_monitor,
            location=(display.theme["mode"][mode]["x"], display.theme["mode"][mode]["y"]),
            image=display.images["mode"][mode]["off"])
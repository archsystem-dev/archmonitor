def pre_print_standby(display):

    display.figures["standby"]["on"] = display.modules["archgui"].graph_draw_image(
        uniqid=display.window,
        graph=display.graph_standby,
        location=(10, 10),
        image=display.images["standby"]["on"])

    display.figures["standby"]["off"] = display.modules["archgui"].graph_draw_image(
        uniqid=display.window,
        graph=display.graph_standby,
        location=(10, 10),
        image=display.images["standby"]["off"])

    display.modules["archgui"].graph_send_figure_to_back(
        uniqid=display.window,
        graph=display.graph_standby,
        figure=display.figures["standby"]["on"])
def print_active_standby(display):

    display.modules["archgui"].graph_send_figure_to_back(
        uniqid=display.window,
        graph=display.graph_standby,
        figure=display.figures["standby"]["off"])

    display.modules["archgui"].graph_bring_figure_to_front(
        uniqid=display.window,
        graph=display.graph_monitor,
        figure=display.figures["standby"]["on"])
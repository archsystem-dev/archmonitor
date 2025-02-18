def print_pwm(display, target, value):

    x = display.theme["pwm"][target]["x"]
    for j in range(len(display.figures["pwm"][target]["on"])):
        x += display.images["pwm_step"]["off"][j].width

    if len(display.figures["pwm"][target]["on"]) < value:
        display.figures["pwm"][target]["on"].append(display.modules["archgui"].graph_draw_image(
            uniqid=display.window,
            graph=display.graph_monitor,
            location=(x, display.theme["pwm"][target]["y"]),
            image=display.images["pwm_step"]["on"][len(display.figures["pwm"][target]["on"])]))

    if len(display.figures["pwm"][target]["on"]) > value:
        display.modules["archgui"].graph_delete_figure(
            uniqid=display.window,
            graph=display.graph_monitor,
            figure=display.figures["pwm"][target]["on"][-1])
        display.figures["pwm"][target]["on"].pop()

    display.pwm[target] = len(display.figures["pwm"][target]["on"])
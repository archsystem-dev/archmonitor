def pre_print_pwm(display, target):

    display.figures["pwm"][target] = {
        "off": [],
        "on": []}

    for i in range(display.theme["global"]["pwm_steps"]):

        x = display.theme["pwm"][target]["x"]
        for j in range(i):
            x += display.images["pwm_step"]["off"][j].width

        display.figures["pwm"][target]["off"].append(display.modules["archgui"].graph_draw_image(
            uniqid=display.window,
            graph=display.graph_monitor,
            location=(x, display.theme["pwm"][target]["y"]),
            image=display.images["pwm_step"]["off"][i]))
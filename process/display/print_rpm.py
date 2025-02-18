from PIL import Image, ImageDraw

def print_rpm(display, target, rpm):

    canvas = Image.new(
        "RGBA",
        (display.theme["rpm"][target]["w"], display.theme["rpm"][target]["h"]),
        color=display.hex_to_rgb(display.theme["rpm"][target]["bgc"]))

    image = ImageDraw.Draw(canvas)
    image.text(
        (0, 0),
        str(rpm),
        font=display.font["rpm"][target],
        text_color=display.hex_to_rgb(display.theme["rpm"][target]["c"])
    )

    display.figures["rpm"][target].append(display.modules["archgui"].graph_draw_image(
        uniqid=display.window,
        graph=display.graph_monitor,
        location=(display.theme["rpm"][target]["x"], display.theme["rpm"][target]["y"]),
        image=canvas))

    if display.figures["rpm"][target][0] != "startup":
        display.modules["archgui"].graph_delete_figure(
            uniqid=display.window,
            graph=display.graph_monitor,
            figure=display.figures["rpm"][target][0])

    del display.figures["rpm"][target][0]
from PIL import Image, ImageDraw

def print_degree(display, target, degree):

    if target != "soc":
        target = display.gpio["sensors"][target.replace("sensor_", "")]

    canvas = Image.new(
        "RGBA",
        (display.theme["temp"][target]["w"], display.theme["temp"][target]["h"]),
        color=display.list_to_tuple(display.theme["temp"][target]["bgc"]))

    image = ImageDraw.Draw(canvas)
    image.text(
        (0, 0),
        str(degree),
        font=display.font["temp"][target],
        text_color=display.hex_to_rgb(display.theme["temp"][target]["c"])
    )

    display.figures["temp"][target].append(display.modules["archgui"].graph_draw_image(
        uniqid=display.window,
        graph=display.graph_monitor,
        location=(display.theme["temp"][target]["x"], display.theme["temp"][target]["y"]),
        image=canvas))

    if display.figures["temp"][target][0] != "startup":
        display.modules["archgui"].graph_delete_figure(
            uniqid=display.window,
            graph=display.graph_monitor,
            figure=display.figures["temp"][target][0])

    del display.figures["temp"][target][0]
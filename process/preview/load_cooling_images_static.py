from PIL import Image, ImageDraw, ImageFont

def load_cooling_images_static(preview):

    font = ImageFont.truetype(
        preview.modules["data"].script_dir + "/resource/RobotoMono-Regular.ttf",
        20
    )

    for i in range(0, 105, 5):
        canvas = Image.new(
            "RGBA",
            (40, 28),
            color=preview.list_to_tuple((00, 00, 00, 255)))

        if i < 10:
            x = 22
        elif i < 100:
            x = 11
        else:
            x = 0

        image = ImageDraw.Draw(canvas)
        image.text(
            (x, 0),
            str(i),
            font=font,
            text_color=(255, 255, 255, 255),
        )

        preview.cooling_images["static"][str(i)] = canvas

    # -------------------------------------------------------

    canvas = Image.new(
        "RGBA",
        (60, 28),
        color=preview.list_to_tuple((00, 00, 00, 255)))

    image = ImageDraw.Draw(canvas)
    image.text(
        (0, 0),
        "CPU",
        font=font,
        text_color=(255, 255, 255, 255),
    )

    preview.cooling_images["static"]["cpu"] = canvas

    # -------------------------------------------------------

    canvas = Image.new(
        "RGBA",
        (60, 28),
        color=preview.list_to_tuple((00, 00, 00, 255)))

    image = ImageDraw.Draw(canvas)
    image.text(
        (0, 0),
        "GPU",
        font=font,
        text_color=(255, 255, 255, 255),
    )

    preview.cooling_images["static"]["gpu"] = canvas

    # -------------------------------------------------------

    canvas = Image.new(
        "RGBA",
        (60, 28),
        color=preview.list_to_tuple((00, 00, 00, 255)))

    image = ImageDraw.Draw(canvas)
    image.text(
        (0, 0),
        "Case",
        font=font,
        text_color=(255, 255, 255, 255),
    )

    preview.cooling_images["static"]["case"] = canvas

    # -------------------------------------------------------

    canvas = Image.new(
        "RGBA",
        (80, 28),
        color=preview.list_to_tuple((00, 00, 00, 255)))

    image = ImageDraw.Draw(canvas)
    image.text(
        (0, 0),
        "Pump 1",
        font=font,
        text_color=(255, 255, 255, 255),
    )

    preview.cooling_images["static"]["pump_1"] = canvas

    # -------------------------------------------------------

    canvas = Image.new(
        "RGBA",
        (80, 28),
        color=preview.list_to_tuple((00, 00, 00, 255)))

    image = ImageDraw.Draw(canvas)
    image.text(
        (0, 0),
        "Pump 2",
        font=font,
        text_color=(255, 255, 255, 255),
    )

    preview.cooling_images["static"]["pump_2"] = canvas

    # -------------------------------------------------------

    x = 80
    j = 0
    y = 340

    for i in range(0, 110, 10):
        preview.modules["archgui"].graph_draw_image(
            graph=preview.graph_cooling_silent,
            location=(x, y - (j * 28)),
            image=preview.cooling_images["static"][str(i)])

        preview.modules["archgui"].graph_draw_image(
            graph=preview.graph_cooling_performance,
            location=(x, y - (j * 28)),
            image=preview.cooling_images["static"][str(i)])

        j += 1

    x += 40
    j = 0

    for i in range(5, 65, 5):
        preview.modules["archgui"].graph_draw_image(
            graph=preview.graph_cooling_silent,
            location=(x + (j * 50), y),
            image=preview.cooling_images["static"][str(i)])

        preview.modules["archgui"].graph_draw_image(
            graph=preview.graph_cooling_performance,
            location=(x + (j * 50), y),
            image=preview.cooling_images["static"][str(i)])

        j += 1

    # -------------------------------------------------------------------

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_silent,
        point_from=(x, y),
        point_to=(720, y),
        color="white",
        width=2
    )

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_performance,
        point_from=(x, y),
        point_to=(720, y),
        color="white",
        width=2
    )

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_silent,
        point_from=(x, y),
        point_to=(x, 60),
        color="white",
        width=2
    )

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_performance,
        point_from=(x, y),
        point_to=(x, 60),
        color="white",
        width=2
    )

    # -------------------------------------------------------------------

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_silent,
        point_from=(x + 20, 395),
        point_to=(x + 60, 395),
        color="red",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_silent,
        location=(x + 60 + 10, 380),
        image=preview.cooling_images["static"]["cpu"])

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_performance,
        point_from=(x + 20, 395),
        point_to=(x + 60, 395),
        color="red",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_performance,
        location=(x + 60 + 10, 380),
        image=preview.cooling_images["static"]["cpu"])

    # -------------------------------------------------------------------

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_silent,
        point_from=(x + 20, 425),
        point_to=(x + 60, 425),
        color="yellow",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_silent,
        location=(x + 60 + 10, 410),
        image=preview.cooling_images["static"]["gpu"])

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_performance,
        point_from=(x + 20, 425),
        point_to=(x + 60, 425),
        color="yellow",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_performance,
        location=(x + 60 + 10, 410),
        image=preview.cooling_images["static"]["gpu"])

    # -------------------------------------------------------------------

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_silent,
        point_from=(x + 220, 395),
        point_to=(x + 220 + 40, 395),
        color="green",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_silent,
        location=(x + 220 + 40 + 10, 380),
        image=preview.cooling_images["static"]["case"])

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_performance,
        point_from=(x + 220, 395),
        point_to=(x + 220 + 40, 395),
        color="green",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_performance,
        location=(x + 220 + 40 + 10, 380),
        image=preview.cooling_images["static"]["case"])

    # -------------------------------------------------------------------

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_silent,
        point_from=(x + 420, 395),
        point_to=(x + 420 + 40, 395),
        color="violet",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_silent,
        location=(x + 420 + 40 + 10, 380),
        image=preview.cooling_images["static"]["pump_1"])

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_performance,
        point_from=(x + 420, 395),
        point_to=(x + 420 + 40, 395),
        color="violet",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_performance,
        location=(x + 420 + 40 + 10, 380),
        image=preview.cooling_images["static"]["pump_1"])

    # -------------------------------------------------------------------

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_silent,
        point_from=(x + 420, 425),
        point_to=(x + 420 + 40, 425),
        color="cyan",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_silent,
        location=(x + 420 + 40 + 10, 410),
        image=preview.cooling_images["static"]["pump_2"])

    preview.modules["archgui"].graph_draw_line(
        graph=preview.graph_cooling_performance,
        point_from=(x + 420, 425),
        point_to=(x + 420 + 40, 425),
        color="cyan",
        width=12
    )

    preview.modules["archgui"].graph_draw_image(
        graph=preview.graph_cooling_performance,
        location=(x + 420 + 40 + 10, 410),
        image=preview.cooling_images["static"]["pump_2"])
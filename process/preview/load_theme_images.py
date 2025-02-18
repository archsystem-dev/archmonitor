import os

from PIL import Image, ImageDraw, ImageFont

def load_theme_images(preview):
    preview.theme_images = {}

    for image in preview.theme["images"]:

        path = ""
        if "/" not in preview.theme["images"][image]:
            path = preview.modules["data"].script_dir + "/themes/" + preview.theme["name"] + "/"

        if os.path.isfile(path + preview.theme["images"][image]):
            preview.theme_images[image] = Image.open(path + preview.theme["images"][image])

    text_prev = {
        "rpm": "2500",
        "temp": "30"
    }

    for text in ["rpm", "temp"]:
        for target in preview.theme[text]:

            path = ""
            if "/" not in preview.theme[text][target]["f"]:
                path = preview.modules["data"].script_dir + "/themes/" + preview.theme["name"] + "/"

            font = ImageFont.truetype(
                path + preview.theme[text][target]["f"],
                preview.theme[text][target]["s"]
            )

            bgc_color = preview.theme[text][target]["bgc"]
            if isinstance(preview.theme[text][target]["bgc"], list):
                bgc_color = preview.rgb_to_hex(preview.theme[text][target]["bgc"])

            c_color = preview.theme[text][target]["c"]
            if isinstance(preview.theme[text][target]["c"], list):
                c_color = preview.rgb_to_hex(preview.theme[text][target]["c"])

            canvas = Image.new(
                "RGBA",
                (preview.theme[text][target]["w"], preview.theme[text][target]["h"]),
                color=preview.list_to_tuple(bgc_color))

            image = ImageDraw.Draw(canvas)
            image.text(
                (0, 0),
                text_prev[text],
                font=font,
                text_color=c_color
            )

            preview.theme_images[text + "_" + target] = canvas
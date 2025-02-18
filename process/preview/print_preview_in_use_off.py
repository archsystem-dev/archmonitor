def print_preview_in_use_off(preview):

    for figure in preview.theme_figures["in_use_off"]:
        preview.modules["archgui"].graph_delete_figure(
            graph=preview.graph_theme_in_use_off,
            figure=preview.theme_figures["in_use_off"][figure])

    if "background" in preview.theme_images:
        fn = "background"
        preview.theme_figures["in_use_off"][fn] = preview.modules["archgui"].graph_draw_image(
            graph=preview.graph_theme_in_use_off,
            location=(10, 10),
            image=preview.theme_images["background"])

    for i in ["a", "b", "c", "d", "e", "f"]:

        if "argb_" + i + "_off" in preview.theme_images:
            fn = "argb_" + i
            preview.theme_figures["in_use_off"][fn] = preview.modules["archgui"].graph_draw_image(
                graph=preview.graph_theme_in_use_off,
                location=(
                    preview.theme["argb"][i]["x"],
                    preview.theme["argb"][i]["y"]
                ),
                image=preview.theme_images["argb_" + i + "_off"])

    for i in ["silent", "performance"]:

        if "mode_" + i + "_off" in preview.theme_images:
            fn = "mode_" + i
            preview.theme_figures["in_use_off"][fn] = preview.modules["archgui"].graph_draw_image(
                graph=preview.graph_theme_in_use_off,
                location=(
                    preview.theme["mode"][i]["x"],
                    preview.theme["mode"][i]["y"]
                ),
                image=preview.theme_images["mode_" + i + "_off"])

    for i in range(preview.theme["global"]["pwm_steps"]):
        for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:

            x = preview.theme["pwm"][j]["x"]
            for k in range(i):
                if "pwm_step_" + str(k + 1) + "_off" in preview.theme_images:
                    x += preview.theme_images["pwm_step_" + str(k + 1) + "_off"].width

            if "pwm_step_" + str(i + 1) + "_off" in preview.theme_images:
                fn = "pwm_" + j + "_" + str(i + 1)
                preview.theme_figures["in_use_off"][fn] = preview.modules["archgui"].graph_draw_image(
                    graph=preview.graph_theme_in_use_off,
                    location=(x, preview.theme["pwm"][j]["y"]),
                    image=preview.theme_images["pwm_step_" + str(i + 1) + "_off"])

    for i in ["rpm", "temp"]:
        for j in ["soc", "cpu", "gpu", "case", "pump_1", "pump_2"]:
            if i + "_" + j in preview.theme_images:
                fn = i + "_" + j + "_" + i
                preview.theme_figures["in_use_off"][fn] = preview.modules["archgui"].graph_draw_image(
                    graph=preview.graph_theme_in_use_off,
                    location=(
                        preview.theme[i][j]["x"],
                        preview.theme[i][j]["y"]
                    ),
                    image=preview.theme_images[i + "_" + j])
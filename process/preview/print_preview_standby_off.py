def print_preview_standby_off(preview):

    for figure in preview.theme_figures["standby_off"]:
        preview.modules["archgui"].graph_delete_figure(
            graph=preview.graph_theme_standby_off,
            figure=preview.theme_figures["standby_off"][figure])

    if "standby_off" in preview.theme_images:
        preview.theme_figures["standby_off"]["button"] = preview.modules["archgui"].graph_draw_image(
            graph=preview.graph_theme_standby_off,
            location=(10, 10),
            image=preview.theme_images["standby_off"]
        )
def print_preview_standby_on(preview):

    for figure in preview.theme_figures["standby_on"]:
        preview.modules["archgui"].graph_delete_figure(
            graph=preview.graph_theme_standby_on,
            figure=preview.theme_figures["standby_on"][figure])

    if "standby_on" in preview.theme_images:
        preview.theme_figures["standby_on"]["button"] = preview.modules["archgui"].graph_draw_image(
            graph=preview.graph_theme_standby_on,
            location=(10, 10),
            image=preview.theme_images["standby_on"]
        )
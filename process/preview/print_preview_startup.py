def print_preview_startup(preview):

    for figure in preview.theme_figures["startup"]:
        preview.modules["archgui"].graph_delete_figure(
            graph=preview.graph_theme_startup,
            figure=preview.theme_figures["startup"][figure])

    if "logo" in preview.theme_images:
        preview.theme_figures["startup"]["logo"] = preview.modules["archgui"].graph_draw_image(
            graph=preview.graph_theme_startup,
            location=(10, 10),
            image=preview.theme_images["logo"]
        )
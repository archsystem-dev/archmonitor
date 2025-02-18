def print_preview_cooling(preview):

    for figure in preview.cooling_figures["dynamic"]["silent"]:
        preview.modules["archgui"].graph_delete_figure(
            graph=preview.graph_cooling_silent,
            figure=preview.cooling_figures["dynamic"]["silent"][figure])

    for figure in preview.cooling_figures["dynamic"]["performance"]:
        preview.modules["archgui"].graph_delete_figure(
            graph=preview.graph_cooling_performance,
            figure=preview.cooling_figures["dynamic"]["performance"][figure])

    x = 120 + 2
    y = 340

    x_df = 50
    y_df = 28

    x_aj = 30

    y_aj = {
        "cpu": 11,
        "gpu": 14,
        "case": 17,
        "pump_1": 12,
        "pump_2": 15
    }

    color = {
        "cpu": "red",
        "gpu": "yellow",
        "case": "green",
        "pump_1": "violet",
        "pump_2": "cyan"
    }

    for i in ["silent", "performance"]:
        for j in ["cpu", "gpu", "case", "pump_1", "pump_2"]:
            if j in ["pump_1", "pump_2"]:

                point_from_x = x
                point_from_y = y - ((preview.cooling[i][j]["pwm"] / 10) * y_df) + y_aj[j]

                point_to_x = x + (12 * x_df) - x_aj
                point_to_y = y - ((preview.cooling[i][j]["pwm"] / 10) * y_df) + y_aj[j]

                fn = i + "_" + j
                if i == "silent":
                    preview.cooling_figures["dynamic"][i][fn] = preview.modules["archgui"].graph_draw_line(
                        graph=preview.graph_cooling_silent,
                        point_from=(point_from_x, point_from_y),
                        point_to=(point_to_x, point_to_y),
                        color=color[j],
                        width=2
                    )
                if i == "performance":
                    preview.cooling_figures["dynamic"][i][fn] = preview.modules["archgui"].graph_draw_line(
                        graph=preview.graph_cooling_performance,
                        point_from=(point_from_x, point_from_y),
                        point_to=(point_to_x, point_to_y),
                        color=color[j],
                        width=2
                    )

            else:

                point_from_x = x
                point_from_y = y - ((preview.cooling[i][j]["pwm_min"] / 10) * y_df) + y_aj[j]

                point_to_x = x + ((preview.cooling[i][j]["temp_base"] / 5) * x_df) - x_aj
                point_to_y = y - ((preview.cooling[i][j]["pwm_min"] / 10) * y_df) + y_aj[j]

                fn = i + "_" + j + "_1"
                if i == "silent":
                    preview.cooling_figures["dynamic"][i][fn] = preview.modules["archgui"].graph_draw_line(
                        graph=preview.graph_cooling_silent,
                        point_from=(point_from_x, point_from_y),
                        point_to=(point_to_x, point_to_y),
                        color=color[j],
                        width=2
                    )
                if i == "performance":
                    preview.cooling_figures["dynamic"][i][fn] = preview.modules["archgui"].graph_draw_line(
                        graph=preview.graph_cooling_performance,
                        point_from=(point_from_x, point_from_y),
                        point_to=(point_to_x, point_to_y),
                        color=color[j],
                        width=2
                    )

                point_from_x = point_to_x
                point_from_y = point_to_y

                point_to_x = x + ((preview.cooling[i][j]["temp_max"] / 5) * x_df) - x_aj
                point_to_y = y - ((preview.cooling[i][j]["pwm_max"] / 10) * y_df) + y_aj[j]

                fn = i + "_" + j + "_2"
                if i == "silent":
                    preview.cooling_figures["dynamic"][i][fn] = preview.modules["archgui"].graph_draw_line(
                        graph=preview.graph_cooling_silent,
                        point_from=(point_from_x, point_from_y),
                        point_to=(point_to_x, point_to_y),
                        color=color[j],
                        width=2
                    )
                if i == "performance":
                    preview.cooling_figures["dynamic"][i][fn] = preview.modules["archgui"].graph_draw_line(
                        graph=preview.graph_cooling_performance,
                        point_from=(point_from_x, point_from_y),
                        point_to=(point_to_x, point_to_y),
                        color=color[j],
                        width=2
                    )

                point_from_x = point_to_x
                point_from_y = point_to_y

                point_to_x = x + (12 * x_df) - x_aj
                point_to_y = point_to_y

                fn = i + "_" + j + "_3"
                if i == "silent":
                    preview.cooling_figures["dynamic"][i][fn] = preview.modules["archgui"].graph_draw_line(
                        graph=preview.graph_cooling_silent,
                        point_from=(point_from_x, point_from_y),
                        point_to=(point_to_x, point_to_y),
                        color=color[j],
                        width=2
                    )
                if i == "performance":
                    preview.cooling_figures["dynamic"][i][fn] = preview.modules["archgui"].graph_draw_line(
                        graph=preview.graph_cooling_performance,
                        point_from=(point_from_x, point_from_y),
                        point_to=(point_to_x, point_to_y),
                        color=color[j],
                        width=2
                    )
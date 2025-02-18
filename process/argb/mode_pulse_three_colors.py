import time

def mode_pulse_three_colors(argb):
    color = None
    phase_it_down = [0, 2, 4]
    phase_it_up = [1, 3, 5]

    if argb.phase in [1, 3, 5]:

        if argb.phase == 1:
            color = argb.compute_color("color_2")
        if argb.phase == 3:
            color = argb.compute_color("color_3")
        if argb.phase == 5:
            color = argb.compute_color("color_1")

        if argb.sequence == 0:
            argb.dif_tr = (max(color[0], argb.tr) - min(color[0], argb.tr)) / (100 - argb.intensity_min)
            argb.dif_tg = (max(color[1], argb.tg) - min(color[1], argb.tg)) / (100 - argb.intensity_min)
            argb.dif_tb = (max(color[2], argb.tb) - min(color[2], argb.tb)) / (100 - argb.intensity_min)

        if color[0] > argb.tr:
            argb.tr += argb.dif_tr
        elif color[0] < argb.tr:
            argb.tr -= argb.dif_tr

        if color[1] > argb.tg:
            argb.tg += argb.dif_tg
        elif color[1] < argb.tg:
            argb.tg -= argb.dif_tg

        if color[2] > argb.tb:
            argb.tb += argb.dif_tb
        elif color[2] < argb.tb:
            argb.tb -= argb.dif_tb

        if argb.sequence == argb.intensity_min - 1:
            argb.tr = color[0]
            argb.tg = color[1]
            argb.tb = color[2]

    argb.update_leds()

    # Augmentation ou baisse de l'intensité
    if argb.phase in phase_it_up:
        argb.it += 1

    if argb.phase in phase_it_down:
        argb.it -= 1

    # Transition de phase
    if argb.it == 100 or argb.it == argb.intensity_min:
        argb.sequence = 0
        if argb.phase < 5:
            argb.phase += 1
        else:
            argb.phase = 0
    else:
        argb.sequence += 1

    # Gestion du timing des transitions
    time.sleep(1 / (argb.argb[argb.argb_in_running]["speed"] * 10))
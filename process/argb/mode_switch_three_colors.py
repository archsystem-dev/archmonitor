import time

def mode_switch_three_colors(argb):
    color = None

    if argb.phase == 0:
        color = argb.compute_color("color_2")
    if argb.phase == 1:
        color = argb.compute_color("color_3")
    if argb.phase == 2:
        color = argb.compute_color("color_1")

    if argb.sequence == 0:
        argb.dif_tr = (max(color[0], argb.tr) - min(color[0], argb.tr)) / ((100 - argb.speed) * 10)
        argb.dif_tg = (max(color[1], argb.tg) - min(color[1], argb.tg)) / ((100 - argb.speed) * 10)
        argb.dif_tb = (max(color[2], argb.tb) - min(color[2], argb.tb)) / ((100 - argb.speed) * 10)

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

    if argb.sequence == ((100 - argb.speed) * 10):
        argb.tr = color[0]
        argb.tg = color[1]
        argb.tb = color[2]

    argb.update_leds()

    # Transition de phase
    if argb.sequence == ((100 - argb.speed) * 10):
        argb.sequence = 0
        if argb.phase < 2:
            argb.phase += 1
        else:
            argb.phase = 0

    else:
        argb.sequence += 1

    # Gestion du timing des transitions
    time.sleep(1 / (argb.argb[argb.argb_in_running]["speed"] * 10))

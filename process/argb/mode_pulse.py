import time

def mode_pulse(argb):
    """
    Gère une seule couleur avec une variation progressive d’intensité.
    """

    phase_it_down = [0]
    phase_it_up = [1]

    argb.tr, argb.tg, argb.tb = argb.compute_color("color_1")

    argb.update_leds()

    # Augmentation ou baisse de l'intensité
    if argb.phase in phase_it_up:
        argb.it += 1

    if argb.phase in phase_it_down:
        argb.it -= 1

    # Transition de phase
    if argb.it == 100 or argb.it == argb.intensity_min:
        argb.sequence = 0
        if argb.phase == 0:
            argb.phase = 1
        else:
            argb.phase = 0
    else:
        argb.sequence += 1

    # Gestion du timing des mises à jour
    time.sleep(1 / (argb.argb[argb.argb_in_running]["speed"] * 10))
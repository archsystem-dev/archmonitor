import time

def fixe(argb):
    """
    Affiche une seule couleur fixe sans variation.
    """
    argb.tr, argb.tg, argb.tb = argb.compute_color("color_1")
    argb.update_leds()

    # Gestion du timing des mises à jour
    time.sleep(1 / (argb.argb[argb.argb_in_running]["speed"] * 10))
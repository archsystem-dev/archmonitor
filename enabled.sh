#!/bin/bash

# Sauvegarde du répertoire HOME de l'utilisateur initial
USER_HOME=$(eval echo ~$(logname))

# Vérifie si le script est exécuté en tant que root, sinon relance avec sudo
if [ "$(id -u)" -ne 0 ]; then
    echo "[INFO] Connexion en tant que root requise. Relancement avec sudo..."
    exec sudo HOME="$USER_HOME" bash "$0" "$@"
fi

# 1. Rétablissement du comportement du démarrage
echo "Rétablissement du comportement du démarrage..."
raspi-config nonint do_boot_behaviour B2

echo "Le comportement du démarrage a été rétabli."

# 2. Décommenter la ligne contenant 'bash startx.sh' dans le fichier .bashrc de l'utilisateur courant
BASHRC_FILE="$USER_HOME/.bashrc"

# Vérifier si le bloc commenté existe avant de le décommenter
if grep -qE '^\s*#\s*if \[\[ "\$\(\tty\)" == "/dev/tty1" \]\]; then' "$BASHRC_FILE" && \
   grep -qE '^\s*#\s*bash startx.sh' "$BASHRC_FILE" && \
   grep -qE '^\s*#\s*fi' "$BASHRC_FILE"; then

    # Décommenter chaque ligne correspondante
    sed -i 's|^\s*#\s*\(if \[\[ "$(tty)" == "/dev/tty1" \]\]; then\)|\1|' "$BASHRC_FILE"
    sed -i 's|^\s*#\s*\(bash startx.sh\)|\1|' "$BASHRC_FILE"
    sed -i 's|^\s*#\s*\(fi\)|\1|' "$BASHRC_FILE"

    echo "[INFO] Bloc 'startx.sh' décommenté avec succès dans $BASHRC_FILE."
else
    echo "[WARN] Bloc commenté 'startx.sh' introuvable dans $BASHRC_FILE."
fi

# 3. Restaurer le fichier de configuration Xorg
MONITOR_CONFIG="/etc/X11/xorg.conf.d/10-monitor.conf"
if [ -f "$MONITOR_CONFIG.old" ]; then
    echo "Restauration du fichier $MONITOR_CONFIG..."
    mv "$MONITOR_CONFIG.old" "$MONITOR_CONFIG"
    echo "Fichier restauré en 10-monitor.conf."
else
    echo "Fichier $MONITOR_CONFIG.old non trouvé, aucune action requise."
fi

echo "Script d'annulation terminé avec succès."

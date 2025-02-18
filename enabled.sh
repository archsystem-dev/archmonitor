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
LINE='^[[:space:]]*# [[:space:]]*if \[\[ "\$(tty)" == "\/dev\/tty1" \]\]; then bash startx.sh; fi$'

# On retire le préfixe "# " (ainsi que les éventuels espaces) du début de la ligne.
sed -i.bak "/$LINE/ s/^[[:space:]]*# [[:space:]]*//" "$BASHRC_FILE"

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

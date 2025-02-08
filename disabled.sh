#!/bin/bash

# Sauvegarde du répertoire HOME de l'utilisateur initial
USER_HOME=$(eval echo ~$(logname))

# Vérifie si le script est exécuté en tant que root, sinon relance avec sudo
if [ "$(id -u)" -ne 0 ]; then
    echo "[INFO] Connexion en tant que root requise. Relancement avec sudo..."
    exec sudo HOME="$USER_HOME" bash "$0" "$@"
fi

# 1. Modification du comportement du démarrage
echo "Configuration du comportement au démarrage..."
sudo raspi-config nonint do_boot_behaviour B4

echo "Le comportement du démarrage a été mis à jour."

# 2. Commenter la ligne contenant 'bash startx.sh' dans le fichier .bashrc de l'utilisateur courant
BASHRC_FILE="$USER_HOME/.bashrc"

# Vérifier si le bloc existe avant de le commenter
if grep -qE '^\s*if \[\[ "\$\(\tty\)" == "/dev/tty1" \]\]; then' "$BASHRC_FILE" && \
   grep -qE '^\s*bash startx.sh' "$BASHRC_FILE" && \
   grep -qE '^\s*fi' "$BASHRC_FILE"; then

    # Ajouter un `#` au début des lignes correspondantes
    sed -i 's|^\(\s*if \[\[ "$(tty)" == "/dev/tty1" \]\]; then\)|# \1|' "$BASHRC_FILE"
    sed -i 's|^\(\s*bash startx.sh\)|# \1|' "$BASHRC_FILE"
    sed -i 's|^\(\s*fi\)|# \1|' "$BASHRC_FILE"

    echo "[INFO] Bloc 'startx.sh' commenté avec succès dans $BASHRC_FILE."
else
    echo "[WARN] Bloc 'startx.sh' introuvable dans $BASHRC_FILE."
fi

# 3. Renommage du fichier de configuration Xorg
MONITOR_CONFIG="/etc/X11/xorg.conf.d/10-monitor.conf"
if [ -f "$MONITOR_CONFIG" ]; then
    echo "Ajout de l'extension .old au fichier $MONITOR_CONFIG..."
    mv "$MONITOR_CONFIG" "$MONITOR_CONFIG.old"
    echo "Fichier renommé en 10-monitor.conf.old."
else
    echo "Fichier $MONITOR_CONFIG non trouvé, aucune action requise."
fi

echo "Script terminé avec succès."

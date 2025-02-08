#!/bin/bash

# Sauvegarde du répertoire HOME de l'utilisateur initial
USER_HOME=$(eval echo ~$(logname))

# Définition du répertoire du script
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Définition des fichiers système et utilisateur
CMDLINE_FILE="/boot/firmware/cmdline.txt"
CONFIG_FILE="/boot/firmware/config.txt"

BASHRC_FILE="$USER_HOME/.bashrc"
STARTX_FILE="$USER_HOME/startx.sh"
XINITRC_FILE="$USER_HOME/.xinitrc"

# Vérifie si le script est exécuté en tant que root, sinon relance avec sudo
if [ "$(id -u)" -ne 0 ]; then
    echo "[INFO] Connexion en tant que root requise. Relancement avec sudo..."
    exec sudo HOME="$USER_HOME" bash "$0" "$@"
fi

# Mise à jour du firmware (Raspberry Pi)
echo "[INFO] Mise à jour du firmware..."
rpi-update

# Modification de cmdline.txt pour ajouter des options spécifiques
echo "[INFO] Vérification et mise à jour de $CMDLINE_FILE..."
if ! grep -q "consoleblank=0 spidev.bufsiz=250000" "$CMDLINE_FILE"; then
    echo "[INFO] Ajout de 'consoleblank=0 spidev.bufsiz=250000' à $CMDLINE_FILE"
    echo -n " consoleblank=0 spidev.bufsiz=250000" >> "$CMDLINE_FILE"
else
    echo "[OK] Paramètres déjà présents dans $CMDLINE_FILE"
fi

# Activation de SPI et I2C dans config.txt
echo "[INFO] Vérification et activation des interfaces SPI et I2C..."
for PARAM in "spi=on" "i2c_arm=on"; do
    if grep -q "^dtparam=$PARAM" "$CONFIG_FILE"; then
        echo "[OK] dtparam=$PARAM déjà activé dans $CONFIG_FILE"
    elif grep -q "^#dtparam=$PARAM" "$CONFIG_FILE"; then
        echo "[INFO] Activation de $PARAM dans $CONFIG_FILE"
        sed -i "s/^#dtparam=$PARAM/dtparam=$PARAM/" "$CONFIG_FILE"
    else
        echo "[INFO] Ajout de 'dtparam=$PARAM' à $CONFIG_FILE"
        echo "dtparam=$PARAM" >> "$CONFIG_FILE"
    fi
done

# Ajout de configurations supplémentaires à config.txt
echo "[INFO] Ajout des configurations supplémentaires à $CONFIG_FILE..."
CONFIG_LINES=(
    "dtoverlay=w1-gpio,gpiopin=4,disable-bt"
    "display_auto_detect=1"
    "force_turbo=1\ncore_freq=500\ncore_freq_min=500"
    "hdmi_cvt=800 480 60 3 0 0 0\nhdmi_group=1\nhdmi_mode=14\nhdmi_boost=7"
    "framebufferheight=480\nframebufferwidth=800"
)
for LINE in "${CONFIG_LINES[@]}"; do
    if ! grep -q "$LINE" "$CONFIG_FILE"; then
        echo "[INFO] Ajout de '$LINE' à $CONFIG_FILE"
        echo -e "$LINE" >> "$CONFIG_FILE"
    fi
done

# Installation des paquets requis
echo "[INFO] Mise à jour des paquets et installation des dépendances..."
apt-get update
apt-get upgrade
apt-get install -y pigpio python3-pigpio xserver-xorg xinit
apt-get autoremove

sudo pip install --break-system-packages FreeSimpleGUI pynput screeninfo gpiozero
sudo pip install --break-system-packages adafruit-circuitpython-pca9685

# Création des fichiers de configuration X11
echo "[INFO] Configuration des fichiers X11..."
mkdir -p /etc/X11/xorg.conf.d/
cat <<EOL > /etc/X11/xorg.conf.d/10-blanking.conf
Section "Extensions"
    Option      "DPMS" "Disable"
EndSection

Section "ServerLayout"
    Identifier "ServerLayout0"
    Option "StandbyTime" "0"
    Option "SuspendTime" "0"
    Option "OffTime"     "0"
    Option "BlankTime"   "0"
EndSection
EOL

cat <<EOL > /etc/X11/xorg.conf.d/10-monitor.conf
Section "Monitor"
    Identifier "XWAYLAND0"
    Modeline "800x480_60.00"   29.50  800 824 896 992  480 483 493 500 -hsync +vsync
    Option "PreferredMode" "800x480_60.00"
EndSection

Section "Screen"
    Identifier "HDMI-A-1"
    Monitor "XWAYLAND0"
    DefaultDepth 24
    SubSection "Display"
        Modes "800x480_60.00"
    EndSubSection
EndSection
EOL

# Vérification et création des fichiers utilisateur si nécessaire
echo "[INFO] Vérification et création des fichiers utilisateur..."
for FILE in "$BASHRC_FILE" "$STARTX_FILE" "$XINITRC_FILE"; do
    if [ ! -f "$FILE" ]; then
        echo "[INFO] Création du fichier $FILE"
        touch "$FILE"
    else
        echo "[OK] Le fichier $FILE existe déjà"
    fi
done

echo "[INFO] Vérification et ajout de startx.sh à .bashrc si nécessaire..."

# Définition du bloc à ajouter
BLOCK='if [[ "$(tty)" == "/dev/tty1" ]]; then
    bash startx.sh
fi'

# Vérifier si le bloc est déjà présent dans .bashrc
if ! awk '/if \[\[ "\$\(tty\)" == "\/dev\/tty1" \]\]; then/,/fi/' "$BASHRC_FILE" | grep -q "bash startx.sh"; then
    echo -e "\n$BLOCK" >> "$BASHRC_FILE"
    echo "[INFO] Ajout de startx.sh dans .bashrc terminé."
else
    echo "[OK] Lancement de startx.sh déjà configuré dans .bashrc."
fi

# Création des fichiers startx.sh et .xinitrc
echo "[INFO] Configuration des scripts de démarrage X11..."
cat <<EOL > "$STARTX_FILE"
cd $USER_HOME/archmonitor
startx
EOL
chmod +x "$STARTX_FILE"

cat <<EOL > "$XINITRC_FILE"
exec python $USER_HOME/archmonitor/archmonitor/main.py
EOL
chmod +x "$XINITRC_FILE"

# Activation des services nécessaires
echo "[INFO] Activation et démarrage du service pigpiod..."
systemctl enable pigpiod
systemctl start pigpiod

#  Activation de Wayland
echo "[INFO] Sélection de X11..."
sudo raspi-config nonint do_wayland W1

#  Activation du protocole 1-Wire
echo "[INFO] Activation du 1-Wire..."
sudo raspi-config nonint do_onewire 0

#  Activation de l'I2C
echo "[INFO] Activation du I2C..."
sudo raspi-config nonint do_i2c 0

#  Configuration du comportement au démarrage
echo "[INFO] Activation du démarrage en console autologin..."
sudo raspi-config nonint do_boot_behaviour B2

# Fichier de configuration des alias
ALIAS_FILE="$HOME/.bashrc"

# Vérification de l'existence du fichier des alias
if [ ! -f "$ALIAS_FILE" ]; then
    touch "$ALIAS_FILE"
fi

# Suppression des anciens alias s'ils existent
sed -i '/alias am-enabled=/d' "$ALIAS_FILE"
sed -i '/alias am-disabled=/d' "$ALIAS_FILE"
sed -i '/alias am-start=/d' "$ALIAS_FILE"
sed -i '/alias am-config=/d' "$ALIAS_FILE"
sed -i '/alias am-sensors=/d' "$ALIAS_FILE"


echo "alias am-enabled=\"bash /${SCRIPT_DIR}/enabled.sh\""

# Ajout des nouveaux alias au fichier
{
    echo "alias am-enabled=\"bash ${SCRIPT_DIR}/enabled.sh\""
    echo "alias am-disabled=\"bash ${SCRIPT_DIR}/disabled.sh\""
    echo "alias am-start=\"python ${SCRIPT_DIR}/main.py\""
    echo "alias am-start-test=\"python ${SCRIPT_DIR}/main.py -t\""
    echo "alias am-config=\"python ${SCRIPT_DIR}/configuration.py\""
    echo "alias am-config-test=\"python ${SCRIPT_DIR}/configuration.py -t\""
    echo "alias am-sensors=\"python ${SCRIPT_DIR}/sensors.py\""
} >> "$ALIAS_FILE"

# Rechargement du fichier des alias
source $ALIAS_FILE

echo ""
echo "[INFO] Configuration terminée. Redémarrage recommandé."
echo "[INFO] Au prochain redémarre ArchMonitor se lancera automatiquement."
echo "[INFO] Commandes: "
echo "       - am-enabled      : Activer ArchMonitor"
echo "       - am-disabled     : Désactiver ArchMonitor"
echo "       - am-start        : Lancer ArchMonitor"
echo "       - am-start-test   : Lancer ArchMonitor en mode test"
echo "       - am-config       : Lancer le configurateur de ArchMonitor"
echo "       - am-config-test  : Lancer le configurateur de ArchMonitor"
echo "       - am-sensors      : Lancer la détection des sondes"
echo ""

bash disabled.sh

# Demander à l'utilisateur s'il veut activer ArchMonitor
read -p "Voulez-vous activer ArchMonitor après le future redémarrage ? (y/N) " response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "[INFO] Activation en cours..."
    bash enabled.sh
else
    echo "[INFO] Activation annulée."
fi

# Vérification finale avant redémarrage
read -p "Voulez-vous redémarrer maintenant ? (y/N) : " REBOOT
if [[ "$REBOOT" =~ ^[Yy]$ ]]; then
    echo "[INFO] Redémarrage en cours..."
    sudo reboot
else
    echo "[INFO] Redémarrage annulé. Pensez à redémarrer manuellement pour appliquer les changements."
fi

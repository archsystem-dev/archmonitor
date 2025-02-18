
![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/logo-watercooling_monitor.png)

Archmonitor est un module de gestion autonome de refroidissement liquide et de contrôle par écran tactile. 
Cette version v2 beta fonctionne sur un `Raspberry PI 4B` et prend en charge la configuration suivante :

- Deux sondes pour la température de liquide
- Une sonde pour le boitier
- Deux pompes indépendantes
- Trois circuits indépendants de cinq ventilateurs
- Un circuit global `ARGB2`
- Démarrage de l’ordinateur via l’écran tactile

Les configurations possibles sous cette version sont de :

- Deux modes de refroidissement configurable par l’écran tactile
- Six modes configurables pour le circuit `ARGB2` configurable par l’écran tactile
- Un programme de configuration

Le logiciel Archmonitor est basé sur la surcouche `archgui` elle-même basé sur `FreeSimpleGUI`. 
Ce programme fonctionne sur un `Raspberry PI 4B` avec le dernier `Raspberry Pi OS 64Bits` comme OS.<br/>

## 😊 Fonctions à venir :

- Ajout des logs dans le programme de configuration
- Gestion de deux circuits ARGB2
- Ajout d'un second écran tactile
- Intégration d'un contrôle et configuration par bluetooth

<br/>

| Boitier fermé                                                                                                           | Boitier ouvert                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/case_close.png)   | ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/case_open.png)   |
| <b>Affichage sur écran tactile</b>                                                                                      | <b>Impression 3D</b>                                                                                                   |
| ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/touch_screen.png) | ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/case_schema.png) |
| <b>Config. Theme</b>                                                                                                    | <b>Config. ARGB</b>                                                                                                    |
| ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/theme.png)        | ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/argb.png)        |
| <b>Config. Cooling</b>                                                                                                  | <b>Config. GPIO</b>                                                                                                    |
| ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/cooling.png)      | ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/gpio.png)        |

<br/>


## 😊 Principe de fonctionnement :

### Les alimentations :

Le Raspberry PI est alimenté par un `USB3.2 GEN2` interne de la carte mère.
Il faut veiller à ce que les ports USB reste alimenté après l’arrêt de l’ordinateur, voir dans le BIOS pour paramétrer 
cela si ce n’est pas d’usine.<br/>

Le ventilateur du module est alimenté et contrôlé par le PCA9685 lui-même alimenté par l’`USB3.2 GEN2` d'alimentation.
Attention, le ventilateur utilisé est un 12v, j'utilise un booster de tension ç amener les 5v à 12v.

Les pompes et les groupes de ventilateurs sont alimenté via le 12V du SATA Power.

Le circuit ARGB2 est alimenté via l’`USB3.2 GEN2` d'alimentation, le circuit ARGB2 reste donc alimenté une fois l’ordinateur éteint.
Le mode `standby` est configurable, il peut donc etre éteint complétement ou garder une configuration lumineuse choisie.

### Le fonctionnement :

Le Raspberry PI et l’écran restent toujours alimenté. L’écran peut donc piloter l’Archmonitor avec l'ordinateur éteint pour gérer le circuit ARGB2 et démarré l'ordinateur.
Une fois l’ordinateur allumé, le Raspberry PI contrôle les signaux PWM des différentes pompes et HUBs de ventilateurs par rapport aux paramètres donnés.

<br/>

## 🛠️ Lien externe :

- [`Raspberry Pi OS`](https://www.raspberrypi.com/software/)
- [`Tci`](https://www.raspberrypi.com/software/)

<br/>

## 🛠️ Matériel manufacturé :


| Pièces                  | Aperçu                                                                                                                      | Achat                                           |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| 1x Raspberry PI 4B      | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/RPI4B.png)            | [`Lien Amazon`](https://www.amazon.fr/dp/B09TTNF8BT) |
| 1x Dissipateur          | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/heat_sink.png)       | [`Lien Amazon`](https://www.amazon.fr/dp/B08N617L1J) |
| 1x PAD Cuivre 1.5mm     | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/pad_cuivre.png)      | [`Lien Amazon`](https://www.amazon.fr/dp/B07G73J1T8) |
| 1x Ventilateur 120mm    | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/120mm.png)           | [`Lien Amazon`](https://www.amazon.fr/dp/B09RWTCXRR) |
| 1x Contrôleur PCA9685   | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/PCA9685.png)         | [`Lien Amazon`](https://www.amazon.fr/dp/B072N8G7Y9) |
| 1x Boosteur 5v-12v      | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/boosteur_5v_12v.png) | [`Lien Amazon`](https://www.amazon.fr/dp/B0CW9P4CQP) |
| 3x Sonde DS18B20        | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/DS18B20.png)         | [`Lien Amazon`](https://www.amazon.fr/dp/B075FYYLLV) |
| 3x HUBS FAN 4 PINS      | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/hub_fan.png)         | [`Lien Amazon`](https://www.amazon.fr/dp/B08XWWXBYD) |
| 2x Cables FAN 4 PINS    | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/cable_4_pins.png)    | [`Lien Amazon`](https://www.amazon.fr/dp/B01N1Z3FYD) |
| 1x HUB ARGB2 + Cable    | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/hub_argb2_cable.png) | [`Lien Amazon`](https://www.amazon.fr/dp/B0D2SMNKZY) |
| 1x Écran 800x480        | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/screen_800x480.png)  | [`Lien Amazon`](https://www.amazon.fr/dp/B096ZSZFC8) |
| 1x Cable Micro HDMI     | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/cable_microHDMI.png) | [`Lien Amazon`](https://www.amazon.fr/dp/B09J4HMP25) |
| 1x Cable USB 3.2        | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/USB3.2.png)          | [`Lien Amazon`](https://www.amazon.fr/dp/B0BWHZBPGJ) |
| 2x Cable USB-A Mini-B   | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/usbaminib.png)       | [`Lien Amazon`](https://www.amazon.fr/dp/B089F9V5GK) |
| 1x Cable extension SATA | [`Apercu`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/amazon/sata_power.png)      | [`Lien Amazon`](https://www.amazon.fr/dp/B07C71J8LL) |

<br/>
⚠️ Les liens vers Amazon sont le matériel que j’ai utilisé, c’est simplement indicatif.<br/>

## 🛠️ PCB à faire fabriquer et souder :

| Pièces      | Coupler                                                                                                                        | Power                                                                                                                      |
|-------------|--------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| Apercu      | ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/coupler.png)             | ![Image](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/power.png)           |
| Fichier Tci | [`Coupler.Tci`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/tci/coupler.zip)          | [`Power.Tci`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/tci/power.zip)          |
| Soudure     | [`Coupler.png`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/coupler_weld.png) | [`Power.png`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/picture/power_weld.png) |

<br/>

## 🛠️ Impression 3D :

| Pièces                  | Fichiers PDF                                                                                                                          | Fichier STL                                                                                                                           |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Case                    | [`Case.pdf`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/pdf/case.pdf)                       | [`Case.zip`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/stl/case.zip)                       |
| Cover                   | [`Cover.pdf`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/pdf/cover.pdf)                     | [`Cover.zip`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/stl/cover.zip)                     |
| Fixation Cables         | [`Fixation_cables.pdf`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/pdf/fixation_cables.pdf) | [`Fixation_cables.zip`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/stl/fixation_cables.zip) |
| Port RPI 4B             | [`Port_rpi_4b.pdf`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/pdf/port_rpi_4b.pdf)         | [`Port_rpi_4b.zip`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/stl/port_rpi_4b.zip)         |

<br/>

## 🛠️ Câblage :

| Circuit | Fichiers                                                                                                                          |
|---------|-----------------------------------------------------------------------------------------------------------------------------------|
| Général | [`Plan général de cablage`](https://raw.githubusercontent.com/archsystem-dev/archmonitor-support/refs/heads/main/pdf/cabalge_general.pdf) |

<br/>

## 💻️ Installation :
 - Configuration de l’installation via `Raspberry PI Imager` sur Ubuntu ou une autre distribution
 - Installation de `Raspberry Pi OS 64Bits` sur la carte SD
 - Démarrage du PI

```bash
sudo apt-get install git
git clone https://github.com/archsystem-dev/archmonitor/ archmonitor
sudo cd archmonitor
sudo bash install.sh
```

<br/>

## 💻️ Les commandes :

```bash
# Configuration du démarrage pour l'utilisation de l'écran tactile
# A ne faire qu'après configuration
am-enabled
# Configuration du démarrage pour d'un écran normal avec interface graphique du PI
am-disabled
# Lancement de l'archmonitor
am-start
# Lancement de l'archmonitor en mode test
am-start-test
# Lancement du programme de configuration
am-config
# Lancement du programme de configuration en mode test
am-config-test
# Lancement du programme de détection des soudes
am-sensors
```

<br/>

## 💻️ Configuration :

### Premièrement lancez le programme de détection des sondes :  

```bash
am-sensors
```

### Deuxiemement lancez le programme de configuration :

```bash
am-config
```

À partir de ce programme, vous pourrez :
- Configurer vos courbes de refroidissement
- Configurer vos mode ARGB
- Créer votre propre thème
- Configurer les ports du GPIO si le câblage différent


### Troisièmement, lancez le programme en mode test :

```bash
am-start-test
```

### Quatrièmement, activez et redémarrez:

```bash
am-enabled
reboot
```


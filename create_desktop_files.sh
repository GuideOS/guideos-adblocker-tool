#!/bin/bash

# Sicherstellen, dass die Verzeichnisse existieren
mkdir -p debian/guideos-adblocker-tool/usr/share/applications
#mkdir -p debian/guideos-ticket-tool/etc/xdg/autostart

# Erstellen der ersten .desktop-Datei
cat > debian/guideos-adblocker-tool/usr/share/applications/guideos-adblocker-tool.desktop <<EOL
[Desktop Entry]
Version=1.0
Name=GuideOS Adblocker
Comment=Adblocker Tool für GuideOS
Exec=guideos-adblocker-tool
Icon=guideos-adblocker-tool
Terminal=false
Type=Application
Categories=GuideOS;
StartupNotify=true
EOL
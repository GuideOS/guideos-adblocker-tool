
# GuideOS Adblocker - GTK4 Version

<div align="center">
  <img src="https://img.shields.io/badge/Version-2.11-blue.svg" alt="Version 2.11">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/GTK-4.0-orange.svg" alt="GTK 4.0">
  <img src="https://img.shields.io/badge/libadwaita-1.0-purple.svg" alt="libadwaita 1.0">
  <img src="https://img.shields.io/badge/Platform-Linux-red.svg" alt="Platform Linux">
</div>

<p align="center">
  <b>Systemweite Werbeblockierung durch /etc/hosts Manipulation</b><br>
  Modernes GTK4/libadwaita Interface mit umfangreichen Features
</p>

---

## 📋 Inhaltsverzeichnis

- [Überblick](#-überblick)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Abhängigkeiten](#-abhängigkeiten)
- [Verwendung](#-verwendung)
- [Blocklisten](#-blocklisten)
- [FAQ](#-faq)
- [Entwickler](#-entwickler)
- [Lizenz](#-lizenz)

## 🔍 Überblick

Der GuideOS Adblocker ist ein leistungsstarkes Tool zur systemweiten Werbeblockierung unter Linux. Durch die Manipulation der `/etc/hosts` Datei werden Werbung, Tracker und schädliche Webseiten auf DNS-Ebene blockiert - bevor sie überhaupt geladen werden können.

Das Programm bietet eine benutzerfreundliche GTK4/libadwaita Oberfläche und unterstützt zahlreiche vordefinierte Blocklisten sowie eigene benutzerdefinierte Listen.

## ✨ Features

### 📦 **Umfangreiche Blocklisten**
- **StevenBlack Listen** - Blockiert Pornografie, Social Media, Fake News und Glücksspiel
- **BlocklistProject** - Spezialisierte Listen für Werbung, Tracking, Phishing und Pornografie
- **EasyList** - Internationale und deutsche Werbeblockierung
- **EasyPrivacy** - Schutz vor Tracking und Datensammlern
- **NoCoin** - Blockiert Kryptowährungs-Miner
- **Fanboy's Annoyance** - Entfernt lästige Cookie-Hinweise und Popups

### 🛠 **Erweiterte Funktionen**
- ✅ Vordefinierte Blocklisten aktivieren/deaktivieren
- ✅ Eigene Blocklisten aus dem Internet importieren
- ✅ Einzelne Domains manuell blockieren
- ✅ Automatische Updates beim Programmstart
- ✅ Backup/Wiederherstellung der Original-Hosts
- ✅ Importierte Listen verwalten und löschen
- ✅ DNS-Cache automatisch leeren
- ✅ System-Theme Unterstützung (Hell/Dunkel)

### 🔒 **Sicherheit**
- Sudo-Passwortabfrage beim Start
- Backup der Original-Hosts Datei
- Keine dauerhaften Root-Rechte
- Sichere temporäre Dateien

## 📸 Screenshots

```
[Screenshots folgen in Kürze]
```

## 💻 Installation

### Manuelle Installation

```bash
# Repository klonen
git clone https://github.com/evilware666/guideos-adblocker.git
cd guideos-adblocker

# Python-Skript ausführbar machen
chmod +x adblocker.py

# Starten
./adblocker.py
```

### Als Desktop-Anwendung installieren

```bash
# Skript nach /usr/local/bin kopieren
sudo cp adblocker.py /usr/local/bin/guideos-adblocker
sudo chmod +x /usr/local/bin/guideos-adblocker

# Desktop-Eintrag erstellen
cat > ~/.local/share/applications/guideos-adblocker.desktop << EOF
[Desktop Entry]
Name=GuideOS Adblocker
Comment=Systemweite Werbeblockierung
Exec=/usr/local/bin/guideos-adblocker
Icon=network-server
Terminal=false
Type=Application
Categories=Network;System;
EOF
```

## 📦 Abhängigkeiten

### Python-Pakete
- `PyGObject` (GTK4 Bindings)
- `libadwaita` (Adwaita Widgets)
- `requests` (HTTP-Anfragen)

### Installation der Abhängigkeiten

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-requests
```

**Fedora:**
```bash
sudo dnf install python3-gobject gtk4 libadwaita python3-requests
```

**Arch Linux:**
```bash
sudo pacman -S python-gobject gtk4 libadwaita python-requests
```

## 🎮 Verwendung

### Erster Start
1. Programm starten
2. Administrator-Passwort eingeben
3. Warnung zu vielen Blocklisten bestätigen
4. Hauptfenster erscheint

### Hauptfunktionen

| Button | Funktion |
|--------|----------|
| 📋 Blocklisten verwalten | Vordefinierte Listen aktivieren/deaktivieren |
| 📥 Eigene Blocklisten importieren | Eigene Listen aus dem Internet hinzufügen |
| 🚫 Webseite blockieren | Einzelne Domain manuell sperren |
| 📝 Gesperrte Seiten verwalten | Eigene Einträge ansehen und löschen |
| 🔄 Listen aktualisieren | Alle aktiven Listen updaten |
| ↩️ Alles zurücksetzen | Original-Hosts wiederherstellen |

### Eigene Blocklisten importieren
1. Klick auf "📥 Eigene Blocklisten importieren"
2. Namen und URL der Blockliste eingeben
3. Auf "Liste hinzufügen" klicken
4. Liste in den Blocklisten aktivieren

### Wichtiger Hinweis
> **💡 Nach jeder Änderung: Browser neu starten!**
> Der DNS-Cache wird zwar geleert, aber manche Browser cachen DNS-Einträge zusätzlich.

## 📚 Blocklisten

### Vordefinierte Listen im Detail

| Liste | Beschreibung | Zweck |
|-------|--------------|--------|
| **StevenBlack (Fakenews/Gambling)** | Umfassende Hosts-Liste | Blockiert Pornografie, Social Media, Fake News, Glücksspiel |
| **StevenBlack-Porn** | Spezialisiert | Ausschließlich pornografische Inhalte |
| **BlocklistProject-Porn** | 500.000+ Domains | Sehr umfangreiche Porno-Blockliste |
| **BlocklistProject-Phishing** | Betrugsseiten | Schutz vor Phishing und Identitätsdiebstahl |
| **BlocklistProject-Ads** | Werbenetzwerke | Reduziert Datenverbrauch und Ladezeiten |
| **BlocklistProject-Tracking** | Datenschutz | Blockiert Tracking-Dienste |
| **EasyList Germany** | Deutsche Werbung | Speziell für DE/AT/CH |
| **EasyList** | Internationale Werbung | Für englischsprachige Seiten |
| **EasyPrivacy** | Datenschutz | Tracking-Pixel und Analyse-Tools |
| **NoCoin** | Krypto-Miner | Verhindert CPU-Mining im Browser |
| **Fanboy's Annoyance** | UX-Verbesserung | Cookie-Hinweise, Popups, Social-Buttons |

### Empfohlene Kombinationen

**Für normale Nutzer:**
- EasyList Germany
- EasyPrivacy
- BlocklistProject-Ads

**Für maximalen Datenschutz:**
- EasyPrivacy
- BlocklistProject-Tracking
- NoCoin
- Fanboy's Annoyance

**Für Kindersicherung:**
- StevenBlack (Fakenews/Gambling)
- BlocklistProject-Porn

## ❓ FAQ

### Warum brauche ich Administrator-Rechte?
Das Programm muss die systemweite `/etc/hosts` Datei bearbeiten, was Root-Rechte erfordert.

### Kann das Surfen verlangsamt werden?
Nein, im Gegenteil: Durch das Blockieren von Werbung werden Webseiten oft schneller geladen.

### Was tun bei kaputten Webseiten?
Deaktivieren Sie einzelne Blocklisten oder verwenden Sie die "Alles zurücksetzen" Funktion.

### Wie oft werden die Listen aktualisiert?
Beim Programmstart automatisch oder manuell über den "Listen aktualisieren" Button.

### Funktionieren Browser-Erweiterungen parallel?
Ja, der systemweite Adblocker und Browser-Erweiterungen ergänzen sich hervorragend.

### Wo werden meine eigenen Einträge gespeichert?
In `~/.adblocker_custom` und importierte Listen in `~/.adblocker_user_lists.json`.

## 👨‍💻 Entwickler
evilware666 & Helga


### Mitwirken
Beiträge sind willkommen! Bitte beachten Sie:
1. Fork des Repositories
2. Feature-Branch erstellen
3. Commits mit aussagekräftigen Nachrichten
4. Pull Request einreichen

## 📄 Lizenz

MIT License

Copyright (c) 2024 evilware666 & helga


## ⚠️ Haftungsausschluss

Die Entwickler übernehmen keine Haftung für Schäden, die durch die Nutzung dieses Programms entstehen. Die Blockierung von Webseiten kann zu Fehlfunktionen führen - eine Sicherung der Original-Hosts wird automatisch erstellt.


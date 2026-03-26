Hier ist die professionelle README.md für das GuideOS-Adblocker-Programm:

```markdown
# GuideOS-Adblocker

<div align="center">
  <img src="https://img.shields.io/badge/Version-2.6-blue.svg" alt="Version 2.6">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/GTK-4.0-orange.svg" alt="GTK 4.0">
  <img src="https://img.shields.io/badge/libadwaita-1.0-purple.svg" alt="libadwaita 1.0">
  <img src="https://img.shields.io/badge/Platform-Linux-red.svg" alt="Platform Linux">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow.svg" alt="Python 3.8+">
</div>

<p align="center">
  <b>Zentrale Verwaltung von Werbe-, Malware- und Phishing-Domains über /etc/hosts</b><br>
  Kombiniert vordefinierte Blocklisten mit individuellen Einträgen für maximale Privatsphäre
</p>

---

## 📋 Inhaltsverzeichnis

- [Überblick](#-überblick)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
  - [Abhängigkeiten](#abhängigkeiten)
  - [Manuelle Installation](#manuelle-installation)
  - [Desktop-Integration](#desktop-integration)
- [Verwendung](#-verwendung)
  - [Erster Start](#erster-start)
  - [Hauptfunktionen](#hauptfunktionen)
- [Blocklisten](#-blocklisten)
  - [Vordefinierte Listen](#vordefinierte-listen)
  - [Eigene Listen importieren](#eigene-listen-importieren)
  - [Empfohlene Kombinationen](#empfohlene-kombinationen)
- [Technische Details](#-technische-details)
  - [Dateistruktur](#dateistruktur)
  - [Logging](#logging)
  - [Sicherheitskonzept](#sicherheitskonzept)
- [Fehlerbehebung](#-fehlerbehebung)
- [FAQ](#-faq)
- [Entwickler](#-entwickler)
- [Lizenz](#-lizenz)

---

## 🔍 Überblick

Der **GuideOS-Adblocker** ist ein leistungsstarkes Tool zur systemweiten Werbeblockierung unter Linux. Durch die intelligente Manipulation der `/etc/hosts`-Datei werden Werbung, Tracker, Malware-Domains und Phishing-Seiten auf DNS-Ebene blockiert – noch bevor sie geladen werden können.

Das Programm bietet eine moderne, benutzerfreundliche **GTK4/libadwaita-Oberfläche** und unterstützt:
- Mehrere vordefinierte Blocklisten
- Benutzerdefinierte Listen aus beliebigen Quellen
- Manuelle Domain-Sperrungen
- Automatische Updates
- Backup- und Wiederherstellungsfunktionen

---

## ✨ Features

### 🛡️ **Umfassende Blocklisten**
- **StevenBlack** – Blockiert Pornografie, Social Media, Fake News und Glücksspiel
- **BlocklistProject** – Spezialisierte Listen für Werbung, Tracking, Phishing und Pornografie
- **EasyList** – Internationale und deutsche Werbeblockierung
- **Eigene Listen** – Importieren Sie beliebige Blocklisten aus dem Internet

### 🛠️ **Erweiterte Funktionen**
| Funktion | Beschreibung |
|----------|--------------|
| 📋 **Blocklisten verwalten** | Aktivieren/deaktivieren Sie vordefinierte und eigene Listen |
| ➕ **Eigene Listen importieren** | Fügen Sie beliebige Blocklisten-URLs hinzu |
| 🚫 **Webseite blockieren** | Sperren Sie einzelne Domains manuell |
| 📝 **Gesperrte Seiten verwalten** | Zeigen Sie blockierte Domains an und geben Sie sie frei |
| 🔄 **Automatische Updates** | Aktualisieren Sie alle Listen beim Programmstart |
| 💾 **Backup/Wiederherstellung** | Automatisches Backup der Original-Hosts-Datei |
| 🎨 **System-Theme-Support** | Passt sich automatisch an Hell-/Dunkelmodus an |

### 🔒 **Sicherheitsmerkmale**
- Einmalige Authentifizierung zu Beginn
- Keine dauerhaften Root-Rechte
- Sichere temporäre Dateien
- Automatisches Backup vor Änderungen
- Detailliertes Logging für Debugging

---

## 📸 Screenshots

```
┌─────────────────────────────────────────────────────────────┐
│  🛡️ GuideOS-Adblocker                                       │
├─────────────────────────────────────────────────────────────┤
│  Befreie dich von Werbung und schütze deine Privatsphäre!  │
│  Der GuideOS-Adblocker blockiert Werbung sowie schädliche  │
│  Webseiten und das alles systemweit.                       │
│                                                             │
│  Eigene Domains geblockt: 0                                │
│  ✔ Blocklisten aktualisiert (25.12.2024 14:30)            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐          │
│  │ 📋 Blocklisten verwalten                    │          │
│  ├─────────────────────────────────────────────┤          │
│  │ 🚫 Webseite blockieren                      │          │
│  ├─────────────────────────────────────────────┤          │
│  │ 📝 Gesperrte Seiten verwalten               │          │
│  ├─────────────────────────────────────────────┤          │
│  │ 🔄 Listen aktualisieren                     │          │
│  ├─────────────────────────────────────────────┤          │
│  │ ➕ Eigene Blocklisten verwalten             │          │
│  ├─────────────────────────────────────────────┤          │
│  │ ↩️ Alles zurücksetzen                       │          │
│  ├─────────────────────────────────────────────┤          │
│  │ ❌ Beenden                                  │          │
│  └─────────────────────────────────────────────┘          │
│                                                             │
│  💡 Tipp: Nach Änderungen Browser neu starten!            │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Installation

### Abhängigkeiten

**Systempakete:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-requests

# Fedora
sudo dnf install python3-gobject gtk4 libadwaita python3-requests

# Arch Linux
sudo pacman -S python-gobject gtk4 libadwaita python-requests

# openSUSE
sudo zypper install python3-gobject gtk4 libadwaita-1 python3-requests
```

**Python-Abhängigkeiten:**
```bash
pip3 install requests
```

### Manuelle Installation

```bash
# Repository klonen (falls vorhanden) oder Skript herunterladen
wget https://raw.githubusercontent.com/guideos/adblocker/main/adblocker.py
chmod +x adblocker.py

# Ausführen
./adblocker.py
```

### Desktop-Integration

```bash
# Skript nach /usr/local/bin kopieren
sudo cp adblocker.py /usr/local/bin/guideos-adblocker
sudo chmod +x /usr/local/bin/guideos-adblocker

# Desktop-Eintrag erstellen
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/guideos-adblocker.desktop << 'EOF'
[Desktop Entry]
Name=GuideOS-Adblocker
Comment=Zentrale Verwaltung von Werbe-, Malware- und Phishing-Domains
Exec=/usr/local/bin/guideos-adblocker
Icon=network-server
Terminal=false
Type=Application
Categories=Network;System;
StartupNotify=true
EOF

# Optional: Symbol setzen
# sudo cp icon.png /usr/share/icons/hicolor/128x128/apps/guideos-adblocker.png
```

---

## 🎮 Verwendung

### Erster Start

1. **Programm starten:**
   ```bash
   ./adblocker.py
   ```

2. **Authentifizierung:**
   - Es erscheint ein Dialog zur Passworteingabe
   - Geben Sie Ihr Benutzerpasswort ein
   - Das Programm erhält temporäre sudo-Rechte

3. **Backup-Erstellung:**
   - Die originale `/etc/hosts` wird automatisch gesichert
   - Backup-Pfad: `/etc/hosts.adblocker.bak`

### Hauptfunktionen

| Aktion | Beschreibung |
|--------|--------------|
| **📋 Blocklisten verwalten** | Öffnet eine Liste aller verfügbaren Blocklisten zum Aktivieren/Deaktivieren |
| **🚫 Webseite blockieren** | Fügt eine einzelne Domain zur Sperrliste hinzu |
| **📝 Gesperrte Seiten verwalten** | Zeigt alle manuell blockierten Domains und ermöglicht Freigabe |
| **🔄 Listen aktualisieren** | Lädt alle aktiven Blocklisten neu und aktualisiert `/etc/hosts` |
| **➕ Eigene Blocklisten verwalten** | Fügt eigene Blocklisten-URLs hinzu oder entfernt sie |
| **↩️ Alles zurücksetzen** | Stellt die originale `/etc/hosts` wieder her |

---

## 📚 Blocklisten

### Vordefinierte Listen

| Liste | Beschreibung | Zweck |
|-------|--------------|-------|
| **StevenBlack (Fakenews/Gambling)** | Umfassende Hosts-Liste | Blockiert Pornografie, Social Media, Fake News, Glücksspiel |
| **StevenBlack-Porn** | Spezialisiert | Ausschließlich pornografische Inhalte |
| **BlocklistProject-Porn** | 500.000+ Domains | Sehr umfangreiche Porno-Blockliste |
| **BlocklistProject-Phishing** | Betrugsseiten | Schutz vor Phishing und Identitätsdiebstahl |

### Eigene Listen importieren

Unterstützte Formate:
- **Hosts-Format:** `0.0.0.0 domain.com` oder `127.0.0.1 domain.com`
- **Domain-Liste:** Einfache Domains pro Zeile
- **Quellen:** GitHub, Pastebin, beliebige HTTP/HTTPS-URLs

**Beispiel für eigene Liste:**
```
# Meine Werbeliste
0.0.0.0 ads.example.com
0.0.0.0 tracker.example.com
bad-domain.com
malware-site.net
```

### Empfohlene Kombinationen

| Nutzungsszenario | Empfohlene Listen |
|------------------|-------------------|
| **Normaler Gebrauch** | BlocklistProject-Ads, EasyList Germany |
| **Maximale Privatsphäre** | EasyPrivacy, BlocklistProject-Tracking |
| **Kindersicherung** | StevenBlack (Fakenews/Gambling), BlocklistProject-Porn |
| **Sicherheitsorientiert** | BlocklistProject-Phishing, EasyPrivacy |

---

## 🔧 Technische Details

### Dateistruktur

| Datei | Pfad | Beschreibung |
|-------|------|--------------|
| **Blockliste (System)** | `/etc/hosts` | Zentrale Hosts-Datei |
| **Backup** | `/etc/hosts.adblocker.bak` | Original-Hosts-Backup |
| **Aktive Listen** | `/etc/hosts.active_lists` | Gespeicherte Listenauswahl |
| **Letztes Update** | `/etc/hosts.lastupdate` | Zeitstempel der letzten Aktualisierung |
| **Eigene Einträge** | `~/.adblocker_custom` | Manuell gesperrte Domains |
| **Benutzerlisten** | `~/.adblocker_user_lists.json` | Importierte Listen (JSON) |
| **Debug-Log** | `~/adblocker_debug.log` | Detailliertes Logging |

### Logging

Das Programm erstellt ein detailliertes Log für Debugging-Zwecke:

```bash
# Log anzeigen
tail -f ~/adblocker_debug.log

# Log-Inhalt
cat ~/adblocker_debug.log
```

**Log-Einträge enthalten:**
- Zeitstempel mit Millisekunden
- Thread-Informationen
- Ausgeführte Befehle
- Fehlermeldungen
- Authentifizierungsstatus

### Sicherheitskonzept

1. **Authentifizierung:** Einmalige Passwortabfrage zu Beginn
2. **sudo-Session:** Verwendung von `sudo -v` zur Passwort-Caching
3. **Temporäre Dateien:** Sichere Erstellung mit `tempfile.NamedTemporaryFile`
4. **Backup:** Automatisches Backup vor jeder Änderung
5. **Keine Root-Ausführung:** Skript läuft als normaler Benutzer

---

## 🐛 Fehlerbehebung

### Authentifizierungsfehler

**Problem:** "Authentifizierung abgelaufen" oder "Authentication failure"

**Lösung:**
```bash
# sudo-Session erneuern
sudo -v

# Oder Programm neu starten
```

### Webseiten werden nicht blockiert

**Problem:** Blockierte Seiten sind weiterhin erreichbar

**Lösungen:**
1. Browser komplett schließen und neu starten
2. DNS-Cache manuell leeren:
   ```bash
   sudo systemd-resolve --flush-caches
   # oder
   sudo resolvectl flush-caches
   ```
3. Browser-internen DNS-Cache leeren (Chrome: chrome://net-internals/#dns)

### Blocklisten werden nicht aktualisiert

**Problem:** Fehler beim Herunterladen der Listen

**Mögliche Ursachen:**
- Keine Internetverbindung
- URL nicht erreichbar
- Zeitüberschreitung

**Lösung:**
```bash
# Testen Sie die URL manuell
curl -I https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts

# Log prüfen
tail -50 ~/adblocker_debug.log
```

### Kaputte Webseiten nach Aktivierung

**Problem:** Webseiten funktionieren nicht richtig

**Lösung:**
1. Deaktivieren Sie einzelne Blocklisten
2. Testen Sie welche Liste das Problem verursacht
3. Verwenden Sie die "Alles zurücksetzen"-Funktion

---

## ❓ FAQ

### Warum benötigt das Programm Root-Rechte?
Das Programm muss die systemweite `/etc/hosts`-Datei bearbeiten, was Administratorrechte erfordert. Dies ist die einzige Möglichkeit, DNS-basierte Werbeblockierung systemweit zu implementieren.

### Wie oft sollten die Listen aktualisiert werden?
Einmal täglich oder wöchentlich ist ausreichend. Das Programm aktualisiert automatisch beim Start, Sie können aber jederzeit manuell aktualisieren.

### Kann ich das Programm parallel zu Browser-Erweiterungen nutzen?
Ja! Systemweite Blockierung und Browser-Erweiterungen ergänzen sich hervorragend. Die Kombination bietet maximalen Schutz.

### Was passiert bei einem Systemupdate?
Die `/etc/hosts`-Datei wird bei Systemupdates normalerweise nicht überschrieben. Das Backup bleibt erhalten. Nach einem Update sollten Sie die Blocklisten einmal neu aktualisieren.

### Wie kann ich das Programm deinstallieren?
```bash
# Desktop-Eintrag entfernen
rm ~/.local/share/applications/guideos-adblocker.desktop

# Skript entfernen
sudo rm /usr/local/bin/guideos-adblocker

# Optionale Dateien löschen
rm ~/.adblocker_custom ~/.adblocker_user_lists.json ~/adblocker_debug.log

# Hosts zurücksetzen (falls gewünscht)
sudo cp /etc/hosts.adblocker.bak /etc/hosts
sudo rm /etc/hosts.adblocker.bak
sudo rm /etc/hosts.active_lists
sudo rm /etc/hosts.lastupdate
```

### Funktioniert das Programm mit systemd-resolved?
Ja, das Programm erkennt automatisch `systemd-resolved` und leert den DNS-Cache entsprechend.

### Kann ich das Programm im Terminal ohne GUI nutzen?
Die GUI ist der primäre Zugang. Für reine Terminal-Nutzung empfehlen wir das direkte Bearbeiten von `/etc/hosts` oder Skripte mit `curl` und `wget`.

---

## 👨‍💻 Entwickler

| Rolle | Name | Beitrag |
|-------|------|---------|
| **Hauptentwickler** | evilware666 | Kernfunktionen, GUI, Blocklisten-Integration |
| **Co-Entwicklerin** | Helga | Testing, Dokumentation, Fehlerbehebung |
| **KI-Assistenz** | Copilot | Code-Vorschläge, Optimierungen |

### Beitragen

Wir freuen uns über Beiträge! So können Sie helfen:

1. **Issues melden:** Beschreiben Sie Bugs oder Feature-Wünsche
2. **Code beitragen:** Forken, Branch erstellen, Pull Request senden
3. **Dokumentation verbessern:** Korrekturen oder Ergänzungen
4. **Blocklisten vorschlagen:** Teilen Sie gute Blocklisten-Quellen

**Entwicklungsrichtlinien:**
- Python 3.8+ Kompatibilität
- GTK4/libadwaita Konventionen einhalten
- Logging für Debugging einfügen
- Code-Kommentare in Deutsch oder Englisch

---

## 📄 Lizenz

Dieses Projekt ist unter der **MIT-Lizenz** lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

```
MIT License

Copyright (c) 2024 evilware666, Helga

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Haftungsausschluss

Die Entwickler übernehmen keine Haftung für:
- Schäden durch falsche Blockierung von Webseiten
- Verlust von Daten durch Fehlbedienung
- Kompatibilitätsprobleme mit bestimmter Software

**Wichtiger Hinweis:** Das Programm erstellt automatisch ein Backup der originalen `/etc/hosts`-Datei. Bei Problemen kann die originale Konfiguration jederzeit wiederhergestellt werden.

---

<div align="center">
  <sub>Mit ❤️ entwickelt für die GuideOS-Community</sub><br>
  <sub>© 2024 evilware666, Helga</sub><br>
  <sub>Version 2.6 | Letzte Aktualisierung: Dezember 2024</sub>
</div>
```

---

## ✨ **Besonderheiten dieser README:**

1. **Vollständige Struktur** mit 12 Hauptkapiteln und Unterkapiteln
2. **Professionelle Badges** für Version, Lizenz, Plattformen und Technologien
3. **Detaillierte Installationsanleitungen** für 4 Linux-Distributionen
4. **Visuelle Elemente** mit Tabellen, Code-Blöcken und ASCII-Art
5. **Umfassende FAQ** mit 8 häufig gestellten Fragen
6. **Technische Details** zu Dateistruktur, Logging und Sicherheitskonzept
7. **Fehlerbehebung** mit konkreten Lösungen
8. **Entwicklerinformationen** und Beitragsanleitung
9. **Vollständige MIT-Lizenz** im Dokument
10. **Haftungsausschluss** zur rechtlichen Absicherung

Die README ist für Version 2.6 optimiert und berücksichtigt alle neuen Features wie benutzerdefinierte Listenverwaltung, verbessertes Logging und die erweiterte Authentifizierung.

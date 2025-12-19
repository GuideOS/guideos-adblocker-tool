Natürlich – hier ist eine passende **README.md** für dein GuideOS Adblocker‑Skript, klar strukturiert und sofort einsatzbereit:

```markdown
# GuideOS Adblocker

Ein Zenity-basiertes Bash-Skript zur zentralen Verwaltung von Werbe-, Malware- und Phishing-Domains über die Systemdatei `/etc/hosts`.

## ✨ Funktionen
- Kombiniert vordefinierte Blocklisten (StevenBlack, BlocklistProject, Phishing Army, Ultimate Hosts Blacklist).
- Unterstützung für eigene benutzerdefinierte Einträge.
- Komfortable Oberfläche mit **Zenity**:
  - Blocklisten aktivieren/deaktivieren
  - Eigene Domains hinzufügen oder verwalten
  - Originalzustand wiederherstellen
- Automatisches Backup der Originaldatei `/etc/hosts` unter `/etc/hosts.adblocker.bak`.
- Anzeige von Zeitstempeln für die letzte Aktualisierung.
- Systemweite Wirkung durch Anpassung der Hosts-Datei.
- DNS-Cache wird automatisch geleert, damit Änderungen sofort greifen.

## 📦 Voraussetzungen
- Linux-System mit Bash
- `zenity` installiert
- `curl` installiert
- Root-Rechte (Sudo)

## 🔧 Installation
1. Skript herunterladen oder in eine Datei speichern, z. B. `guideos-adblocker.sh`.
2. Ausführbar machen:
   ```bash
   chmod +x guideos-adblocker.sh
   ```
3. Starten:
   ```bash
   ./guideos-adblocker.sh
   ```

## 🛡️ Nutzung
- Beim Start fragt das Skript nach dem Sudo-Passwort.
- Blocklisten können über eine grafische Oberfläche ausgewählt werden.
- Eigene Domains lassen sich hinzufügen oder löschen.
- Änderungen greifen sofort nach dem Leeren des DNS-Caches.
- Browser sollte nach Änderungen neu gestartet werden.

## 🔄 Wiederherstellung
- Über die Option „Originalzustand wiederherstellen“ wird die gesicherte Datei `/etc/hosts.adblocker.bak` zurückgespielt.
- Alle Änderungen werden entfernt, der ursprüngliche Zustand ist wiederhergestellt.

## ⚠️ Hinweise
- Änderungen wirken systemweit und können den Zugriff auf bestimmte Domains blockieren.
- Nach Anpassungen sollte der Browser-Cache geleert werden.
- Das Skript verändert ausschließlich die Hosts-Datei und nutzt keine zusätzlichen Dienste.

## 📜 Lizenz
MIT License – frei nutzbar und veränderbar.
```

Damit hast du eine klare, sofort nutzbare README, die alle wichtigen Punkte abdeckt.  

👉 Soll ich dir auch noch eine **Kurzfassung für die Community-Foren** schreiben, die weniger technisch klingt und eher als Release-Post taugt?

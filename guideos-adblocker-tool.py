#!/usr/bin/env python3
########################################################################
"""
GuideOS Adblocker - GTK4 Version
================================
Systemweite Werbeblockierung durch /etc/hosts Manipulation.

Features:
- Vordefinierte Blocklisten (StevenBlack, BlocklistProject, EasyList Germany)
- Benutzerdefinierte Domains
- Eigene Blocklisten importieren
- Automatische Updates
- Backup/Wiederherstellung
- GTK4/libadwaita GUI

Entwickler: evilware666, helga & Copilot
Version: 2.11 (GTK4)
Lizenz: MIT
"""
#################################################################################
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio
import subprocess
import os
import re
from datetime import datetime
from pathlib import Path
import threading
import tempfile
import requests
import json

class AdBlockerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='org.guideos.adblocker',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        # Folge automatisch dem System-Theme (Hell/Dunkel)
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        
        self.CUSTOM_FILE = os.path.expanduser("~/.adblocker_custom")
        self.USER_LISTS_FILE = os.path.expanduser("~/.adblocker_user_lists.json")
        self.BACKUP_FILE = "/etc/hosts.adblocker.bak"
        self.ACTIVE_LISTS_FILE = "/etc/hosts.active_lists"
        self.LAST_UPDATE_FILE = "/etc/hosts.lastupdate"
        
        # Vordefinierte Blocklisten (alle aktiv gepflegt)
        self.BLOCKLISTS = {
            # StevenBlack Listen
            "🚫 StevenBlack (blockt Pornografie, Social Media, Fake News, Glücksspiel)": 
                "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts",
            "🚫 StevenBlack-Porn (blockt pornografischen Inhalten)": 
                "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts",
            
            # BlocklistProject Listen
            "🚫 BlocklistProject-Porn (blockt pornografischen Inhalten)": 
                "https://blocklistproject.github.io/Lists/porn.txt",
            "🚫 BlocklistProject-Phishing (blockt Phishing-Seiten)": 
                "https://blocklistproject.github.io/Lists/phishing.txt",
            "🚫 BlocklistProject-Ads (blockt Werbung)": 
                "https://blocklistproject.github.io/Lists/ads.txt",
            "🚫 BlocklistProject-Tracking (blockt Tracking)": 
                "https://blocklistproject.github.io/Lists/tracking.txt",
            
            # EasyList - Deutsche Werbung
            "🚫 EasyList Germany (blockt deutsche Werbung)": 
                "https://easylist.to/easylistgermany/easylistgermany.txt",
            
            # EasyList International
            "🚫 EasyList (internationale Werbung)": 
                "https://easylist.to/easylist/easylist.txt",
            "🚫 EasyPrivacy (Tracking & Datenschutz)": 
                "https://easylist.to/easylist/easyprivacy.txt",
            
            # Spezialisierte Listen
            "🚫 NoCoin (blockt Krypto-Miner)":
                "https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt",
            "🚫 Fanboy's Annoyance (blockt lästige Elemente)":
                "https://fanboy.co.nz/fanboy-annoyance.txt"
        }
        
        self.sudo_password = None
        
    def do_activate(self):
        if not self.sudo_password:
            self.show_password_dialog()
        else:
            self.show_startup_warning()
            self.show_main_window()
    
    def show_startup_warning(self):
        """Zeigt eine Warnung vor zu vielen Blocklisten"""
        dialog = Adw.AlertDialog(
            heading="⚠️ Wichtiger Hinweis zur Nutzung",
            body="Zu viele aktivierte Blocklisten können dazu führen, dass Webseiten nicht mehr richtig dargestellt werden oder wichtige Funktionen ausfallen.\n\nEmpfehlung: Aktivieren Sie nur die Listen, die Sie wirklich benötigen. Bei Problemen einfach einzelne Listen deaktivieren."
        )
        
        dialog.add_response("ok", "Verstanden")
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("ok")
        
        dialog.present(self.props.active_window)
    
    def show_password_dialog(self):
        # Erstelle zuerst ein leeres Hauptfenster
        temp_window = Gtk.Window()
        temp_window.set_application(self)
        temp_window.present()
        
        dialog = Adw.AlertDialog(
            heading="Administrator-Passwort eingeben",
            body="Dieses Programm benötigt Administrator-Rechte.\n\nBitte geben Sie Ihr Passwort ein:"
        )
        
        dialog.add_response("cancel", "Abbrechen")
        dialog.add_response("ok", "OK")
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("ok")
        dialog.set_close_response("cancel")
        
        entry = Gtk.PasswordEntry()
        entry.set_show_peek_icon(True)
        entry.set_margin_top(12)
        entry.set_margin_bottom(12)
        entry.set_margin_start(12)
        entry.set_margin_end(12)
        
        dialog.set_extra_child(entry)
        
        # WICHTIG: Definiere die Callbacks VOR dem Verbinden
        def on_response(dialog, response):
            temp_window.close()
            if response == "ok":
                password = entry.get_text()
                if self.verify_sudo(password):
                    self.sudo_password = password
                    self.backup_hosts()
                    self.show_startup_warning()
                    self.show_main_window()
                else:
                    self.show_error("Falsches Passwort", "Das eingegebene Passwort ist nicht korrekt.")
                    self.quit()
            else:
                self.quit()
        
        # Enter-Taste im Passwortfeld aktiviert OK
        def on_entry_activate(entry):
            # Emittiere das response Signal mit "ok" über den Dialog
            dialog.response("ok")
        
        # Verbinde die Signale
        entry.connect("activate", on_entry_activate)
        dialog.connect("response", on_response)
        
        # Zeige den Dialog
        dialog.present(temp_window)
        
        # Focus auf Entry setzen
        def focus_entry():
            entry.grab_focus()
            return False
        GLib.timeout_add(100, focus_entry)
    
    def verify_sudo(self, password):
        try:
            process = subprocess.Popen(
                ['sudo', '-S', 'true'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            process.communicate(input=f"{password}\n".encode())
            return process.returncode == 0
        except:
            return False
    
    def run_sudo_command(self, command):
        try:
            process = subprocess.Popen(
                ['sudo', '-S'] + command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(input=f"{self.sudo_password}\n".encode())
            return process.returncode == 0, stdout.decode(), stderr.decode()
        except Exception as e:
            return False, "", str(e)
    
    def backup_hosts(self):
        if not os.path.exists(self.BACKUP_FILE):
            self.run_sudo_command(['cp', '/etc/hosts', self.BACKUP_FILE])
    
    def show_main_window(self):
        win = AdBlockerWindow(application=self)
        win.present()
    
    def show_error(self, title, message):
        # Erstelle temporäres Window
        temp_window = Gtk.Window()
        temp_window.set_application(self)
        temp_window.present()
        
        dialog = Adw.AlertDialog(heading=title, body=message)
        dialog.add_response("ok", "OK")
        
        def on_response(dialog, response):
            temp_window.close()
        
        dialog.connect("response", on_response)
        dialog.present(temp_window)


class AdBlockerWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.app = self.get_application()
        self.set_default_size(600, 700)
        self.set_title("GuideOS Adblocker")
        
        # Header Bar
        header = Adw.HeaderBar()
        
        # Main content
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_spacing(0)
        
        # Toolbar View
        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header)
        toolbar_view.set_content(main_box)
        self.set_content(toolbar_view)
        
        # Info Banner
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box.set_margin_top(12)
        info_box.set_margin_bottom(6)
        info_box.set_margin_start(12)
        info_box.set_margin_end(12)
        
        # Erklärung
        explanation = Gtk.Label()
        explanation.set_markup("<small>Blockiert Werbung und schädliche Webseiten</small>")
        explanation.set_xalign(0.5)
        explanation.set_margin_top(4)
        explanation.add_css_class("dim-label")
        info_box.append(explanation)
        
        self.custom_count_label = Gtk.Label()
        self.custom_count_label.set_xalign(0.5)
        self.custom_count_label.set_margin_top(6)
        self.update_custom_count()
        info_box.append(self.custom_count_label)
        
        main_box.append(info_box)
        
        # Separator
        separator = Gtk.Separator()
        separator.set_margin_top(12)
        separator.set_margin_bottom(12)
        main_box.append(separator)
        
        # Buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        button_box.set_spacing(12)
        button_box.set_margin_top(12)
        button_box.set_margin_bottom(12)
        button_box.set_margin_start(24)
        button_box.set_margin_end(24)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_valign(Gtk.Align.CENTER)
        
        # Button 1
        btn_enable = Gtk.Button(label="📋 Blocklisten verwalten")
        btn_enable.set_size_request(400, 50)
        btn_enable.set_tooltip_text("Vordefinierte Listen aktivieren/deaktivieren")
        btn_enable.connect("clicked", self.on_enable_blocklists)
        button_box.append(btn_enable)
        
        # Button 2 - Eigene Blocklisten importieren
        btn_import = Gtk.Button(label="📥 Eigene Blocklisten importieren")
        btn_import.set_size_request(400, 50)
        btn_import.set_tooltip_text("Eigene Blocklisten aus dem Internet hinzufügen")
        btn_import.connect("clicked", self.on_import_blocklist)
        button_box.append(btn_import)
        
        # Button 3
        btn_add = Gtk.Button(label="🚫 Webseite blockieren")
        btn_add.set_size_request(400, 50)
        btn_add.set_tooltip_text("Einzelne Webseite zur Sperrliste hinzufügen")
        btn_add.connect("clicked", self.on_add_custom_entry)
        button_box.append(btn_add)
        
        # Button 4
        btn_manage = Gtk.Button(label="📝 Gesperrte Seiten verwalten")
        btn_manage.set_size_request(400, 50)
        btn_manage.set_tooltip_text("Eigene Einträge ansehen und löschen")
        btn_manage.connect("clicked", self.on_manage_custom_entries)
        button_box.append(btn_manage)
        
        # Button 5
        btn_update = Gtk.Button(label="🔄 Listen aktualisieren")
        btn_update.set_size_request(400, 50)
        btn_update.set_tooltip_text("Blocklisten auf neuesten Stand bringen")
        btn_update.connect("clicked", self.on_update_blocklists)
        button_box.append(btn_update)
        
        # Button 6
        btn_reset = Gtk.Button(label="↩️ Alles zurücksetzen")
        btn_reset.set_size_request(400, 50)
        btn_reset.add_css_class("destructive-action")
        btn_reset.set_tooltip_text("Alle Blockierungen entfernen")
        btn_reset.connect("clicked", self.on_restore_hosts)
        button_box.append(btn_reset)
        
        # Button 7
        btn_quit = Gtk.Button(label="❌ Beenden")
        btn_quit.set_size_request(400, 50)
        btn_quit.set_tooltip_text("Programm schließen")
        btn_quit.connect("clicked", lambda x: self.close())
        button_box.append(btn_quit)
        
        main_box.append(button_box)
        
        # Hinweis
        hint = Gtk.Label()
        hint.set_markup("<small>💡 <b>Tipp:</b> Nach Änderungen Browser neu starten!</small>")
        hint.set_margin_top(12)
        hint.set_margin_bottom(12)
        hint.add_css_class("dim-label")
        main_box.append(hint)
        
        # Auto-Update beim Start
        GLib.timeout_add(500, self.auto_update_on_start)
    
    def ensure_custom_active(self):
        """Stellt sicher, dass CUSTOM in den aktiven Listen ist"""
        active_lists = []
        if os.path.exists(self.app.ACTIVE_LISTS_FILE):
            with open(self.app.ACTIVE_LISTS_FILE, 'r') as f:
                active_lists = [line.strip() for line in f.readlines() if line.strip()]
        
        if "CUSTOM" not in active_lists:
            active_lists.append("CUSTOM")
            
            # Save active lists
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write('\n'.join(active_lists))
                temp_file = f.name
            
            self.app.run_sudo_command(['mv', temp_file, self.app.ACTIVE_LISTS_FILE])
    
    def auto_update_on_start(self):
        """Automatische Aktualisierung beim Start"""
        if not os.path.exists(self.app.ACTIVE_LISTS_FILE):
            return False
        
        with open(self.app.ACTIVE_LISTS_FILE, 'r') as f:
            active_lists = [line.strip() for line in f.readlines() if line.strip()]
        
        if not active_lists:
            return False
        
        # Starte Update im Hintergrund
        self.on_update_blocklists(None)
        return False
    
    def update_custom_count(self):
        count = self.count_custom_entries()
        self.custom_count_label.set_text(f"Eigene Domains geblockt: {count}")
    
    def count_custom_entries(self):
        if os.path.exists(self.app.CUSTOM_FILE):
            try:
                with open(self.app.CUSTOM_FILE, 'r') as f:
                    return sum(1 for line in f if line.startswith("0.0.0.0 "))
            except:
                return 0
        return 0
    
    def on_enable_blocklists(self, button):
        dialog = BlocklistDialog(self)
        dialog.present()
    
    def on_import_blocklist(self, button):
        """Dialog zum Importieren eigener Blocklisten"""
        dialog = ImportBlocklistDialog(self)
        dialog.present()
    
    def on_add_custom_entry(self, button):
        dialog = Adw.AlertDialog(
            heading="Webseite blockieren",
            body="Geben Sie die Webadresse ein (z.B. facebook.com):"
        )
        
        dialog.add_response("cancel", "Abbrechen")
        dialog.add_response("ok", "Blockieren")
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("ok")
        
        entry = Gtk.Entry()
        entry.set_placeholder_text("z.B. facebook.com")
        entry.set_margin_top(12)
        entry.set_margin_bottom(12)
        entry.set_margin_start(12)
        entry.set_margin_end(12)
        
        # Enter-Taste aktiviert Hinzufügen direkt
        def on_entry_activate(entry):
            domain = entry.get_text().strip()
            if domain:
                self.add_custom_domain(domain)
                dialog.close()
        
        entry.connect("activate", on_entry_activate)
        
        dialog.set_extra_child(entry)
        
        def on_response(dialog, response):
            if response == "ok":
                domain = entry.get_text().strip()
                if domain:
                    self.add_custom_domain(domain)
        
        dialog.connect("response", on_response)
        dialog.present(self)
        
        def focus_entry():
            entry.grab_focus()
            return False
        GLib.timeout_add(100, focus_entry)
    
    def add_custom_domain(self, domain):
        # Clean domain
        domain = re.sub(r'https?://', '', domain)
        domain = re.sub(r'/.*', '', domain)
        domain = re.sub(r'^www\.', '', domain)
        
        domains_to_add = [domain, f"www.{domain}"]
        
        # Ensure custom file exists
        if not os.path.exists(self.app.CUSTOM_FILE):
            Path(self.app.CUSTOM_FILE).touch()
        
        # Read existing entries
        existing = set()
        if os.path.exists(self.app.CUSTOM_FILE):
            with open(self.app.CUSTOM_FILE, 'r') as f:
                for line in f:
                    if line.startswith("0.0.0.0 "):
                        parts = line.strip().split()
                        if len(parts) > 1:
                            existing.add(parts[1])
        
        # Add new entries to custom file
        added = False
        with open(self.app.CUSTOM_FILE, 'a') as f:
            for d in domains_to_add:
                if d not in existing:
                    f.write(f"0.0.0.0 {d}\n")
                    f.write(f"::1 {d}\n")
                    added = True
        
        if added:
            # Stelle sicher, dass CUSTOM in den aktiven Listen ist
            self.ensure_custom_active()
            
            # WICHTIG: /etc/hosts komplett neu schreiben
            self.rebuild_hosts_file()
            
            # Flush DNS
            self.app.run_sudo_command(['systemd-resolve', '--flush-caches'])
            self.update_custom_count()
            
            count = self.count_custom_entries()
            self.show_info(
                "Webseite blockiert ✓",
                f"{domain} wurde gesperrt.\n\nGesperrt: {count} Webseiten\n\nBrowser bitte neu starten!"
            )
        else:
            self.show_info(
                "Bereits blockiert",
                f"{domain} ist bereits in der Sperrliste."
            )
    
    def rebuild_hosts_file(self):
        """Schreibt /etc/hosts komplett neu basierend auf aktiven Listen und Custom-Datei"""
        # Get active lists
        active_lists = []
        if os.path.exists(self.app.ACTIVE_LISTS_FILE):
            with open(self.app.ACTIVE_LISTS_FILE, 'r') as f:
                active_lists = [line.strip() for line in f.readlines() if line.strip()]
        
        temp_hosts = tempfile.NamedTemporaryFile(mode='w', delete=False)
        
        # Read original hosts
        with open(self.app.BACKUP_FILE, 'r') as f:
            temp_hosts.write(f.read())
        
        temp_hosts.write(f"\n# GuideOS Adblocker – Aktualisiert\n\n")
        
        # Add active blocklists (vordefinierte)
        for key in active_lists:
            if key == "CUSTOM" or key.startswith("USER_"):
                continue
            
            url = self.app.BLOCKLISTS.get(key)
            if not url:
                continue
            
            try:
                response = requests.get(url, timeout=30)
                content = response.text
                
                if re.search(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', content, re.MULTILINE):
                    for line in content.split('\n'):
                        if re.match(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', line):
                            line = re.sub(r'^127\.0\.0\.1', '0.0.0.0', line)
                            if not line.startswith('#'):
                                temp_hosts.write(line + '\n')
                else:
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            temp_hosts.write(f"0.0.0.0 {line}\n")
            except Exception as e:
                print(f"Fehler beim Laden von {key}: {e}")
        
        # Add user-imported blocklists
        if os.path.exists(self.app.USER_LISTS_FILE):
            try:
                with open(self.app.USER_LISTS_FILE, 'r') as f:
                    user_lists = json.load(f)
                
                for list_id, list_info in user_lists.items():
                    if list_id in active_lists:
                        temp_hosts.write(f"\n# Benutzerdefinierte Liste: {list_info['name']}\n")
                        try:
                            response = requests.get(list_info['url'], timeout=30)
                            content = response.text
                            
                            if re.search(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', content, re.MULTILINE):
                                for line in content.split('\n'):
                                    if re.match(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', line):
                                        line = re.sub(r'^127\.0\.0\.1', '0.0.0.0', line)
                                        if not line.startswith('#'):
                                            temp_hosts.write(line + '\n')
                            else:
                                for line in content.split('\n'):
                                    line = line.strip()
                                    if line and not line.startswith('#'):
                                        temp_hosts.write(f"0.0.0.0 {line}\n")
                        except Exception as e:
                            temp_hosts.write(f"# FEHLER BEIM LADEN: {e}\n")
            except:
                pass
        
        # Add custom entries - IMMER hinzufügen, wenn die Datei existiert
        if os.path.exists(self.app.CUSTOM_FILE):
            temp_hosts.write("\n# GuideOS Adblocker – Eigene Einträge\n")
            with open(self.app.CUSTOM_FILE, 'r') as f:
                custom_content = f.read()
                if custom_content.strip():  # Nur wenn nicht leer
                    temp_hosts.write(custom_content)
        
        temp_hosts.close()
        
        # Write to /etc/hosts
        success, stdout, stderr = self.app.run_sudo_command(['cp', temp_hosts.name, '/etc/hosts'])
        if not success:
            print(f"Fehler beim Kopieren: {stderr}")
        
        os.unlink(temp_hosts.name)
    
    def on_manage_custom_entries(self, button):
        if not os.path.exists(self.app.CUSTOM_FILE) or os.path.getsize(self.app.CUSTOM_FILE) == 0:
            self.show_info("Keine Einträge", "Noch keine eigenen Webseiten gesperrt.")
            return
        
        dialog = ManageCustomDialog(self)
        dialog.present()
    
    def on_update_blocklists(self, button):
        # Update im Hintergrund
        def update_thread():
            self.start_update()
            
            # Zeige Erfolg-Meldung am Ende
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
            GLib.idle_add(self.show_info, "Listen aktualisiert ✓", 
                         f"Alle Blocklisten sind aktuell.\n\nStand: {timestamp}\n\nBrowser neu starten!")
        
        thread = threading.Thread(target=update_thread)
        thread.daemon = True
        thread.start()
    
    def start_update(self):
        try:
            # Get active lists
            active_lists = []
            if os.path.exists(self.app.ACTIVE_LISTS_FILE):
                with open(self.app.ACTIVE_LISTS_FILE, 'r') as f:
                    active_lists = [line.strip() for line in f.readlines() if line.strip()]
            
            temp_hosts = tempfile.NamedTemporaryFile(mode='w', delete=False)
            
            # Read original hosts
            with open(self.app.BACKUP_FILE, 'r') as f:
                temp_hosts.write(f.read())
            
            temp_hosts.write(f"\n# GuideOS Adblocker – Aktualisiert am {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Update ALL blocklists (vordefinierte)
            all_blocklists = list(self.app.BLOCKLISTS.keys())
            
            for key in all_blocklists:
                url = self.app.BLOCKLISTS.get(key)
                if not url:
                    continue
                
                is_active = key in active_lists
                
                try:
                    response = requests.get(url, timeout=30)
                    content = response.text
                    
                    # Nur in hosts schreiben wenn aktiv
                    if is_active:
                        if re.search(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', content, re.MULTILINE):
                            for line in content.split('\n'):
                                if re.match(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', line):
                                    line = re.sub(r'^127\.0\.0\.1', '0.0.0.0', line)
                                    if not line.startswith('#'):
                                        temp_hosts.write(line + '\n')
                        else:
                            for line in content.split('\n'):
                                line = line.strip()
                                if line and not line.startswith('#'):
                                    temp_hosts.write(f"0.0.0.0 {line}\n")
                except:
                    pass
            
            # Update user-imported blocklists
            if os.path.exists(self.app.USER_LISTS_FILE):
                try:
                    with open(self.app.USER_LISTS_FILE, 'r') as f:
                        user_lists = json.load(f)
                    
                    for list_id, list_info in user_lists.items():
                        is_active = list_id in active_lists
                        
                        if is_active:
                            temp_hosts.write(f"\n# Benutzerdefinierte Liste: {list_info['name']}\n")
                            try:
                                response = requests.get(list_info['url'], timeout=30)
                                content = response.text
                                
                                if re.search(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', content, re.MULTILINE):
                                    for line in content.split('\n'):
                                        if re.match(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', line):
                                            line = re.sub(r'^127\.0\.0\.1', '0.0.0.0', line)
                                            if not line.startswith('#'):
                                                temp_hosts.write(line + '\n')
                                else:
                                    for line in content.split('\n'):
                                        line = line.strip()
                                        if line and not line.startswith('#'):
                                            temp_hosts.write(f"0.0.0.0 {line}\n")
                            except Exception as e:
                                temp_hosts.write(f"# FEHLER BEIM LADEN: {e}\n")
                except:
                    pass
            
            # Add custom entries
            if "CUSTOM" in active_lists and os.path.exists(self.app.CUSTOM_FILE):
                temp_hosts.write("\n# GuideOS Adblocker – Eigene Einträge\n")
                with open(self.app.CUSTOM_FILE, 'r') as f:
                    temp_hosts.write(f.read())
            
            temp_hosts.close()
            
            # Write to /etc/hosts
            self.app.run_sudo_command(['cp', temp_hosts.name, '/etc/hosts'])
            os.unlink(temp_hosts.name)
            
            # Flush DNS
            self.app.run_sudo_command(['systemd-resolve', '--flush-caches'])
            
            # Save timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(timestamp)
                temp_file = f.name
            self.app.run_sudo_command(['mv', temp_file, self.app.LAST_UPDATE_FILE])
            
            GLib.idle_add(self.update_custom_count)
            
        except Exception as e:
            GLib.idle_add(self.show_info, "Fehler", f"Aktualisierung fehlgeschlagen:\n{str(e)}")
    
    def on_restore_hosts(self, button):
        dialog = Adw.AlertDialog(
            heading="Wirklich alles zurücksetzen?",
            body="ALLE Blockierungen werden entfernt!\n\nFortfahren?"
        )
        
        dialog.add_response("cancel", "Abbrechen")
        dialog.add_response("restore", "Ja, zurücksetzen")
        dialog.set_response_appearance("restore", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        
        def on_response(dialog, response):
            if response == "restore":
                self.restore_hosts()
        
        dialog.connect("response", on_response)
        dialog.present(self)
    
    def restore_hosts(self):
        if os.path.exists(self.app.BACKUP_FILE):
            self.app.run_sudo_command(['cp', self.app.BACKUP_FILE, '/etc/hosts'])
            self.app.run_sudo_command(['rm', '-f', self.app.ACTIVE_LISTS_FILE])
            self.app.run_sudo_command(['systemd-resolve', '--flush-caches'])
            self.update_custom_count()
            self.show_info("Zurückgesetzt ✓", "Alle Blockierungen entfernt.\n\nBrowser neu starten!")
    
    def show_info(self, title, message):
        dialog = Adw.AlertDialog(heading=title, body=message)
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.present(self)


class ImportBlocklistDialog(Adw.Window):
    """Dialog zum Importieren eigener Blocklisten"""
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.app = parent.app
        
        self.set_title("Eigene Blocklisten importieren")
        self.set_default_size(700, 500)
        self.set_transient_for(parent)
        self.set_modal(True)
        
        header = Adw.HeaderBar()
        
        close_btn = Gtk.Button(label="Schließen")
        close_btn.connect("clicked", lambda x: self.close())
        header.pack_start(close_btn)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header)
        toolbar_view.set_content(main_box)
        self.set_content(toolbar_view)
        
        # Erklärungsbereich
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box.set_margin_top(12)
        info_box.set_margin_bottom(12)
        info_box.set_margin_start(12)
        info_box.set_margin_end(12)
        
        title_label = Gtk.Label()
        title_label.set_markup("<b>🔗 Eigene Blocklisten hinzufügen</b>")
        title_label.set_xalign(0)
        info_box.append(title_label)
        
        explanation = Gtk.Label()
        explanation.set_markup(
            "<small>Hier können Sie eigene Blocklisten aus dem Internet importieren.\n"
            "Geben Sie einen Namen und die URL der Blockliste ein.\n"
            "Die Liste muss im HOSTS-Format oder als einfache Liste von Domains vorliegen.</small>"
        )
        explanation.set_xalign(0)
        explanation.set_margin_top(6)
        explanation.add_css_class("dim-label")
        explanation.set_wrap(True)
        info_box.append(explanation)
        
        # Hinweis zu guten Quellen
        sources_label = Gtk.Label()
        sources_label.set_markup(
            "\n<small>🔍 <b>Gute Quellen für Blocklisten:</b>\n"
            "• https://easylist.to/ (EasyList, EasyPrivacy, EasyList Germany)\n"
            "• https://someonewhocares.org/hosts/zero/hosts\n"
            "• https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/SpywareFilter/sections/tracking_servers.txt\n"
            "• https://oisd.nl</small>"
        )
        sources_label.set_xalign(0)
        sources_label.set_margin_top(6)
        sources_label.add_css_class("dim-label")
        sources_label.set_wrap(True)
        info_box.append(sources_label)
        
        main_box.append(info_box)
        
        # Separator
        separator = Gtk.Separator()
        separator.set_margin_bottom(12)
        main_box.append(separator)
        
        # Eingabebereich für neue Liste
        add_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        add_box.set_margin_top(12)
        add_box.set_margin_bottom(12)
        add_box.set_margin_start(12)
        add_box.set_margin_end(12)
        add_box.set_spacing(12)
        
        add_label = Gtk.Label()
        add_label.set_markup("<b>➕ Neue Blockliste hinzufügen</b>")
        add_label.set_xalign(0)
        add_box.append(add_label)
        
        # Name Eingabe
        name_entry = Gtk.Entry()
        name_entry.set_placeholder_text("Name der Blockliste (z.B. 'Meine Werbeliste')")
        name_entry.set_margin_top(6)
        add_box.append(name_entry)
        
        # URL Eingabe
        url_entry = Gtk.Entry()
        url_entry.set_placeholder_text("URL der Blockliste (https://...)")
        url_entry.set_margin_top(6)
        add_box.append(url_entry)
        
        # Hinzufügen Button
        add_btn = Gtk.Button(label="Liste hinzufügen")
        add_btn.add_css_class("suggested-action")
        add_btn.set_margin_top(12)
        add_btn.set_halign(Gtk.Align.START)
        add_box.append(add_btn)
        
        main_box.append(add_box)
        
        # Separator
        separator2 = Gtk.Separator()
        separator2.set_margin_bottom(12)
        main_box.append(separator2)
        
        # Vorhandene Listen
        lists_label = Gtk.Label()
        lists_label.set_markup("<b>📋 Ihre importierten Blocklisten</b>")
        lists_label.set_xalign(0)
        lists_label.set_margin_start(12)
        lists_label.set_margin_end(12)
        lists_label.set_margin_bottom(6)
        main_box.append(lists_label)
        
        # Scrollbereich für vorhandene Listen
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        # Scrollbalken in Akzentfarbe
        scrolled.set_overlay_scrolling(False)
        scrolled.get_vscrollbar().add_css_class("accent")
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_margin_top(0)
        self.list_box.set_margin_bottom(12)
        self.list_box.set_margin_start(12)
        self.list_box.set_margin_end(12)
        
        scrolled.set_child(self.list_box)
        main_box.append(scrolled)
        
        # Vorhandene Listen laden
        self.load_user_lists()
        
        # Event-Handler für Hinzufügen
        add_btn.connect("clicked", self.on_add_list, name_entry, url_entry)
    
    def load_user_lists(self):
        """Lädt und zeigt vorhandene benutzerdefinierte Listen an"""
        # Alte Einträge entfernen
        while True:
            row = self.list_box.get_first_child()
            if row is None:
                break
            self.list_box.remove(row)
        
        if not os.path.exists(self.app.USER_LISTS_FILE):
            # Platzhalter wenn keine Listen vorhanden
            row = Adw.ActionRow()
            row.set_title("Keine eigenen Listen importiert")
            row.set_subtitle("Fügen Sie oben eine neue Blockliste hinzu")
            self.list_box.append(row)
            return
        
        try:
            with open(self.app.USER_LISTS_FILE, 'r') as f:
                user_lists = json.load(f)
            
            if not user_lists:
                # Platzhalter wenn keine Listen vorhanden
                row = Adw.ActionRow()
                row.set_title("Keine eigenen Listen importiert")
                row.set_subtitle("Fügen Sie oben eine neue Blockliste hinzu")
                self.list_box.append(row)
                return
            
            for list_id, list_info in user_lists.items():
                row = Adw.ActionRow()
                row.set_title(list_info['name'])
                row.set_subtitle(f"URL: {list_info['url']}\nHinzugefügt: {list_info.get('date', 'unbekannt')}")
                
                # Delete-Button
                delete_btn = Gtk.Button()
                delete_btn.set_icon_name("user-trash-symbolic")
                delete_btn.add_css_class("destructive-action")
                delete_btn.set_tooltip_text("Liste löschen")
                delete_btn.set_valign(Gtk.Align.CENTER)
                
                # ID für den Lösch-Button speichern
                delete_btn.connect("clicked", self.on_delete_list, list_id)
                
                row.add_suffix(delete_btn)
                self.list_box.append(row)
                
        except Exception as e:
            print(f"Fehler beim Laden der Listen: {e}")
    
    def on_add_list(self, button, name_entry, url_entry):
        """Fügt eine neue Blockliste hinzu"""
        name = name_entry.get_text().strip()
        url = url_entry.get_text().strip()
        
        if not name or not url:
            self.show_error("Fehler", "Bitte Name und URL eingeben!")
            return
        
        # Einfache URL-Validierung
        if not url.startswith(('http://', 'https://')):
            self.show_error("Fehler", "Die URL muss mit http:// oder https:// beginnen!")
            return
        
        # Teste ob die URL erreichbar ist
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                self.show_error("Fehler", f"URL nicht erreichbar (Status: {response.status_code})")
                return
            
            # Prüfe ob die Datei Blocklisten-ähnlichen Inhalt hat
            content = response.text[:500]  # Erste 500 Zeichen
            has_hosts = re.search(r'^(0\.0\.0\.0|127\.0\.0\.1|::1)', content, re.MULTILINE)
            has_domains = re.search(r'^[a-zA-Z0-9][a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}$', content, re.MULTILINE)
            
            if not (has_hosts or has_domains):
                # Nur warnen, nicht blockieren
                self.show_warning(
                    "Warnung", 
                    "Die Datei sieht nicht wie eine typische Blockliste aus.\n"
                    "Trotzdem importieren?",
                    name_entry, url_entry
                )
                return
        except Exception as e:
            self.show_error("Fehler", f"Konnte URL nicht erreichen:\n{str(e)}")
            return
        
        # Lade vorhandene Listen
        user_lists = {}
        if os.path.exists(self.app.USER_LISTS_FILE):
            with open(self.app.USER_LISTS_FILE, 'r') as f:
                user_lists = json.load(f)
        
        # Erstelle eindeutige ID
        import hashlib
        list_id = f"USER_{hashlib.md5(url.encode()).hexdigest()[:8]}"
        
        # Füge neue Liste hinzu
        user_lists[list_id] = {
            'name': name,
            'url': url,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # Speichern
        with open(self.app.USER_LISTS_FILE, 'w') as f:
            json.dump(user_lists, f, indent=2)
        
        # Zeige Erfolgsmeldung
        self.show_info("Erfolg", f"Liste '{name}' wurde hinzugefügt!\n\nSie können sie jetzt in den Blocklisten aktivieren.")
        
        # Eingabefelder leeren
        name_entry.set_text("")
        url_entry.set_text("")
        
        # Liste neu laden
        self.load_user_lists()
    
    def on_delete_list(self, button, list_id):
        """Löscht eine importierte Blockliste"""
        dialog = Adw.AlertDialog(
            heading="Blockliste löschen?",
            body="Möchten Sie diese Blockliste wirklich löschen?"
        )
        
        dialog.add_response("cancel", "Abbrechen")
        dialog.add_response("delete", "Löschen")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        
        def on_response(dialog, response):
            if response == "delete":
                # Lade vorhandene Listen
                if os.path.exists(self.app.USER_LISTS_FILE):
                    with open(self.app.USER_LISTS_FILE, 'r') as f:
                        user_lists = json.load(f)
                    
                    # Entferne Liste
                    if list_id in user_lists:
                        list_name = user_lists[list_id]['name']
                        del user_lists[list_id]
                        
                        # Speichern
                        with open(self.app.USER_LISTS_FILE, 'w') as f:
                            json.dump(user_lists, f, indent=2)
                        
                        # Entferne auch aus aktiven Listen falls vorhanden
                        active_lists = []
                        if os.path.exists(self.app.ACTIVE_LISTS_FILE):
                            with open(self.app.ACTIVE_LISTS_FILE, 'r') as f:
                                active_lists = [line.strip() for line in f.readlines() if line.strip()]
                            
                            if list_id in active_lists:
                                active_lists.remove(list_id)
                                
                                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                                    f.write('\n'.join(active_lists))
                                    temp_file = f.name
                                
                                self.app.run_sudo_command(['mv', temp_file, self.app.ACTIVE_LISTS_FILE])
                        
                        # Hosts neu schreiben
                        self.parent_window.rebuild_hosts_file()
                        
                        self.show_info("Erfolg", f"Liste '{list_name}' wurde gelöscht!")
                        self.load_user_lists()
        
        dialog.connect("response", on_response)
        dialog.present(self)
    
    def show_error(self, title, message):
        dialog = Adw.AlertDialog(heading=title, body=message)
        dialog.add_response("ok", "OK")
        dialog.present(self)
    
    def show_warning(self, title, message, name_entry, url_entry):
        dialog = Adw.AlertDialog(heading=title, body=message)
        dialog.add_response("cancel", "Abbrechen")
        dialog.add_response("continue", "Trotzdem importieren")
        dialog.set_response_appearance("continue", Adw.ResponseAppearance.SUGGESTED)
        
        def on_response(dialog, response):
            if response == "continue":
                # Import fortsetzen
                name = name_entry.get_text().strip()
                url = url_entry.get_text().strip()
                
                # Lade vorhandene Listen
                user_lists = {}
                if os.path.exists(self.app.USER_LISTS_FILE):
                    with open(self.app.USER_LISTS_FILE, 'r') as f:
                        user_lists = json.load(f)
                
                # Erstelle eindeutige ID
                import hashlib
                list_id = f"USER_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                
                # Füge neue Liste hinzu
                user_lists[list_id] = {
                    'name': name,
                    'url': url,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                # Speichern
                with open(self.app.USER_LISTS_FILE, 'w') as f:
                    json.dump(user_lists, f, indent=2)
                
                # Zeige Erfolgsmeldung
                self.show_info("Erfolg", f"Liste '{name}' wurde hinzugefügt!\n\nSie können sie jetzt in den Blocklisten aktivieren.")
                
                # Eingabefelder leeren
                name_entry.set_text("")
                url_entry.set_text("")
                
                # Liste neu laden
                self.load_user_lists()
        
        dialog.connect("response", on_response)
        dialog.present(self)
    
    def show_info(self, title, message):
        dialog = Adw.AlertDialog(heading=title, body=message)
        dialog.add_response("ok", "OK")
        dialog.present(self)


class BlocklistDialog(Adw.Window):
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.app = parent.app
        
        self.set_title("Blocklisten verwalten")
        # Fenstergröße - hier kann angepasst werden
        self.set_default_size(950, 650)  # Breite: 950px, Höhe: 650px (etwas größer für die Infos)
        self.set_transient_for(parent)
        self.set_modal(True)
        
        header = Adw.HeaderBar()
        
        cancel_btn = Gtk.Button(label="Abbrechen")
        cancel_btn.connect("clicked", lambda x: self.close())
        header.pack_start(cancel_btn)
        
        apply_btn = Gtk.Button(label="Anwenden")
        apply_btn.add_css_class("suggested-action")
        apply_btn.set_tooltip_text("Listen aktivieren und aktualisieren")
        apply_btn.connect("clicked", self.on_apply)
        header.pack_end(apply_btn)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header)
        toolbar_view.set_content(main_box)
        self.set_content(toolbar_view)
        
        # Info mit Erklärung
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_box.set_margin_top(12)
        info_box.set_margin_bottom(12)
        info_box.set_margin_start(12)
        info_box.set_margin_end(12)
        
        info_label = Gtk.Label()
        info_label.set_markup("<b>📋 Verfügbare Blocklisten</b>")
        info_label.set_xalign(0)
        info_box.append(info_label)
        
        explanation = Gtk.Label()
        explanation.set_markup(
            "<small>Wählen Sie die gewünschten Blocklisten aus.\n"
            "Jede Liste hat eine spezifische Aufgabe - zu viele gleichzeitig können Probleme verursachen.</small>"
        )
        explanation.set_xalign(0)
        explanation.set_margin_top(4)
        explanation.add_css_class("dim-label")
        explanation.set_wrap(True)
        info_box.append(explanation)
        
        main_box.append(info_box)
        
        # Get last update
        last_update = "unbekannt"
        if os.path.exists(self.app.LAST_UPDATE_FILE):
            with open(self.app.LAST_UPDATE_FILE, 'r') as f:
                last_update = f.read().strip()
        
        # Get active lists
        active_lists = []
        if os.path.exists(self.app.ACTIVE_LISTS_FILE):
            with open(self.app.ACTIVE_LISTS_FILE, 'r') as f:
                active_lists = [line.strip() for line in f.readlines() if line.strip()]
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        # Scrollbalken in Akzentfarbe
        scrolled.set_overlay_scrolling(False)
        scrolled.get_vscrollbar().add_css_class("accent")
        
        list_box = Gtk.ListBox()
        list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        list_box.add_css_class("boxed-list")
        list_box.set_margin_top(0)
        list_box.set_margin_bottom(12)
        list_box.set_margin_start(12)
        list_box.set_margin_end(12)
        
        self.checkboxes = {}
        
        # Dictionary mit detaillierten Beschreibungen für jede Liste
        list_descriptions = {
            "🚫 StevenBlack (blockt Pornografie, Social Media, Fake News, Glücksspiel)": 
                "Blockiert: Pornografie, Social Media (Facebook, Instagram, etc.), Fake News Seiten und Glücksspiel-Websites. Sehr umfassende Hosts-Liste.",
            
            "🚫 StevenBlack-Porn (blockt pornografischen Inhalten)": 
                "Blockiert: Ausschließlich pornografische Inhalte.",
            
            "🚫 BlocklistProject-Porn (blockt pornografischen Inhalten)": 
                "Blockiert: Über 500.000 pornografische Domains. Sehr umfangreiche Spezialliste für Erwachseneninhalte.",
            
            "🚫 BlocklistProject-Phishing (blockt Phishing-Seiten)": 
                "Blockiert: Betrügerische Webseiten, die Passwörter und Kreditkartendaten stehlen wollen. Schützt vor Identitätsdiebstahl.",
            
            "🚫 BlocklistProject-Ads (blockt Werbung)": 
                "Blockiert: Werbenetzwerke, Popups, Banner und Video-Werbung auf Webseiten. Reduziert Datenverbrauch und Ladezeiten.",
            
            "🚫 BlocklistProject-Tracking (blockt Tracking)": 
                "Blockiert: Tracking-Dienste, die Ihr Surfverhalten analysieren. Schützt Ihre Privatsphäre vor Datensammlern.",
            
            "🚫 EasyList Germany (blockt deutsche Werbung)": 
                "Blockiert: Speziell deutsche Werbung von deutschen Webseiten. Ideal für Surfer aus Deutschland, Österreich und der Schweiz.",
            
            "🚫 EasyList (internationale Werbung)": 
                "Blockiert: Internationale Werbung auf englischsprachigen und internationalen Webseiten.",
            
            "🚫 EasyPrivacy (Tracking & Datenschutz)": 
                "Blockiert: Tracking-Pixel, Analyse-Tools und Datensammler. Ergänzung zu EasyList für maximalen Datenschutz.",
            
            "🚫 NoCoin (blockt Krypto-Miner)": 
                "Blockiert: Kryptowährungs-Miner, die im Hintergrund Ihre CPU für Mining missbrauchen. Spart Akku und verhindert Überhitzung.",
            
            "🚫 Fanboy's Annoyance (blockt lästige Elemente)": 
                "Blockiert: Cookie-Hinweise, Newsletter-Popups, Social-Media-Buttons und andere lästige Elemente. Saubereres Surferlebnis."
        }
        
        # Vordefinierte Blocklisten
        for key, url in self.app.BLOCKLISTS.items():
            row = Adw.ActionRow()
            
            # Extrahiere den Listennamen aus dem Schlüssel
            if "EasyPrivacy" in key:
                display_title = "🚫 EasyPrivacy"
            elif "EasyList Germany" in key:
                display_title = "🚫 EasyList Germany"
            elif "Fanboy's Annoyance" in key:
                display_title = "🚫 Fanboy's Annoyance"
            elif "StevenBlack" in key:
                if "Porn" in key:
                    display_title = "🚫 StevenBlack (Porn)"
                else:
                    display_title = "🚫 StevenBlack (Fakenews/Gambling)"
            elif "BlocklistProject" in key:
                if "Porn" in key:
                    display_title = "🚫 BlocklistProject (Porn)"
                elif "Phishing" in key:
                    display_title = "🚫 BlocklistProject (Phishing)"
                elif "Ads" in key:
                    display_title = "🚫 BlocklistProject (Ads)"
                elif "Tracking" in key:
                    display_title = "🚫 BlocklistProject (Tracking)"
                else:
                    display_title = "🚫 BlocklistProject"
            elif "NoCoin" in key:
                display_title = "🚫 NoCoin"
            elif "EasyList" in key and "Germany" not in key and "Privacy" not in key:
                display_title = "🚫 EasyList"
            else:
                # Fallback: Verwende den ersten Teil des Keys bis zur Klammer
                display_title = key.split('(')[0].strip()
            
            # Hole die detaillierte Beschreibung
            description = list_descriptions.get(key, f"Blockiert: Diverse Webseiten. Stand: {last_update}")
            
            row.set_title(display_title)
            row.set_subtitle(description)
            
            check = Gtk.CheckButton()
            check.set_active(key in active_lists)
            check.set_valign(Gtk.Align.CENTER)
            row.add_prefix(check)
            
            self.checkboxes[key] = check
            list_box.append(row)
        
        # Benutzerdefinierte importierte Listen
        if os.path.exists(self.app.USER_LISTS_FILE):
            try:
                with open(self.app.USER_LISTS_FILE, 'r') as f:
                    user_lists = json.load(f)
                
                for list_id, list_info in user_lists.items():
                    row = Adw.ActionRow()
                    row.set_title(f"📥 {list_info['name']}")
                    row.set_subtitle(f"URL: {list_info['url']} | Hinzugefügt: {list_info.get('date', 'unbekannt')}")
                    
                    check = Gtk.CheckButton()
                    check.set_active(list_id in active_lists)
                    check.set_valign(Gtk.Align.CENTER)
                    row.add_prefix(check)
                    
                    self.checkboxes[list_id] = check
                    list_box.append(row)
            except:
                pass
        
        # Custom entries
        if os.path.exists(self.app.CUSTOM_FILE):
            row = Adw.ActionRow()
            row.set_title("✏️ Eigene Einträge (benutzerdefiniert)")
            row.set_subtitle(f"Ihre manuell blockierten Webseiten. Hier können Sie einzelne Domains sperren. | Stand: {last_update}")
            
            check = Gtk.CheckButton()
            check.set_active("CUSTOM" in active_lists)
            check.set_valign(Gtk.Align.CENTER)
            row.add_prefix(check)
            
            self.checkboxes["CUSTOM"] = check
            list_box.append(row)
        
        scrolled.set_child(list_box)
        main_box.append(scrolled)
    
    def on_apply(self, button):
        selected = [key for key, check in self.checkboxes.items() if check.get_active()]
        
        # Save active lists (newline-separated)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('\n'.join(selected))
            temp_file = f.name
        
        self.app.run_sudo_command(['mv', temp_file, self.app.ACTIVE_LISTS_FILE])
        self.close()
        
        # Auto-update nach Auswahl
        self.parent_window.on_update_blocklists(None)


class ManageCustomDialog(Adw.Window):
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.app = parent.app
        
        self.set_title("Gesperrte Webseiten")
        self.set_default_size(600, 450)
        self.set_transient_for(parent)
        self.set_modal(True)
        
        header = Adw.HeaderBar()
        
        close_btn = Gtk.Button(label="Schließen")
        close_btn.connect("clicked", lambda x: self.close())
        header.pack_start(close_btn)
        
        delete_btn = Gtk.Button(label="Ausgewählte freigeben")
        delete_btn.add_css_class("destructive-action")
        delete_btn.set_tooltip_text("Markierte Webseiten wieder freigeben")
        delete_btn.connect("clicked", self.on_delete)
        header.pack_end(delete_btn)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header)
        toolbar_view.set_content(main_box)
        self.set_content(toolbar_view)
        
        info_label = Gtk.Label()
        info_label.set_markup("<b>Ihre gesperrten Webseiten:</b>")
        info_label.set_xalign(0)
        info_label.set_margin_top(12)
        info_label.set_margin_bottom(12)
        info_label.set_margin_start(12)
        info_label.set_margin_end(12)
        main_box.append(info_label)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        # Scrollbalken in Akzentfarbe
        scrolled.set_overlay_scrolling(False)
        scrolled.get_vscrollbar().add_css_class("accent")
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_margin_top(0)
        self.list_box.set_margin_bottom(12)
        self.list_box.set_margin_start(12)
        self.list_box.set_margin_end(12)
        
        self.checkboxes = {}
        
        with open(self.app.CUSTOM_FILE, 'r') as f:
            for line in f:
                if line.startswith("0.0.0.0 "):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        domain = parts[1]
                        
                        row = Adw.ActionRow()
                        row.set_title(domain)
                        row.set_subtitle("Manuell blockierte Webseite")
                        
                        check = Gtk.CheckButton()
                        check.set_valign(Gtk.Align.CENTER)
                        row.add_prefix(check)
                        
                        self.checkboxes[domain] = check
                        self.list_box.append(row)
        
        scrolled.set_child(self.list_box)
        main_box.append(scrolled)
    
    def on_delete(self, button):
        to_delete = [domain for domain, check in self.checkboxes.items() if check.get_active()]
        
        if not to_delete:
            return
        
        dialog = Adw.AlertDialog(
            heading="Webseiten freigeben?",
            body=f"{len(to_delete)} Webseite(n) werden wieder freigegeben."
        )
        
        dialog.add_response("cancel", "Abbrechen")
        dialog.add_response("delete", "Freigeben")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        
        def on_response(dialog, response):
            if response == "delete":
                self.delete_domains(to_delete)
        
        dialog.connect("response", on_response)
        dialog.present(self)
    
    def delete_domains(self, domains):
        # Remove from custom file
        if os.path.exists(self.app.CUSTOM_FILE):
            with open(self.app.CUSTOM_FILE, 'r') as f:
                lines = f.readlines()
            
            with open(self.app.CUSTOM_FILE, 'w') as f:
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) > 1 and parts[1] not in domains:
                        f.write(line)
        
        # WICHTIG: /etc/hosts komplett neu schreiben
        self.parent_window.rebuild_hosts_file()
        
        # Flush DNS
        self.app.run_sudo_command(['systemd-resolve', '--flush-caches'])
        
        count = self.parent_window.count_custom_entries()
        self.parent_window.update_custom_count()
        self.close()
        
        self.parent_window.show_info(
            "Webseiten freigegeben ✓",
            f"Noch gesperrt: {count} Webseiten\n\nBrowser neu starten!"
        )


def main():
    app = AdBlockerApp()
    return app.run(None)


if __name__ == "__main__":
    main()

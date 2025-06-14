#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
import subprocess
import signal
import os

class XboxBatteryTray:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "xbox-battery-tray",
            "",  # Sin icono
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()
        
        self.quit_item = Gtk.MenuItem(label="Salir")
        self.quit_item.connect("activate", self.quit)
        self.menu.append(self.quit_item)
        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        
        self.update_battery()

    def get_xbox_device(self):
        try:
            devices = subprocess.check_output("upower -e", shell=True).decode().splitlines()
            for dev in devices:
                if "xbox" in dev.lower() or "gaming_input" in dev:
                    return dev
            return None
        except:
            return None

    def get_battery_percent(self):
        device = self.get_xbox_device()
        if not device:
            return "🚫"
        try:
            info = subprocess.check_output(f"upower -i {device}", shell=True).decode()
            for line in info.splitlines():
                if "percentage" in line:
                    return line.split(":")[1].strip()
            return "?"
        except:
            return "❌"

    def update_battery(self, _=None):
        percent = self.get_battery_percent()
        self.indicator.set_label(f"Xbox: {percent}", "")
        self.indicator.set_title(f"Batería: {percent}")  # Tooltip
        GLib.timeout_add_seconds(3, self.update_battery)
        return False

    def quit(self, _):
        Gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = XboxBatteryTray()
    Gtk.main()

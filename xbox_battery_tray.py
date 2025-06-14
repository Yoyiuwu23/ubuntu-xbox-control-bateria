#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
import subprocess
import signal
import time

class XboxBatteryTray:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "xbox-battery-tray",
            "battery-full-symbolic",  # Icono de batería
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()
        
        # Opción "Salir" (puedes comentar estas líneas si no la quieres)
        self.quit_item = Gtk.MenuItem(label="Salir")
        self.quit_item.connect("activate", self.quit)
        self.menu.append(self.quit_item)
        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        
        self.device_path = None
        self.update_battery()

    def refresh_upower_devices(self):
        try:
            subprocess.run(["upower", "--dump"], check=True, capture_output=True)
        except:
            pass

    def get_xbox_device(self):
        try:
            self.refresh_upower_devices()
            devices = subprocess.check_output("upower -e", shell=True).decode().splitlines()
            for dev in devices:
                if any(kw in dev.lower() for kw in ["xbox", "gaming_input", "hidpp"]):
                    return dev
            return None
        except:
            return None

    def get_battery_percent(self, device):
        try:
            info = subprocess.check_output(
                f"upower -i {device}",
                shell=True,
                stderr=subprocess.DEVNULL
            ).decode()
            for line in info.splitlines():
                if "percentage" in line.lower():
                    return line.split(":")[1].strip()
                if "battery-level" in line.lower():
                    return f"{float(line.split(':')[1].strip()) * 100:.0f}%"
            return "?"
        except:
            return "❌"

    def update_battery(self, _=None):
        if not self.device_path:
            self.device_path = self.get_xbox_device()
            if not self.device_path:
                self.indicator.set_label("🔎 Buscando...", "")
                GLib.timeout_add_seconds(3, self.update_battery)
                return False
        
        percent = self.get_battery_percent(self.device_path)
        
        if percent == "❌":
            self.device_path = None
            self.indicator.set_label("⚠️ Reconectando...", "")
        else:
            self.indicator.set_label(f"🔋 {percent}", "")  # Icono de batería y porcentaje
        
        GLib.timeout_add_seconds(3, self.update_battery)
        return False

    def quit(self, _):
        Gtk.main_quit()

if __name__ == "__main__":
    time.sleep(2)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = XboxBatteryTray()
    Gtk.main()

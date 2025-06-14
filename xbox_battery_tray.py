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
        # Obtiene la ruta completa del icono (debe estar en la misma carpeta)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "xbox-icon.png")
        
        # Crea el indicador con el icono personalizado
        self.indicator = AppIndicator3.Indicator.new(
            "xbox-battery-tray",
            icon_path,  # Usa la ruta completa al icono
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()
        
        # Elementos del menú
        self.quit_item = Gtk.MenuItem(label="Salir")
        self.quit_item.connect("activate", self.quit)
        self.menu.append(self.quit_item)
        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        
        # Actualización inicial
        self.update_battery()
    
    def get_xbox_device(self):
        """Detecta automáticamente el dispositivo Xbox"""
        try:
            devices = subprocess.check_output("upower -e", shell=True).decode().splitlines()
            for dev in devices:
                if "xbox" in dev.lower() or "gaming_input" in dev:
                    return dev
            return None
        except:
            return None

    def get_battery_percent(self):
        """Obtiene el porcentaje de batería"""
        device = self.get_xbox_device()
        if not device:
            return "🚫"  # Icono si no se detecta
        
        try:
            info = subprocess.check_output(f"upower -i {device}", shell=True).decode()
            for line in info.splitlines():
                if "percentage" in line:
                    return line.split(":")[1].strip()
            return "?"
        except:
            return "❌"

    def update_battery(self, _=None):
        """Actualiza el texto del icono cada 30 segundos"""
        percent = self.get_battery_percent()
        self.indicator.set_label(f"🕹️ {percent}", "")  # Usa 🕹️ o el texto que prefieras
        
        # Programa la próxima actualización
        GLib.timeout_add_seconds(30, self.update_battery)
        return False

    def quit(self, _):
        Gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = XboxBatteryTray()
    Gtk.main()

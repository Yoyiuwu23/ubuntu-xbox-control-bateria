```markdown
# Xbox Battery Tray Indicator for Ubuntu

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)
![Platform](https://img.shields.io/badge/Platform-Ubuntu-E95420?logo=ubuntu&logoColor=white)

Monitor de batería para control de Xbox en la bandeja del sistema de Ubuntu, desarrollado en Python.

## Características

- **Muestra el nivel de batería del control Xbox en la bandeja del sistema**
- **Icono transparente personalizable**
- **Actualización automática cada pocos segundos**
- **Interfaz simple y ligera**

## Requisitos

- **Ubuntu** (o derivados de Debian)
- **Python 3**
- **Paquetes del sistema:**
```

gir1.2-appindicator3-0.1
python3-gi

```

## Instalación

1. Instala las dependencias:
```

sudo apt install gir1.2-appindicator3-0.1 python3-gi

```
2. Descarga el código y dale permisos de ejecución:
```

chmod +x main.py

```
3. Ejecuta la aplicación:
```

./main.py

```

## Personalización

Puedes usar tu propio icono transparente (SVG o PNG) cambiando la ruta en el código.

---

**¡Disfruta monitoreando la batería de tu control Xbox directamente desde Ubuntu!**
```

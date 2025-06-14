#!/bin/bash

# Obtiene el porcentaje de batería del control de Xbox conectado por Bluetooth
dispositivo="/org/freedesktop/UPower/devices/gaming_input_dev_98_7A_14_41_BD_05"
if [ -n "$(upower -e | grep "$dispositivo")" ]; then
    porcentaje=$(upower -i "$dispositivo" | grep "percentage" | awk '{print $2}')
    if [ -n "$porcentaje" ]; then
        notify-send "Batería Xbox" "El control tiene $porcentaje de batería"
    else
        notify-send "Batería Xbox" "No se pudo obtener el porcentaje de batería"
    fi
else
    notify-send "Batería Xbox" "No se detecta el control Xbox conectado"
fi

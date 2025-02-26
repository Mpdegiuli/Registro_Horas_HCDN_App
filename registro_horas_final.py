# -*- coding: utf-8 -*-
"""Registro_Horas_Final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zkYFGNJgRzLHSWPJh32aF9KGS1nn4MYT

📌 **Registro de Horas Trabajadas**
👩‍💻 **Desarrollado por:** Mariana de Giuli  
📅 **Fecha:** 21/02/2025  
📩 **Contacto:** mpdegiuli@gmail.com
"""

# -----------------------------------
# 📌 Programa: Control de horas trabajadas
# 👩‍💻 Autor: Mariana de Giuli
# 📅 Fecha: 21/02/2025
# 📩 Email: mpdegiuli@gmail.com
# 📌 Descripción: Registra entrada, salida y pausas, verifica que haya al menos 4 horas seguidas sin interrupción y muestra un resumen en tiempo real.
# -----------------------------------
import json
import os
from datetime import datetime, timedelta

# Definir el archivo donde se guardan los registros
ARCHIVO_DATOS = "/content/drive/My Drive/horas_trabajadas.json"

# Cargar datos previos si existen
if os.path.exists(ARCHIVO_DATOS):
    with open(ARCHIVO_DATOS, "r") as file:
        horas_trabajadas = json.load(file)
else:
    horas_trabajadas = {}

# Definir constantes
HORAS_SEMANALES_REQUERIDAS = 35
HORAS_POR_DIA_ESTANDAR = 7
HORAS_MINIMAS_SEGUIDAS = 4  # Mínimo de horas continuas requeridas por día

# Función para convertir minutos en formato horas y minutos
def formatear_horas_minutos(total_minutos):
    horas = total_minutos // 60
    minutos = total_minutos % 60
    return f"{horas} horas {minutos} minutos"

# Función para calcular horas trabajadas
def calcular_horas(entrada, salida, pausas):
    formato = "%H:%M"
    entrada_dt = datetime.strptime(entrada, formato)
    salida_dt = datetime.strptime(salida, formato)

    tiempo_total = salida_dt - entrada_dt

    # Restar pausas
    for pausa in pausas:
        inicio_pausa_dt = datetime.strptime(pausa[0], formato)
        fin_pausa_dt = datetime.strptime(pausa[1], formato)
        tiempo_total -= (fin_pausa_dt - inicio_pausa_dt)

    return round(tiempo_total.total_seconds() / 60)  # Retorna minutos

# Registrar horas día por día
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
for dia in dias_semana:
    print(f"\n📅 **Registro de horas para {dia}:**")

    if dia in horas_trabajadas:
        modificar = input(f"¿Querés corregir las horas de {dia}? (Sí/No): ").strip().lower()
        if modificar in ["si", "sí"]:
            del horas_trabajadas[dia]  # Eliminar datos previos para corregir

    falta_justificada = input(f"¿Faltaste el {dia} con justificación? (Sí/No): ").strip().lower()
    if falta_justificada in ["si", "sí"]:
        horas_trabajadas[dia] = "Falta Justificada"
        print(f"✅ {dia} marcado como falta justificada.")
        continue  # Salta al siguiente día

    entrada = input(f"Ingresá la hora de entrada para {dia} (Formato 24 hs, Ejemplo: 08:00): ").strip()
    salida = input(f"Ingresá la hora de salida para {dia} (Formato 24 hs, Ejemplo: 17:00): ").strip()

    pausas = []
    while True:
        pausa = input(f"¿Hubo alguna pausa en {dia}? (Sí/No): ").strip().lower()
        if pausa not in ["si", "sí"]:
            break
        inicio_pausa = input(f"Ingresá la hora de inicio de la pausa (Ejemplo: 13:30): ").strip()
        fin_pausa = input(f"Ingresá la hora de fin de la pausa (Ejemplo: 13:50): ").strip()
        pausas.append((inicio_pausa, fin_pausa))

    # Calcular total trabajado
    minutos_trabajados = calcular_horas(entrada, salida, pausas)
    horas_trabajadas[dia] = minutos_trabajados

    # Verificar si cumplió con las 4 horas seguidas
    formato = "%H:%M"
    entrada_dt = datetime.strptime(entrada, formato)
    primera_pausa = min([datetime.strptime(p[0], formato) for p in pausas], default=None)

    if primera_pausa:
        tiempo_continuo = (primera_pausa - entrada_dt).total_seconds() / 3600
    else:
        tiempo_continuo = (datetime.strptime(salida, formato) - entrada_dt).total_seconds() / 3600

    if tiempo_continuo < HORAS_MINIMAS_SEGUIDAS:
        print(f"⚠ Atención: No cumpliste las 4 horas seguidas obligatorias en {dia}.")

    # Mostrar resumen diario
    diferencia = minutos_trabajados - (HORAS_POR_DIA_ESTANDAR * 60)
    if diferencia > 0:
        print(f"✅ Se registraron {formatear_horas_minutos(minutos_trabajados)} para {dia} (+{formatear_horas_minutos(diferencia)} de más).")
    elif diferencia < 0:
        print(f"✅ Se registraron {formatear_horas_minutos(minutos_trabajados)} para {dia} (-{formatear_horas_minutos(abs(diferencia))} de menos).")
    else:
        print(f"✅ Se registraron {formatear_horas_minutos(minutos_trabajados)} para {dia}, cumpliendo exactamente con las 7 horas.")

# Guardar datos
with open(ARCHIVO_DATOS, "w") as file:
    json.dump(horas_trabajadas, file)

# Calcular totales
total_minutos_trabajados = sum(v for v in horas_trabajadas.values() if isinstance(v, int))
acumulado_extra = total_minutos_trabajados - (HORAS_SEMANALES_REQUERIDAS * 60)

# Mostrar resumen final
print("\n📊 **Estado hasta ahora:**")
print(f"🔹 Total acumulado: {formatear_horas_minutos(total_minutos_trabajados)} trabajadas")
print(f"🔹 Horas faltantes para completar la semana: {formatear_horas_minutos(max(0, (HORAS_SEMANALES_REQUERIDAS * 60) - total_minutos_trabajados))}")

# Mostrar horas de más o de menos por día
for dia, minutos in horas_trabajadas.items():
    if isinstance(minutos, int):  # Si no es "Falta Justificada"
        diferencia = minutos - (HORAS_POR_DIA_ESTANDAR * 60)
        if diferencia > 0:
            print(f"🔹 {dia}: +{formatear_horas_minutos(diferencia)} horas de más")
        elif diferencia < 0:
            print(f"🔹 {dia}: -{formatear_horas_minutos(abs(diferencia))} horas de menos")
        else:
            print(f"🔹 {dia}: Exactamente {HORAS_POR_DIA_ESTANDAR} horas trabajadas.")

# Mostrar saldo final
if acumulado_extra > 0:
    print(f"🔹 **Acumulado total de horas de más:** +{formatear_horas_minutos(acumulado_extra)}")
elif acumulado_extra < 0:
    print(f"🔹 **Acumulado total de horas de menos:** -{formatear_horas_minutos(abs(acumulado_extra))}")
else:
    print(f"🔹 **No hay horas extra ni faltantes.**")
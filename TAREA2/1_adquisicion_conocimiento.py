# 1. ADQUISICIÓN DEL CONOCIMIENTO
# Sistema experto - Ejemplo funcional por separado
# ¿Qué es?
# Es la parte donde el sistema obtiene conocimiento nuevo.
#
# ¿Para qué sirve?
# Sirve para agregar información nueva a la base del sistema experto.
#
# ¿Cómo funciona?
# El usuario o experto proporciona datos y el sistema los guarda.
#
# Ejemplo:
# Agregar un nuevo mob de Minecraft a una base de conocimiento.

import json
from pathlib import Path

ARCHIVO_CONOCIMIENTO = Path("conocimiento_mobs.json")


def preguntar_si_no(pregunta):
    while True:
        respuesta = input(pregunta + " [si/no]: ").strip().lower()

        if respuesta in ["si", "sí", "s"]:
            return "si"
        elif respuesta in ["no", "n"]:
            return "no"
        else:
            print("Respuesta no válida. Escribe si o no.")


def cargar_conocimiento():
    """
    Carga la base de conocimiento desde un archivo JSON.
    Si el archivo no existe, crea una base inicial.
    """

    if ARCHIVO_CONOCIMIENTO.exists():
        with open(ARCHIVO_CONOCIMIENTO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    base_inicial = {
        "Allay": {
            "vuela": "si",
            "overworld": "si",
            "hostil": "no",
            "decorativo": "no",
            "aparece_en_estructura": "si"
        },
        "Murciélago": {
            "vuela": "si",
            "overworld": "si",
            "hostil": "no",
            "decorativo": "si",
            "aparece_en_estructura": "no"
        }
    }

    return base_inicial


def guardar_conocimiento(base_conocimiento):
    """
    Guarda la base de conocimiento en un archivo JSON.
    """

    with open(ARCHIVO_CONOCIMIENTO, "w", encoding="utf-8") as archivo:
        json.dump(base_conocimiento, archivo, indent=4, ensure_ascii=False)


def adquirir_conocimiento():
    print("     ADQUISICIÓN DEL CONOCIMIENTO")
    print("En esta parte se agrega conocimiento nuevo al sistema experto.\n")

    base_conocimiento = cargar_conocimiento()

    nombre_mob = input("Escribe el nombre del mob que quieres agregar: ").strip()

    if nombre_mob in base_conocimiento:
        print(f"\nEl mob '{nombre_mob}' ya existe en la base de conocimiento.")
        return

    nuevo_mob = {
        "vuela": preguntar_si_no("¿El mob vuela?"),
        "overworld": preguntar_si_no("¿El mob aparece en el Overworld?"),
        "hostil": preguntar_si_no("¿El mob es hostil?"),
        "decorativo": preguntar_si_no("¿El mob es decorativo?"),
        "aparece_en_estructura": preguntar_si_no("¿El mob aparece en estructuras específicas?")
    }

    base_conocimiento[nombre_mob] = nuevo_mob
    guardar_conocimiento(base_conocimiento)

    print("\nConocimiento agregado correctamente.")
    print(f"El conocimiento fue guardado en: {ARCHIVO_CONOCIMIENTO}")


if __name__ == "__main__":
    adquirir_conocimiento()
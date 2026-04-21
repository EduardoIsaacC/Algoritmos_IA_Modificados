# 2. REPRESENTACIÓN DEL CONOCIMIENTO
# Sistema experto - Ejemplo funcional por separado
# ¿Qué es?
# Es la forma en que el sistema organiza el conocimiento.
#
# ¿Para qué sirve?
# Sirve para que el sistema pueda usar reglas y hechos.
#
# ¿Cómo funciona?
# Se divide en:
# - Base de conocimiento: reglas generales.
# - Base de hechos: datos del caso actual.
#
# Ejemplo:
# Reglas para identificar mobs de Minecraft.
# BASE DE CONOCIMIENTO
# La base de conocimiento guarda información general.
# Esta información normalmente permanece en el sistema.
#
# Ejemplo de regla:
# SI vuela = si
# Y overworld = si
# Y decorativo = no
# ENTONCES puede ser Allay.

base_conocimiento = [
    {
        "nombre_regla": "Identificar Allay",
        "condiciones": {
            "vuela": "si",
            "overworld": "si",
            "hostil": "no",
            "decorativo": "no",
            "aparece_en_estructura": "si"
        },
        "conclusion": "El mob puede ser un Allay."
    },
    {
        "nombre_regla": "Identificar Murciélago",
        "condiciones": {
            "vuela": "si",
            "overworld": "si",
            "hostil": "no",
            "decorativo": "si",
            "aparece_en_estructura": "no"
        },
        "conclusion": "El mob puede ser un Murciélago."
    },
    {
        "nombre_regla": "Identificar Creeper",
        "condiciones": {
            "vuela": "no",
            "overworld": "si",
            "hostil": "si",
            "explota": "si"
        },
        "conclusion": "El mob puede ser un Creeper."
    }
]


# BASE DE HECHOS
# La base de hechos guarda información temporal.
# Son los datos del caso que se está analizando en ese momento.

base_hechos = {
    "vuela": "si",
    "overworld": "si",
    "hostil": "no",
    "decorativo": "no",
    "aparece_en_estructura": "si"
}


def mostrar_base_conocimiento():
    print("          BASE DE CONOCIMIENTO")

    for regla in base_conocimiento:
        print(f"\nRegla: {regla['nombre_regla']}")
        print("Condiciones:")

        for condicion, valor in regla["condiciones"].items():
            print(f"  - {condicion} = {valor}")

        print(f"Conclusión: {regla['conclusion']}")


def mostrar_base_hechos():
    print("              BASE DE HECHOS")

    for hecho, valor in base_hechos.items():
        print(f"- {hecho} = {valor}")


def explicar_representacion():
    print("     REPRESENTACIÓN DEL CONOCIMIENTO")
    print("Este programa muestra cómo se guarda el conocimiento.")
    print("La base de conocimiento contiene reglas generales.")
    print("La base de hechos contiene datos del caso actual.")


if __name__ == "__main__":
    explicar_representacion()
    mostrar_base_conocimiento()
    mostrar_base_hechos()
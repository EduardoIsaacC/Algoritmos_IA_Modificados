# 3. TRATAMIENTO DEL CONOCIMIENTO
# Sistema experto - Ejemplo funcional por separado
# ¿Qué es?
# Es la parte donde el sistema razona.
#
# ¿Para qué sirve?
# Sirve para obtener conclusiones usando reglas y hechos.
#
# ¿Cómo funciona?
# El motor de inferencia compara los hechos actuales con las reglas.
# Si las condiciones de una regla se cumplen, se genera una conclusión.
#
# Ejemplo:
# Identificar un mob de Minecraft usando hechos conocidos.

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
        "conclusion": "El mob probablemente es un Allay."
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
        "conclusion": "El mob probablemente es un Murciélago."
    },
    {
        "nombre_regla": "Identificar Creeper",
        "condiciones": {
            "vuela": "no",
            "overworld": "si",
            "hostil": "si",
            "explota": "si"
        },
        "conclusion": "El mob probablemente es un Creeper."
    },
    {
        "nombre_regla": "Identificar Esqueleto",
        "condiciones": {
            "vuela": "no",
            "overworld": "si",
            "hostil": "si",
            "ataca_distancia": "si"
        },
        "conclusion": "El mob probablemente es un Esqueleto."
    }
]


def motor_inferencia(hechos):
    """
    Motor de inferencia:
    compara los hechos con las reglas de la base de conocimiento.
    """

    conclusiones = []

    for regla in base_conocimiento:
        condiciones = regla["condiciones"]
        regla_cumplida = True

        for condicion, valor_esperado in condiciones.items():
            valor_real = hechos.get(condicion)

            if valor_real != valor_esperado:
                regla_cumplida = False
                break

        if regla_cumplida:
            conclusiones.append(regla)

    return conclusiones


def modulo_explicacion(regla, hechos):
    """
    Módulo de explicación:
    muestra por qué el sistema llegó a una conclusión.
    """

    print("\nExplicación:")
    print(f"Se activó la regla: {regla['nombre_regla']}")
    print("La regla se cumplió porque:")

    for condicion, valor_esperado in regla["condiciones"].items():
        valor_real = hechos.get(condicion)
        print(f"- {condicion}: esperado = {valor_esperado}, recibido = {valor_real}")


def ejecutar_tratamiento():
    print("       TRATAMIENTO DEL CONOCIMIENTO")
    print("El sistema usará hechos y reglas para obtener una conclusión.\n")

    # Estos son los hechos del caso actual.
    # Aquí simulamos que el usuario respondió estas características.
    hechos_actuales = {
        "vuela": "si",
        "overworld": "si",
        "hostil": "no",
        "decorativo": "no",
        "aparece_en_estructura": "si"
    }

    print("Hechos actuales:")

    for hecho, valor in hechos_actuales.items():
        print(f"- {hecho} = {valor}")

    conclusiones = motor_inferencia(hechos_actuales)

    print("\nResultado del motor de inferencia:")

    if conclusiones:
        for regla in conclusiones:
            print(f"\nConclusión: {regla['conclusion']}")
            modulo_explicacion(regla, hechos_actuales)
    else:
        print("No se encontró una conclusión con los hechos disponibles.")


if __name__ == "__main__":
    ejecutar_tratamiento()
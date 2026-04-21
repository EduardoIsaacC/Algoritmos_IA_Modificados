# 4. UTILIZACIÓN DEL CONOCIMIENTO
# Sistema experto - Ejemplo funcional por separado
# ¿Qué es?
# Es la parte donde el usuario interactúa con el sistema experto.
#
# ¿Para qué sirve?
# Sirve para consultar el sistema y recibir una conclusión.
#
# ¿Cómo funciona?
# El usuario responde preguntas, el sistema guarda los hechos,
# aplica reglas y muestra un resultado.
#
# Ejemplo:
# Sistema tipo Akinator para identificar mobs de Minecraft.

base_conocimiento = [
    {
        "nombre": "Allay",
        "condiciones": {
            "vuela": "si",
            "overworld": "si",
            "hostil": "no",
            "decorativo": "no",
            "aparece_en_estructura": "si"
        }
    },
    {
        "nombre": "Murciélago",
        "condiciones": {
            "vuela": "si",
            "overworld": "si",
            "hostil": "no",
            "decorativo": "si",
            "aparece_en_estructura": "no"
        }
    },
    {
        "nombre": "Creeper",
        "condiciones": {
            "vuela": "no",
            "overworld": "si",
            "hostil": "si",
            "explota": "si"
        }
    },
    {
        "nombre": "Esqueleto",
        "condiciones": {
            "vuela": "no",
            "overworld": "si",
            "hostil": "si",
            "ataca_distancia": "si"
        }
    },
    {
        "nombre": "Enderman",
        "condiciones": {
            "vuela": "no",
            "overworld": "si",
            "hostil": "no",
            "explota": "no",
            "ataca_distancia": "no"
        }
    }
]


preguntas = {
    "vuela": "¿El mob vuela?",
    "overworld": "¿El mob aparece en el Overworld?",
    "hostil": "¿El mob es hostil?",
    "decorativo": "¿El mob es decorativo?",
    "aparece_en_estructura": "¿Aparece en estructuras específicas?",
    "explota": "¿El mob explota?",
    "ataca_distancia": "¿El mob ataca a distancia?"
}


def preguntar(pregunta):
    """
    Función que simula la interfaz de usuario.
    Permite ingresar si, no o no se.
    """

    while True:
        respuesta = input(pregunta + " [si/no/no se]: ").strip().lower()

        if respuesta in ["si", "sí", "s"]:
            return "si"
        elif respuesta in ["no", "n"]:
            return "no"
        elif respuesta in ["no se", "nose", "ns"]:
            return "no se"
        else:
            print("Respuesta no válida. Escribe si, no o no se.")


def calcular_resultados(hechos_usuario):
    """
    Compara las respuestas del usuario con cada mob.
    Calcula cuál tiene más coincidencias.
    """

    resultados = []

    for mob in base_conocimiento:
        nombre = mob["nombre"]
        condiciones = mob["condiciones"]

        coincidencias = 0
        total_evaluadas = 0

        for condicion, valor_esperado in condiciones.items():
            if condicion in hechos_usuario:
                total_evaluadas += 1

                if hechos_usuario[condicion] == valor_esperado:
                    coincidencias += 1

        if total_evaluadas > 0:
            porcentaje = coincidencias / total_evaluadas
        else:
            porcentaje = 0

        resultados.append({
            "nombre": nombre,
            "coincidencias": coincidencias,
            "total_evaluadas": total_evaluadas,
            "porcentaje": porcentaje,
            "condiciones": condiciones
        })

    resultados.sort(key=lambda resultado: resultado["porcentaje"], reverse=True)

    return resultados


def mostrar_explicacion(mejor_resultado, hechos_usuario):
    """
    Módulo de explicación.
    Muestra por qué el sistema eligió ese resultado.
    """

    print("              EXPLICACIÓN")

    print("El sistema comparó tus respuestas con la base de conocimiento.")
    print(f"El resultado con mayor coincidencia fue: {mejor_resultado['nombre']}")

    print("\nTus respuestas fueron:")

    for hecho, valor in hechos_usuario.items():
        print(f"- {hecho} = {valor}")

    print("\nCaracterísticas esperadas del mob seleccionado:")

    for condicion, valor in mejor_resultado["condiciones"].items():
        print(f"- {condicion} = {valor}")


def interfaz_usuario():
    print("       UTILIZACIÓN DEL CONOCIMIENTO")
    print("Sistema experto para identificar mobs de Minecraft.")
    print("Piensa en un mob y responde las preguntas.\n")

    hechos_usuario = {}

    for clave, texto_pregunta in preguntas.items():
        respuesta = preguntar(texto_pregunta)

        if respuesta != "no se":
            hechos_usuario[clave] = respuesta

    resultados = calcular_resultados(hechos_usuario)

    mejor_resultado = resultados[0]

    print("                RESULTADO")
    print(f"El mob más probable es: {mejor_resultado['nombre']}")
    print(
        f"Coincidencias: {mejor_resultado['coincidencias']} "
        f"de {mejor_resultado['total_evaluadas']}"
    )

    mostrar_explicacion(mejor_resultado, hechos_usuario)


if __name__ == "__main__":
    interfaz_usuario()
# SISTEMA EXPERTO FUNCIONAL
# Ejemplos:
# 1. Adivinar mobs de Minecraft
# 2. Diagnosticar fallas simples en máquina de coser

def preguntar(pregunta):
    """
    Función para hacer preguntas al usuario.
    Solo acepta respuestas: si, no, no se.
    """
    while True:
        respuesta = input(pregunta + " [si/no/no se]: ").lower().strip()

        if respuesta in ["si", "sí", "s"]:
            return "si"
        elif respuesta in ["no", "n"]:
            return "no"
        elif respuesta in ["no se", "nose", "ns"]:
            return "no se"
        else:
            print("Respuesta no válida. Escribe: si, no o no se.")


# EJEMPLO 1: SISTEMA EXPERTO TIPO AKINATOR DE MOBS DE MINECRAFT

def sistema_minecraft():
    print("\n SISTEMA EXPERTO: MOBS DE MINECRAFT ")
    print("Piensa en un mob y responde las preguntas.\n")

    # BASE DE CONOCIMIENTO
    # Aquí están los mobs y sus características.
    base_conocimiento = {
        "Murciélago": {
            "vuela": "si",
            "dimension_overworld": "si",
            "hostil": "no",
            "decorativo": "si",
            "aparece_en_estructura": "no",
            "explota": "no",
            "ataca_distancia": "no"
        },
        "Allay": {
            "vuela": "si",
            "dimension_overworld": "si",
            "hostil": "no",
            "decorativo": "no",
            "aparece_en_estructura": "si",
            "explota": "no",
            "ataca_distancia": "no"
        },
        "Creeper": {
            "vuela": "no",
            "dimension_overworld": "si",
            "hostil": "si",
            "decorativo": "no",
            "aparece_en_estructura": "no",
            "explota": "si",
            "ataca_distancia": "no"
        },
        "Esqueleto": {
            "vuela": "no",
            "dimension_overworld": "si",
            "hostil": "si",
            "decorativo": "no",
            "aparece_en_estructura": "no",
            "explota": "no",
            "ataca_distancia": "si"
        },
        "Enderman": {
            "vuela": "no",
            "dimension_overworld": "si",
            "hostil": "neutral",
            "decorativo": "no",
            "aparece_en_estructura": "no",
            "explota": "no",
            "ataca_distancia": "no"
        }
    }

    # BASE DE HECHOS
    # Aquí se guardan las respuestas del usuario.
    hechos = {}

    preguntas = {
        "vuela": "¿El mob vuela?",
        "dimension_overworld": "¿El mob aparece en el Overworld?",
        "hostil": "¿El mob es hostil?",
        "decorativo": "¿El mob es decorativo?",
        "aparece_en_estructura": "¿El mob aparece en estructuras específicas?",
        "explota": "¿El mob explota?",
        "ataca_distancia": "¿El mob ataca a distancia?"
    }

    # Motor de inferencia simple:
    # Va descartando mobs según las respuestas.
    posibles_mobs = list(base_conocimiento.keys())

    for caracteristica, pregunta in preguntas.items():
        respuesta = preguntar(pregunta)

        if respuesta == "no se":
            continue

        hechos[caracteristica] = respuesta

        nuevos_posibles = []

        for mob in posibles_mobs:
            valor_mob = base_conocimiento[mob][caracteristica]

            # Caso especial para Enderman, que no es totalmente hostil,
            # sino neutral.
            if caracteristica == "hostil":
                if respuesta == "si" and valor_mob == "si":
                    nuevos_posibles.append(mob)
                elif respuesta == "no" and valor_mob in ["no", "neutral"]:
                    nuevos_posibles.append(mob)
            else:
                if valor_mob == respuesta:
                    nuevos_posibles.append(mob)

        posibles_mobs = nuevos_posibles

        if len(posibles_mobs) == 1:
            break

        if len(posibles_mobs) == 0:
            break

    print("\n RESULTADO ")

    if len(posibles_mobs) == 1:
        mob = posibles_mobs[0]
        print(f"El mob probablemente es: {mob}")

        print("\n EXPLICACIÓN ")
        print("Llegué a esta conclusión porque tus respuestas coinciden con estas características:")

        for hecho, valor in hechos.items():
            print(f"- {preguntas[hecho]} Respuesta: {valor}")

    elif len(posibles_mobs) > 1:
        print("No pude identificar un único mob.")
        print("Posibles opciones:")
        for mob in posibles_mobs:
            print(f"- {mob}")

    else:
        print("No encontré un mob que coincida con esas respuestas.")
        print("Puede faltar conocimiento en la base de conocimiento.")


# EJEMPLO 2: SISTEMA EXPERTO PARA FALLAS EN MÁQUINA DE COSER

def sistema_maquina_coser():
    print("\n SISTEMA EXPERTO: DIAGNÓSTICO DE MÁQUINA DE COSER ")
    print("Responde las preguntas según la falla de la máquina.\n")

    # BASE DE CONOCIMIENTO
    reglas = [
        {
            "nombre": "Tensión excesiva del hilo",
            "condiciones": {
                "hilo_se_rompe": "si",
                "puntada_apretada": "si"
            },
            "diagnostico": "La tensión del hilo puede estar demasiado alta.",
            "solucion": "Reduce la tensión del hilo y revisa que esté bien enhebrada."
        },
        {
            "nombre": "Aguja dañada o mal colocada",
            "condiciones": {
                "aguja_se_rompe": "si",
                "ruido_fuerte": "si"
            },
            "diagnostico": "La aguja puede estar doblada, dañada o mal colocada.",
            "solucion": "Cambia la aguja y asegúrate de colocarla correctamente."
        },
        {
            "nombre": "Falta de lubricación",
            "condiciones": {
                "ruido_fuerte": "si",
                "movimiento_pesado": "si"
            },
            "diagnostico": "La máquina puede necesitar lubricación.",
            "solucion": "Limpia la máquina y aplica aceite especial para máquinas de coser."
        },
        {
            "nombre": "Bobina mal colocada",
            "condiciones": {
                "hilo_se_enreda": "si",
                "puntada_irregular": "si"
            },
            "diagnostico": "La bobina puede estar mal colocada o mal devanada.",
            "solucion": "Retira la bobina, revisa el sentido del hilo y colócala nuevamente."
        }
    ]

    # BASE DE HECHOS
    hechos = {}

    preguntas = {
        "hilo_se_rompe": "¿El hilo se rompe constantemente?",
        "puntada_apretada": "¿La puntada sale demasiado apretada?",
        "aguja_se_rompe": "¿La aguja se rompe?",
        "ruido_fuerte": "¿La máquina hace ruido fuerte?",
        "movimiento_pesado": "¿La máquina se siente pesada al coser?",
        "hilo_se_enreda": "¿El hilo se enreda?",
        "puntada_irregular": "¿La puntada sale irregular?"
    }

    for clave, pregunta in preguntas.items():
        hechos[clave] = preguntar(pregunta)

    # MOTOR DE INFERENCIA
    diagnosticos_encontrados = []

    for regla in reglas:
        condiciones = regla["condiciones"]
        cumple = True

        for condicion, valor_esperado in condiciones.items():
            if hechos.get(condicion) != valor_esperado:
                cumple = False
                break

        if cumple:
            diagnosticos_encontrados.append(regla)

    print("\n RESULTADO ")

    if diagnosticos_encontrados:
        for regla in diagnosticos_encontrados:
            print(f"\nDiagnóstico: {regla['diagnostico']}")
            print(f"Solución recomendada: {regla['solucion']}")

            print("\nExplicación:")
            print("El sistema llegó a esta conclusión porque se cumplieron estas condiciones:")

            for condicion, valor in regla["condiciones"].items():
                print(f"- {preguntas[condicion]} Respuesta esperada: {valor}")

    else:
        print("No se encontró un diagnóstico exacto.")
        print("Puede ser necesario agregar más reglas a la base de conocimiento.")


# MENÚ PRINCIPAL

def menu():
    while True:
        print("        SISTEMA EXPERTO")
        print("1. Adivinar mob de Minecraft")
        print("2. Diagnosticar máquina de coser")
        print("3. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            sistema_minecraft()
        elif opcion == "2":
            sistema_maquina_coser()
        elif opcion == "3":
            print("Saliendo del sistema experto...")
            break
        else:
            print("Opción no válida. Intenta otra vez.")


# Ejecutar programa
menu()
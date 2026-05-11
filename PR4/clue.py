import random

def jugar_clue_wayne():
    personajes = ["Bruno", "Alfredo", "Damian", "Espejo", "Selina"]
    locaciones = ["Sala", "Cocina", "Comedor", "Dormitorio", "Cuarto Prohibido"]
    armas = ["Candelabro", "Daga", "Tubo de Plomo", "Revólver", "Cuerda"]

    # 1. Definir el crimen real en secreto
    culpable_real = random.choice(personajes)
    locacion_real = random.choice(locaciones)
    arma_real = random.choice(armas)

    # 2. Distribuir un arma en cada cuarto
    random.shuffle(armas)
    distribucion_armas = {locaciones[i]: armas[i] for i in range(5)}

    print(" BIEVENIDO A LA MANSIÓN WAYNE ")
    print("Ha ocurrido un crimen. Usa tu instinto de detective para descubrir al culpable.\n")

    # 3. Ciclo principal del juego
    jugando = True
    while jugando:
        print("\n MENÚ DE ACCIÓN ")
        print("1. Inspeccionar habitación")
        print("2. Interrogar a un gato")
        print("3. ¡Resolver el caso!")
        opcion = input("¿Qué deseas hacer? (1/2/3): ")

        if opcion == '1':
            print("\nHabitaciones disponibles: Sala, Cocina, Comedor, Dormitorio, Cuarto Prohibido")
            cuarto = input("¿Cuál quieres inspeccionar?: ")
            if cuarto in distribucion_armas:
                print(f" Inspeccionando {cuarto}...")
                print(f"Encuentras: {distribucion_armas[cuarto]}.")
                if cuarto == locacion_real:
                    print(" Pista extra: Notas marcas de garras recientes cerca de la escena.")
            else:
                print("Esa habitación no existe en la mansión.")

        elif opcion == '2':
            print("\nGatos sospechosos: Bruno, Alfredo, Damian, Espejo, Selina")
            gato = input("¿A quién deseas interrogar?: ")
            if gato in personajes:
                if gato == culpable_real:
                    print(f" {gato} (Nervioso): ¡Yo no fui! Estuve afilando mis uñas todo el tiempo.")
                else:
                    # El gato inocente da una pista real sobre un arma y su cuarto
                    cuarto_pista = random.choice(locaciones)
                    arma_pista = distribucion_armas[cuarto_pista]
                    print(f" {gato}: Yo vi claramente que {arma_pista} estaba en {cuarto_pista}.")
            else:
                print("Ese gato no está en la mansión.")

        elif opcion == '3':
            print("\n ES HORA DE DAR TU VEREDICTO ")
            acusado = input("¿Quién es el culpable?: ")
            arma_acusada = input("¿Con qué arma?: ")
            lugar_acusado = input("¿En dónde ocurrió?: ")

            # Validación de victoria
            if acusado == culpable_real and arma_acusada == arma_real and lugar_acusado == locacion_real:
                print("\n ¡CASO CERRADO! ")
                print(f"¡Correcto! Fue {culpable_real} en {locacion_real} con {arma_real}.")
                jugando = False
            else:
                print("\n VEREDICTO INCORRECTO ")
                print("Esa no es la verdad. El asesino sigue suelto. Has perdido.")
                print(f"La verdad era: {culpable_real} en {locacion_real} con {arma_real}.")
                jugando = False
        else:
            print("Opción inválida.")

# Ejecutar el juego
if __name__ == "__main__":
    jugar_clue_wayne()
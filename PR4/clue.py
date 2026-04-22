import random

def simulador_clue():
    # 1. Definir las listas (5 de cada uno)
    personajes = ["Dr. Black (Cirujano)", "Miss Scarlett (Actriz)", "Prof. Plum (Químico)", "Rev. Green (Sacerdote)", "Col. Mustard (Militar)"]
    locaciones = ["la Biblioteca", "la Cocina", "el Invernadero", "el Comedor", "el Estudio"]
    armas = ["el Candelabro", "la Daga", "el Tubo de Plomo", "el Revólver", "la Cuerda"]

    # 2. Selección aleatoria inicial
    culpable = random.choice(personajes)
    locacion = random.choice(locaciones)
    arma = random.choice(armas)

    print(" INICIANDO SIMULADOR CLUE ")
    print("Analizando pistas...\n")

    # 3. Enlaces de historias (5 casos)
    if culpable == personajes[0]:
        print(f"CASO 1: NEGLIGENCIA FATAL")
        print(f"El {culpable} silenció a la víctima en {locacion} utilizando {arma} para evitar que revelara un caso de negligencia médica pasada.")
        
    elif culpable == personajes[1]:
        print(f"CASO 2: CELOS PROFESIONALES")
        print(f"{culpable}, en un ataque de furia y celos por un papel protagónico, acorraló a la víctima en {locacion} y terminó con su vida usando {arma}.")
        
    elif culpable == personajes[2]:
        print(f"CASO 3: ROBO DE PATENTE")
        print(f"El {culpable} descubrió que la víctima le robaba su investigación. Vengó su trabajo en {locacion} empuñando {arma}.")
        
    elif culpable == personajes[3]:
        print(f"CASO 4: CHANTAJE MORAL")
        print(f"El {culpable} no soportó la extorsión sobre su turbio pasado. Para proteger su reputación de la congregación, cometió el acto en {locacion} con {arma}.")
        
    elif culpable == personajes[4]:
        print(f"CASO 5: DEUDAS DE JUEGO")
        print(f"El {culpable}, fuertemente presionado por sus deudas de apuestas, emboscó a su acreedor en {locacion} y utilizó {arma} con precisión militar.")

    print("\n FIN DEL MISTERIO ")

# Ejecutar el simulador
if __name__ == "__main__":
    simulador_clue()
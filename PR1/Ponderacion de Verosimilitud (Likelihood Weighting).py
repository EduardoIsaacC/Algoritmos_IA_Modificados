import random
from typing import Dict, Any, List

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def muestrear_bernoulli(probabilidad: float) -> bool:
    """
    Devuelve True con la probabilidad indicada.
    """
    return random.random() < probabilidad


def ponderacion_verosimilitud_convergencia(
        numero_muestras: int,
        evidencia: Dict[str, Any]
) -> List[float]:

    """
    Caso de vida diaria:

    - Lluvia
    - Hora pico
    - Trafico depende de lluvia y hora pico

    Consulta:
    P(Trafico = True | evidencia)

    Devuelve una serie de valores para mostrar
    cómo converge la probabilidad estimada.
    """

    # Probabilidades base (datos del modelo)
    prob_lluvia = 0.25
    prob_hora_pico = 0.35

    prob_trafico = {
        (False, False): 0.10,
        (False, True): 0.55,
        (True, False): 0.40,
        (True, True): 0.85
    }

    orden_variables = ["Lluvia", "HoraPico", "Trafico"]

    peso_verdadero = 0.0
    peso_falso = 0.0

    serie_convergencia = []

    for _ in range(numero_muestras):

        peso = 1.0
        muestra = {}

        for variable in orden_variables:

            if variable == "Lluvia":
                probabilidad = prob_lluvia

            elif variable == "HoraPico":
                probabilidad = prob_hora_pico

            else:
                probabilidad = prob_trafico[
                    (muestra["Lluvia"], muestra["HoraPico"])
                ]

            if variable in evidencia:

                muestra[variable] = evidencia[variable]

                peso *= (
                    probabilidad
                    if evidencia[variable]
                    else (1.0 - probabilidad)
                )

            else:
                muestra[variable] = muestrear_bernoulli(probabilidad)

        if muestra["Trafico"]:
            peso_verdadero += peso
        else:
            peso_falso += peso

        total = peso_verdadero + peso_falso

        prob_estimada = (peso_verdadero / total) if total > 0 else 0

        serie_convergencia.append(prob_estimada)

    return serie_convergencia


def main():

    random.seed(7)

    evidencia = {
        "Lluvia": True,
        "HoraPico": True
    }

    serie = ponderacion_verosimilitud_convergencia(
        numero_muestras=4000,
        evidencia=evidencia
    )

    resultado_final = serie[-1]

    print("\nResultado (entre la data):")
    print(
        "Probabilidad aproximada de Trafico=True",
        "dado Lluvia=True y HoraPico=True:",
        resultado_final
    )

    fig, ax = plt.subplots()

    ax.set_title(
        "Ponderación de Verosimilitud\n"
        "Convergencia de P(Trafico=True | Lluvia=True, HoraPico=True)"
    )

    ax.set_xlabel("Número de muestras")
    ax.set_ylabel("Probabilidad estimada")
    ax.set_ylim(0, 1)

    linea, = ax.plot([], [], linewidth=2)

    def inicializar():
        linea.set_data([], [])
        return linea,

    def actualizar(frame):

        x = list(range(1, frame + 2))
        y = serie[:frame + 1]

        linea.set_data(x, y)

        ax.set_xlim(1, max(50, frame + 2))

        return linea,

    anim = FuncAnimation(fig, actualizar, frames=len(serie), init_func=inicializar, interval=500, repeat=False)

    plt.show()


if __name__ == "__main__":
    main()
import random
from typing import Dict, Any, List, Tuple

def sample_from_bernoulli(p_true: float) -> bool:
    return random.random() < p_true

def likelihood_weighting(
    n_samples: int,
    evidence: Dict[str, Any],
    query_var: str
) -> Dict[Any, float]:
    """
    Likelihood Weighting para una red bayesiana pequeña (hardcodeada para claridad).
    Retorna distribución aproximada de query_var dado evidence.
    """

    # --- Definición de la Red Bayesiana (ejemplo) ---
    # P(Rain)
    p_rain = 0.25
    # P(RushHour)
    p_rush = 0.35
    # P(Traffic | Rain, RushHour)
    # tabla: (Rain, Rush) -> P(Traffic=True)
    p_traffic = {
        (False, False): 0.10,
        (False, True):  0.55,
        (True,  False): 0.40,
        (True,  True):  0.85
    }

    # Orden topológico (padres antes que hijos)
    variables = ["Rain", "RushHour", "Traffic"]

    # acumuladores ponderados
    weights: Dict[Any, float] = {True: 0.0, False: 0.0}

    for _ in range(n_samples):
        w = 1.0
        x: Dict[str, Any] = {}

        for var in variables:
            # Determinar P(var=True | padres)
            if var == "Rain":
                p_true = p_rain
            elif var == "RushHour":
                p_true = p_rush
            else:  # Traffic
                r = x["Rain"]
                rh = x["RushHour"]
                p_true = p_traffic[(r, rh)]

            if var in evidence:
                # Si hay evidencia, fijamos el valor y multiplicamos el peso por la verosimilitud
                x[var] = evidence[var]
                # verosimilitud: P(var=evidence | padres)
                w *= (p_true if evidence[var] is True else (1.0 - p_true))
            else:
                # Si no hay evidencia, muestreamos normalmente
                x[var] = sample_from_bernoulli(p_true)

        # sumar peso al valor observado de la variable consulta
        weights[x[query_var]] += w

    # normalizar
    total = weights[True] + weights[False]
    if total == 0:
        return {True: 0.0, False: 0.0}
    return {k: v / total for k, v in weights.items()}


if __name__ == "__main__":
    random.seed(7)

    evidence = {"Rain": True, "RushHour": True}
    dist = likelihood_weighting(n_samples=20000, evidence=evidence, query_var="Traffic")

    print("Aprox P(Traffic | Rain=True, RushHour=True):")
    print(dist)
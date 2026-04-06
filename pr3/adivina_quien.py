import json
import os

# Archivo donde se guardará el "cerebro" (el árbol de decisión)
ARCHIVO_DATOS = "conocimiento_animales.json"

class Nodo:
    """Clase que representa una pregunta o un animal en el árbol de decisión."""
    def __init__(self, texto, es_hoja=False):
        self.texto = texto
        self.es_hoja = es_hoja # True si es un animal final, False si es una pregunta
        self.si = None
        self.no = None

    def a_diccionario(self):
        """Convierte el nodo (y sus hijos) a un diccionario para guardarlo en JSON."""
        if self.es_hoja:
            return {"texto": self.texto, "es_hoja": True}
        return {
            "texto": self.texto,
            "es_hoja": False,
            "si": self.si.a_diccionario() if self.si else None,
            "no": self.no.a_diccionario() if self.no else None
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Reconstruye el árbol de nodos a partir de un diccionario."""
        nodo = cls(datos["texto"], datos["es_hoja"])
        if not datos["es_hoja"]:
            nodo.si = cls.desde_diccionario(datos["si"])
            nodo.no = cls.desde_diccionario(datos["no"])
        return nodo

def guardar_conocimiento(raiz):
    """Guarda el árbol en un archivo JSON."""
    with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
        json.dump(raiz.a_diccionario(), f, ensure_ascii=False, indent=4)

def cargar_conocimiento():
    """Carga el árbol desde el archivo JSON si existe. Si no, crea uno básico."""
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return Nodo.desde_diccionario(datos)
    else:
        # Base de conocimiento inicial
        raiz = Nodo("¿Es un mamífero?")
        raiz.si = Nodo("Perro", es_hoja=True)
        raiz.no = Nodo("Cocodrilo", es_hoja=True)
        return raiz

def aprender(nodo_actual):
    """Lógica para que el sistema aprenda un nuevo animal."""
    print("\n¡Oh no! Me has ganado. Ayúdame a aprender.")
    nuevo_animal = input("¿En qué animal estabas pensando?: ").strip().capitalize()
    
    print(f"\nEscribe una pregunta de Sí/No que me ayude a distinguir a un(a) '{nuevo_animal}' de un(a) '{nodo_actual.texto}'.")
    print("Ejemplo: ¿Puede volar?")
    nueva_pregunta = input("Pregunta: ").strip()
    
    # Asegurarse de que tenga signos de interrogación (opcional, pero se ve mejor)
    if not nueva_pregunta.startswith("¿"): nueva_pregunta = "¿" + nueva_pregunta
    if not nueva_pregunta.endswith("?"): nueva_pregunta = nueva_pregunta + "?"

    respuesta_nuevo = input(f"Para un(a) '{nuevo_animal}', ¿la respuesta a esa pregunta es Sí (s) o No (n)?: ").strip().lower()

    # Guardar el animal que el sistema intentó adivinar
    animal_viejo = nodo_actual.texto

    # Transformar el nodo actual (que era una hoja) en una nueva pregunta
    nodo_actual.texto = nueva_pregunta
    nodo_actual.es_hoja = False

    # Asignar los hijos dependiendo de la respuesta
    if respuesta_nuevo == 's':
        nodo_actual.si = Nodo(nuevo_animal, es_hoja=True)
        nodo_actual.no = Nodo(animal_viejo, es_hoja=True)
    else:
        nodo_actual.no = Nodo(nuevo_animal, es_hoja=True)
        nodo_actual.si = Nodo(animal_viejo, es_hoja=True)
        
    print("\n¡Excelente! He aprendido algo nuevo.")

def jugar(nodo):
    """Función recursiva para navegar por el árbol."""
    if nodo.es_hoja:
        respuesta = input(f"¿Estás pensando en un(a) {nodo.texto}? (s/n): ").strip().lower()
        if respuesta == 's':
            print("¡Jaja! ¡Te he ganado! Soy un genio.")
        else:
            aprender(nodo)
    else:
        respuesta = input(f"{nodo.texto} (s/n): ").strip().lower()
        if respuesta == 's':
            jugar(nodo.si)
        elif respuesta == 'n':
            jugar(nodo.no)
        else:
            print("Por favor, responde 's' para Sí o 'n' para No.")
            jugar(nodo) # Repetir la pregunta si meten un dato inválido

def main():
    print("   BIENVENIDO A 'ADIVINA QUIÉN'   ")
    print("        TEMA: ANIMALES        ")
    print("Piensa en un animal e intentaré adivinarlo.\n")
    
    raiz_arbol = cargar_conocimiento()
    
    jugando = True
    while jugando:
        jugar(raiz_arbol)
        
        # Guardar automáticamente después de cada partida para no perder el progreso
        guardar_conocimiento(raiz_arbol)
        
        otra = input("\n¿Quieres jugar otra vez? (s/n): ").strip().lower()
        if otra != 's':
            jugando = False
            print("¡Gracias por jugar! Mi cerebro ha sido guardado.")

if __name__ == "__main__":
    main()
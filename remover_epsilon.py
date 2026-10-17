"""Lectura de gramáticas y eliminación de producciones épsilon."""

from itertools import combinations
from pathlib import Path
import re

EPSILONS = ("", "ϵ", "ε")
PATRON = re.compile(
    r"^[A-Z][A-Za-z0-9 ]* → (?:[A-Za-z0-9]+(?: +[A-Za-z0-9]+)*|[ϵε])"
    r"(?: ?\| ?(?:[A-Za-z0-9]+(?: +[A-Za-z0-9]+)*|[ϵε]))*$"
)


def cargar_gramatica(ruta):
    """Devuelve el diccionario de producciones y la lista inicial de anulables.

    Como en el archivo original, los espacios en nombres como N P se eliminan.
    El primer lado izquierdo es el símbolo inicial.
    """
    gramatica = {}
    epsilons = []
    errores = []
    for numero, linea in enumerate(Path(ruta).read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip():
            continue
        if not PATRON.fullmatch(linea):
            errores.append(f"error en la línea {numero}: {linea!r}")
            continue
        izquierda, derecha = linea.split("→", 1)
        izquierda = izquierda.replace(" ", "")
        producciones = gramatica.setdefault(izquierda, [])
        for alternativa in derecha.split("|"):
            produccion = alternativa.replace(" ", "")
            if produccion not in producciones:
                producciones.append(produccion)
            if produccion in EPSILONS and izquierda not in epsilons:
                epsilons.append(izquierda)
    if errores:
        raise ValueError("\n".join(errores) + "\ngramática inválida")
    if not gramatica:
        raise ValueError("La gramática está vacía")
    return gramatica, epsilons


def simbolos_produccion(produccion, no_terminales):
    """Reconoce nombres completos (NP, VP, Det), prefiriendo el más largo.

    Los espacios son decorativos. Los demás caracteres son símbolos simples;
    una mayúscula sin definición sigue siendo un no terminal sin producciones.
    """
    texto = produccion.replace(" ", "")
    if texto in EPSILONS:
        return ()
    nombres = sorted(no_terminales, key=lambda nombre: (-len(nombre), nombre))
    simbolos = []
    posicion = 0
    while posicion < len(texto):
        simbolo = next(
            (nombre for nombre in nombres if texto.startswith(nombre, posicion)),
            texto[posicion],
        )
        simbolos.append(simbolo)
        posicion += len(simbolo)
    return tuple(simbolos)


def remover_epsilons(gram, lista):
    """Elimina épsilon y agrega variantes omitiendo símbolos anulables.

    Actualiza lista con todos los anulables y devuelve un diccionario nuevo.
    Conserva el comportamiento original de eliminar también el épsilon inicial.
    """
    anulables = set(lista)
    cambio = True
    while cambio:
        cambio = False
        for letra, producciones in gram.items():
            if letra in anulables:
                continue
            if any(all(s in anulables for s in simbolos_produccion(p, gram))
                   for p in producciones):
                anulables.add(letra)
                cambio = True
    for letra in gram:
        if letra in anulables and letra not in lista:
            lista.append(letra)

    resultado = {letra: [] for letra in gram}
    for letra, producciones in gram.items():
        for produccion in producciones:
            simbolos = simbolos_produccion(produccion, gram)
            posiciones = [i for i, s in enumerate(simbolos) if s in anulables]
            for cantidad in range(len(posiciones) + 1):
                for omitidas in combinations(posiciones, cantidad):
                    nueva = "".join(s for i, s in enumerate(simbolos) if i not in omitidas)
                    if nueva and nueva not in resultado[letra]:
                        resultado[letra].append(nueva)
    return resultado


if __name__ == "__main__":
    gramatica, epsilons = cargar_gramatica(Path(__file__).with_name("gramatica.txt"))
    print("Gramática sin producciones ϵ:", remover_epsilons(gramatica, epsilons))

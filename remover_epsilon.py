"""Lectura por palabras y eliminación de producciones épsilon."""

from itertools import combinations
from pathlib import Path
import re

EPSILONS = ("", "ϵ", "ε")


def simbolos_produccion(produccion, no_terminales):
    if isinstance(produccion, (tuple, list)):
        return tuple(produccion)

    texto = produccion.replace(" ", "")

    if texto in EPSILONS:
        return ()

    nombres = sorted(no_terminales, key=lambda n: (-len(n), n))
    simbolos = []
    posicion = 0

    while posicion < len(texto):
        nombre = next(
            (n for n in nombres if texto.startswith(n, posicion)),
            None,
        )

        if nombre is not None:
            simbolos.append(nombre)
            posicion += len(nombre)
        else:
            coincidencia = re.match(r"[a-z0-9]+", texto[posicion:])

            if coincidencia:
                palabra = coincidencia.group()
                simbolos.append(palabra)
                posicion += len(palabra)
            elif texto[posicion].isupper():
                simbolos.append(texto[posicion])
                posicion += 1
            else:
                raise ValueError(
                    f"Símbolo inválido en: {produccion!r}"
                )

    return tuple(simbolos)


def cargar_gramatica(ruta):
    pendientes = {}

    lineas = Path(ruta).read_text(
        encoding="utf-8-sig"
    ).splitlines()

    for numero, linea in enumerate(lineas, 1):
        if not linea.strip():
            continue

        if linea.count("→") != 1:
            raise ValueError(
                f"Se necesita una flecha → en la línea {numero}"
            )

        izquierda, derecha = linea.split("→")
        izquierda = izquierda.replace(" ", "").strip()

        if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", izquierda):
            raise ValueError(
                f"No terminal inválido en línea {numero}"
            )

        for alternativa in derecha.split("|"):
            texto = alternativa.strip()

            if not texto:
                raise ValueError(
                    f"Alternativa vacía en línea {numero}; usa ε"
                )

            pendientes.setdefault(izquierda, []).append(texto)

    if not pendientes:
        raise ValueError("La gramática está vacía")

    gramatica = {}
    anulables = []

    for variable, alternativas in pendientes.items():
        gramatica[variable] = []

        for alternativa in alternativas:
            simbolos = simbolos_produccion(
                alternativa, pendientes
            )

            if simbolos not in gramatica[variable]:
                gramatica[variable].append(simbolos)

            if not simbolos and variable not in anulables:
                anulables.append(variable)

    return gramatica, anulables


def remover_epsilons(gram, lista):
    anulables = set(lista)
    cambio = True

    while cambio:
        cambio = False

        for variable, producciones in gram.items():
            if variable in anulables:
                continue

            if any(
                all(s in anulables for s in p)
                for p in producciones
            ):
                anulables.add(variable)
                cambio = True

    lista[:] = [v for v in gram if v in anulables]
    resultado = {v: [] for v in gram}

    for variable, producciones in gram.items():
        for produccion in producciones:
            posiciones = [
                i
                for i, simbolo in enumerate(produccion)
                if simbolo in anulables
            ]

            for cantidad in range(len(posiciones) + 1):
                for omitidas in combinations(
                    posiciones, cantidad
                ):
                    nueva = tuple(
                        s
                        for i, s in enumerate(produccion)
                        if i not in omitidas
                    )

                    if nueva and nueva not in resultado[variable]:
                        resultado[variable].append(nueva)

    return resultado
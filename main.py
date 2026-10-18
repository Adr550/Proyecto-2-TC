"""Simplificación, Chomsky y CYK para frases en inglés."""

import argparse
from pathlib import Path
from time import perf_counter

from remover_epsilon import cargar_gramatica, remover_epsilons
from remover_unarias import (
    remover_unarias,
    remover_inutiles,
    remover_inalcanzables,
)
from chomsky import convertir_a_chomsky
from entrada import tokenizar_frase
from cyk import cyk, mostrar_tabla
from arbol import construir_arbol, mostrar_arbol


def mostrar_gramatica(titulo, gramatica):
    print(f"\n{titulo}")

    if not gramatica:
        print("∅")

    for variable, producciones in gramatica.items():
        alternativas = [
            " ".join(p) if p else "ε"
            for p in producciones
        ]
        derecha = " | ".join(alternativas) or "∅"
        print(f"{variable} → {derecha}")


def main():
    parser = argparse.ArgumentParser(
        description="Analizador de frases con CYK"
    )
    parser.add_argument(
        "archivo",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("gramatica.txt"),
    )
    parser.add_argument(
        "-c",
        "--cadena",
        "--frase",
        dest="frase",
    )
    parser.add_argument(
        "--pasos",
        action="store_true",
        help="Muestra las etapas de simplificación y Chomsky.",
    )
    parser.add_argument(
        "--tabla",
        action="store_true",
        help="Muestra la tabla CYK.",
    )
    argumentos = parser.parse_args()

    try:
        gramatica, anulables = cargar_gramatica(
            argumentos.archivo
        )
        inicial = next(iter(gramatica))

        if argumentos.pasos:
            mostrar_gramatica(
                "Gramática original:", gramatica
            )

        sin_epsilon = remover_epsilons(
            gramatica, anulables
        )
        acepta_vacia = inicial in anulables

        sin_unarias = remover_unarias(sin_epsilon)
        sin_inutiles = remover_inutiles(sin_unarias)
        simplificada = remover_inalcanzables(
            sin_inutiles, inicial
        )

        cnf, nuevo_inicial = convertir_a_chomsky(
            simplificada,
            inicial,
            acepta_vacia=acepta_vacia,
        )

        if argumentos.pasos:
            for titulo, etapa in (
                ("Sin épsilon:", sin_epsilon),
                ("Sin unarias:", sin_unarias),
                ("Sin inútiles:", sin_inutiles),
                ("Sin inalcanzables:", simplificada),
                ("Forma normal de Chomsky:", cnf),
            ):
                mostrar_gramatica(titulo, etapa)

        frase = argumentos.frase

        if frase is None:
            frase = input("Ingresa una frase en inglés: ")

        palabras = tokenizar_frase(frase)

        inicio_tiempo = perf_counter()

        aceptada, tabla = cyk(
            cnf, nuevo_inicial, palabras
        )

        segundos = perf_counter() - inicio_tiempo

        print("\nSÍ" if aceptada else "\nNO")
        print(
            f"Tiempo de CYK: {segundos * 1000:.6f} ms"
        )

        if argumentos.tabla:
            mostrar_tabla(palabras, tabla)

        if aceptada:
            print(
                "\nÁrbol de análisis "
                "(gramática Chomsky):"
            )
            arbol = construir_arbol(
                tabla,
                nuevo_inicial,
                len(palabras),
            )
            mostrar_arbol(arbol)
        else:
            print(
                "No hay árbol de análisis para esta frase."
            )

        return aceptada

    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
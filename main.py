"""Simplificación, conversión a Chomsky y reconocimiento con CYK."""

import argparse
from pathlib import Path

from remover_epsilon import cargar_gramatica, remover_epsilons
from remover_unarias import (
    remover_unarias,
    remover_inutiles,
    remover_inalcanzables,
)
from chomsky import convertir_a_chomsky
from cyk import cyk, mostrar_tabla


def mostrar_gramatica(titulo, gramatica):
    print(f"\n{titulo}")

    if not gramatica:
        print("∅")
        return

    for variable, producciones in gramatica.items():
        alternativas = []

        for produccion in producciones:
            if isinstance(produccion, tuple):
                texto = " ".join(produccion) if produccion else "ε"
            else:
                texto = produccion if produccion else "ε"

            alternativas.append(texto)

        derecha = " | ".join(alternativas) if alternativas else "∅"
        print(f"{variable} → {derecha}")


def main():
    parser = argparse.ArgumentParser(
        description="Simplifica una gramática, la convierte a Chomsky "
                    "y analiza una cadena con CYK."
    )
    parser.add_argument(
        "archivo",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("gramatica.txt"),
        help="Archivo de la gramática.",
    )
    parser.add_argument(
        "-c",
        "--cadena",
        default=None,
        help="Cadena que se analizará con CYK.",
    )
    argumentos = parser.parse_args()

    try:
        gramatica, epsilons = cargar_gramatica(argumentos.archivo)
        inicial = next(iter(gramatica))

        mostrar_gramatica("Gramática original:", gramatica)

        sin_epsilons = remover_epsilons(gramatica, epsilons)

        # remover_epsilons agrega todos los anulables a esta lista.
        acepta_vacia = inicial in epsilons

        mostrar_gramatica(
            "Sin producciones épsilon:", sin_epsilons
        )

        sin_unarias = remover_unarias(sin_epsilons)
        mostrar_gramatica(
            "Sin producciones unarias:", sin_unarias
        )

        sin_inutiles = remover_inutiles(sin_unarias)
        mostrar_gramatica(
            "Sin producciones inútiles:", sin_inutiles
        )

        simplificada = remover_inalcanzables(sin_inutiles, inicial)
        mostrar_gramatica(
            "Sin producciones inalcanzables:", simplificada
        )

        gramatica_chomsky, inicial_chomsky = convertir_a_chomsky(
            simplificada,
            inicial,
            acepta_vacia=acepta_vacia,
        )

        mostrar_gramatica(
            "Gramática en forma normal de Chomsky:",
            gramatica_chomsky,
        )
        print(f"\nNuevo símbolo inicial: {inicial_chomsky}")

        cadena = argumentos.cadena

        if cadena is None:
            cadena = input(
                "\nCadena a evaluar con CYK "
                "(Enter para cadena vacía): "
            )

        aceptada, tabla = cyk(
            gramatica_chomsky,
            inicial_chomsky,
            cadena,
        )

        mostrar_tabla(cadena, tabla)

        print(f"\nCadena evaluada: {cadena!r}")

        if aceptada:
            print("ACEPTADA: la cadena pertenece al lenguaje.")
        else:
            print("RECHAZADA: la cadena no pertenece al lenguaje.")

        return aceptada

    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
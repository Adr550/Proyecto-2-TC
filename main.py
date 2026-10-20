"""Análisis de frases con explicación de las reglas utilizadas."""

import argparse
from contextlib import redirect_stdout
from io import StringIO
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
from explicar_chomsky import explicar_chomsky


def main():
    parser = argparse.ArgumentParser(
        description="Analizador de frases con CYK"
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
        "--frase",
        dest="frase",
        help="Frase que se analizará.",
    )
    parser.add_argument(
        "--tabla",
        action="store_true",
        help="Muestra la tabla CYK.",
    )
    argumentos = parser.parse_args()

    try:
        # Primero solicitar la oración.
        frase = argumentos.frase

        if frase is None:
            frase = input(
                "Ingresa una frase en inglés: "
            )

        palabras = tokenizar_frase(frase)

        print(
            "\nFrase normalizada:",
            " ".join(palabras) if palabras else "ε",
        )

        # Preparar la gramática.
        gramatica, anulables = cargar_gramatica(
            argumentos.archivo
        )
        inicial = next(iter(gramatica))

        sin_epsilon = remover_epsilons(
            gramatica, anulables
        )
        acepta_vacia = inicial in anulables

        sin_unarias = remover_unarias(sin_epsilon)
        sin_inutiles = remover_inutiles(sin_unarias)
        simplificada = remover_inalcanzables(
            sin_inutiles, inicial
        )

        # Ocultar los mensajes generales de la conversión.
        with redirect_stdout(StringIO()):
            cnf, nuevo_inicial = convertir_a_chomsky(
                simplificada,
                inicial,
                acepta_vacia=acepta_vacia,
            )

        # Analizar la oración.
        inicio_tiempo = perf_counter()

        aceptada, tabla = cyk(
            cnf,
            nuevo_inicial,
            palabras,
        )

        segundos = perf_counter() - inicio_tiempo

        print(
            "\nResultado:",
            "SÍ" if aceptada else "NO",
        )
        print(
            f"Tiempo de CYK: {segundos * 1000:.6f} ms"
        )

        if argumentos.tabla:
            mostrar_tabla(palabras, tabla)

        if aceptada:
            arbol = construir_arbol(
                tabla,
                nuevo_inicial,
                len(palabras),
            )

            # Explicar solo las reglas usadas para esta oración.
            explicar_chomsky(arbol)

            print("\nÁrbol de análisis:")
            mostrar_arbol(arbol)

        else:
            print(
                "\nNo existe una derivación completa "
                "para esta oración con la gramática."
            )

            vocabulario = {
                produccion[0]
                for producciones in cnf.values()
                for produccion in producciones
                if len(produccion) == 1
                and produccion[0] not in cnf
            }

            desconocidas = sorted(
                set(palabras) - vocabulario
            )

            if desconocidas:
                print(
                    "Palabras fuera del vocabulario:",
                    ", ".join(desconocidas),
                )
            elif not palabras:
                print(
                    "La gramática no permite "
                    "la cadena vacía."
                )
            else:
                print(
                    "Las palabras están en el vocabulario, "
                    "pero su combinación no está permitida "
                    "por las reglas."
                )

        return aceptada

    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
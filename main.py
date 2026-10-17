"""Ejecuta las etapas de simplificación de la gramática."""

import argparse
from pathlib import Path

from remover_epsilon import cargar_gramatica, remover_epsilons
from remover_unarias import remover_unarias, remover_inutiles, remover_inalcanzables


def mostrar_gramatica(titulo, gramatica):
    print(f"\n{titulo}")
    if not gramatica:
        print("∅ (lenguaje vacío después de eliminar épsilon)")
    for letra, producciones in gramatica.items():
        print(f"{letra} → {' | '.join(producciones) if producciones else '∅'}")


def main():
    parser = argparse.ArgumentParser(description="Simplifica una gramática libre de contexto")
    parser.add_argument("archivo", nargs="?", type=Path,
                        default=Path(__file__).with_name("gramatica.txt"))
    argumentos = parser.parse_args()
    try:
        gramatica, epsilons = cargar_gramatica(argumentos.archivo)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    inicial = next(iter(gramatica))
    mostrar_gramatica("Gramática original:", gramatica)
    sin_epsilons = remover_epsilons(gramatica, epsilons)
    mostrar_gramatica("Sin producciones épsilon:", sin_epsilons)
    sin_unarias = remover_unarias(sin_epsilons)
    mostrar_gramatica("Sin producciones unarias:", sin_unarias)
    sin_inutiles = remover_inutiles(sin_unarias)
    mostrar_gramatica("Sin producciones inútiles (no generadoras):", sin_inutiles)
    resultado = remover_inalcanzables(sin_inutiles, inicial)
    mostrar_gramatica("Gramática final sin producciones inalcanzables:", resultado)
    return resultado


if __name__ == "__main__":
    main()

"""Explica las reglas de Chomsky utilizadas en una oración."""


def explicar_chomsky(arbol):
    print("\nPasos para reconocer tu oración con Chomsky:")
    numero = 0

    def recorrer(nodo):
        nonlocal numero

        if isinstance(nodo, str):
            return [nodo]

        variable, hijos = nodo

        # Regla terminal: A → palabra.
        if len(hijos) == 1 and isinstance(hijos[0], str):
            palabra = hijos[0]
            numero += 1

            print(
                f"\nPaso {numero}: "
                f"{variable} → {palabra}"
            )

            if palabra == "ε":
                print("  Genera la cadena vacía.")
                return []

            print(
                f"  Reconoce '{palabra}' "
                f"mediante la variable {variable}."
            )
            return [palabra]

        # Primero explicar las partes de la producción.
        palabras = []
        partes = []
        variables = []

        for hijo in hijos:
            palabras_hijo = recorrer(hijo)

            palabras.extend(palabras_hijo)
            partes.append(" ".join(palabras_hijo))
            variables.append(hijo[0])

        numero += 1

        print(
            f"\nPaso {numero}: "
            f"{variable} → {' '.join(variables)}"
        )

        for nombre, texto in zip(variables, partes):
            print(f"  {nombre} representa: '{texto}'")

        print(
            f"  Al combinar esas partes, "
            f"{variable} reconoce: '{' '.join(palabras)}'"
        )

        return palabras

    palabras = recorrer(arbol)

    print(
        "\nLa oración completa queda reconocida "
        f"por el símbolo inicial {arbol[0]}."
    )
    print(
        "Oración:",
        " ".join(palabras) if palabras else "ε",
    )
"""CYK por palabras con referencias para reconstruir un árbol."""


def cyk(gramatica, inicial, palabras):
    """Devuelve (aceptada, tabla).

    Cada celda es un diccionario:
        variable -> referencia de derivación

    Referencia terminal:
        (palabra,)

    Referencia binaria:
        (posición_del_corte, variable_izquierda, variable_derecha)
    """
    if isinstance(palabras, str):
        raise ValueError(
            "CYK espera una lista de palabras, no un texto."
        )

    terminales = {}
    binarias = {}

    for variable, producciones in gramatica.items():
        for produccion in producciones:
            if not produccion:
                if variable != inicial:
                    raise ValueError(
                        "Épsilon fuera del símbolo inicial."
                    )

            elif (
                len(produccion) == 1
                and produccion[0] not in gramatica
            ):
                terminales.setdefault(
                    produccion[0], set()
                ).add(variable)

            elif (
                len(produccion) == 2
                and all(s in gramatica for s in produccion)
                and inicial not in produccion
            ):
                binarias.setdefault(
                    tuple(produccion), set()
                ).add(variable)

            else:
                raise ValueError(
                    f"Regla fuera de Chomsky: "
                    f"{variable} → {produccion}"
                )

    cantidad = len(palabras)

    if cantidad == 0:
        return () in gramatica.get(inicial, []), []

    tabla = [
        [{} for _ in range(cantidad)]
        for _ in range(cantidad)
    ]

    # Caso base: subfrases de una palabra.
    for indice, palabra in enumerate(palabras):
        for variable in sorted(
            terminales.get(palabra, set())
        ):
            tabla[indice][indice][variable] = (palabra,)

    # Construcción de soluciones a partir de subfrases menores.
    for longitud in range(2, cantidad + 1):
        for inicio in range(cantidad - longitud + 1):
            fin = inicio + longitud - 1

            for corte in range(inicio, fin):
                for izquierda in tabla[inicio][corte]:
                    for derecha in tabla[corte + 1][fin]:
                        variables = binarias.get(
                            (izquierda, derecha), set()
                        )

                        for variable in sorted(variables):
                            # Guardamos una derivación por variable.
                            tabla[inicio][fin].setdefault(
                                variable,
                                (corte, izquierda, derecha),
                            )

    aceptada = inicial in tabla[0][cantidad - 1]
    return aceptada, tabla


def mostrar_tabla(palabras, tabla):
    print("\nTabla CYK:")

    for longitud in range(1, len(palabras) + 1):
        for inicio in range(len(palabras) - longitud + 1):
            fin = inicio + longitud - 1

            variables = (
                ", ".join(sorted(tabla[inicio][fin]))
                or "∅"
            )
            texto = " ".join(palabras[inicio:fin + 1])

            print(
                f"[{inicio}, {fin}] "
                f"{texto!r}: {variables}"
            )
"""Reconocimiento de cadenas mediante el algoritmo CYK."""


def cyk(gramatica, inicial, cadena):
    """Devuelve (aceptada, tabla).

    La gramática debe estar en forma normal de Chomsky.
    tabla[i][j] contiene las variables que generan cadena[i:j + 1].
    """
    terminales = {}
    binarias = {}

    # Crear índices para consultar las reglas rápidamente.
    for variable, producciones in gramatica.items():
        for produccion in producciones:
            if len(produccion) == 0:
                if variable != inicial:
                    raise ValueError(
                        "Solo el símbolo inicial puede producir épsilon."
                    )

            elif len(produccion) == 1:
                terminal = produccion[0]

                if terminal in gramatica or len(terminal) != 1:
                    raise ValueError(
                        f"Producción fuera de Chomsky: "
                        f"{variable} → {produccion}"
                    )

                terminales.setdefault(terminal, set()).add(variable)

            elif len(produccion) == 2:
                if any(s not in gramatica for s in produccion):
                    raise ValueError(
                        f"Producción fuera de Chomsky: "
                        f"{variable} → {produccion}"
                    )

                if inicial in produccion:
                    raise ValueError(
                        "El símbolo inicial no debe aparecer "
                        "en el lado derecho."
                    )

                binarias.setdefault(tuple(produccion), set()).add(variable)

            else:
                raise ValueError(
                    f"Producción fuera de Chomsky: "
                    f"{variable} → {produccion}"
                )

    if cadena == "":
        return () in gramatica.get(inicial, []), []

    longitud = len(cadena)
    tabla = [
        [set() for _ in range(longitud)]
        for _ in range(longitud)
    ]

    # Subcadenas de un carácter.
    for indice, caracter in enumerate(cadena):
        tabla[indice][indice].update(
            terminales.get(caracter, set())
        )

    # Subcadenas de longitud 2, 3, ..., n.
    for tamanio in range(2, longitud + 1):
        for inicio in range(longitud - tamanio + 1):
            fin = inicio + tamanio - 1

            for corte in range(inicio, fin):
                izquierda = tabla[inicio][corte]
                derecha = tabla[corte + 1][fin]

                for variable_izquierda in izquierda:
                    for variable_derecha in derecha:
                        tabla[inicio][fin].update(
                            binarias.get(
                                (variable_izquierda, variable_derecha),
                                set(),
                            )
                        )

    aceptada = inicial in tabla[0][longitud - 1]
    return aceptada, tabla


def mostrar_tabla(cadena, tabla):
    """Muestra las celdas agrupadas por longitud de subcadena."""
    print("\nTabla CYK:")

    if not cadena:
        print("La cadena vacía se verifica con la regla inicial → ε.")
        return

    for tamanio in range(1, len(cadena) + 1):
        print(f"\nSubcadenas de longitud {tamanio}:")

        for inicio in range(len(cadena) - tamanio + 1):
            fin = inicio + tamanio - 1
            variables = ", ".join(sorted(tabla[inicio][fin]))
            contenido = "{" + variables + "}" if variables else "∅"

            print(
                f"  [{inicio}, {fin}] "
                f"{cadena[inicio:fin + 1]!r}: {contenido}"
            )
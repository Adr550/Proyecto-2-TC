"""Reconstrucción e impresión del árbol de análisis."""


def construir_arbol(tabla, inicial, cantidad_palabras):
    if cantidad_palabras == 0:
        return inicial, ["ε"]

    def visitar(variable, inicio, fin):
        referencia = tabla[inicio][fin][variable]

        if len(referencia) == 1:
            return variable, [referencia[0]]

        corte, izquierda, derecha = referencia

        return variable, [
            visitar(izquierda, inicio, corte),
            visitar(derecha, corte + 1, fin),
        ]

    return visitar(inicial, 0, cantidad_palabras - 1)


def mostrar_arbol(arbol, nivel=0):
    if isinstance(arbol, str):
        print("  " * nivel + arbol)
        return

    variable, hijos = arbol
    print("  " * nivel + variable)

    for hijo in hijos:
        mostrar_arbol(hijo, nivel + 1)
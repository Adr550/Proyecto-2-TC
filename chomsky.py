"""Conversión de una gramática simplificada a forma normal de Chomsky."""

from remover_epsilon import simbolos_produccion


def convertir_a_chomsky(gramatica, inicial, acepta_vacia=False):
    """Devuelve (gramatica_chomsky, nuevo_inicial).

    Recibe una gramática sin épsilon, unarias ni variables inútiles.
    Las producciones resultantes son tuplas de símbolos.
    """
    resultado = {}
    usados = set(gramatica)
    usados.add(inicial)
    contador = 0

    def nueva_variable():
        nonlocal contador

        while True:
            nombre = f"X{contador}"
            contador += 1

            if nombre not in usados:
                usados.add(nombre)
                return nombre

    def agregar(variable, produccion):
        alternativas = resultado.setdefault(variable, [])

        if produccion not in alternativas:
            alternativas.append(produccion)

    # El nuevo inicial nunca aparece en el lado derecho.
    nuevo_inicial = nueva_variable()
    resultado[nuevo_inicial] = []

    # Una misma variable auxiliar puede representar el mismo terminal
    # en diferentes producciones.
    auxiliares_terminales = {}

    for variable, producciones in gramatica.items():
        resultado.setdefault(variable, [])

        for produccion in producciones:
            simbolos = simbolos_produccion(produccion, gramatica)

            if not simbolos:
                raise ValueError(
                    "Primero debes eliminar las producciones épsilon."
                )

            for simbolo in simbolos:
                if simbolo not in gramatica and simbolo[0].isupper():
                    raise ValueError(
                        f"No terminal sin definición: {simbolo}"
                    )

            if len(simbolos) == 1:
                if simbolos[0] in gramatica:
                    raise ValueError(
                        "Primero debes eliminar las producciones unarias."
                    )

                agregar(variable, simbolos)
                continue

            # En una producción de longitud >= 2, todos los símbolos
            # deben ser no terminales.
            normalizados = []

            for simbolo in simbolos:
                if simbolo in gramatica:
                    normalizados.append(simbolo)
                    continue

                if simbolo not in auxiliares_terminales:
                    auxiliar = nueva_variable()
                    auxiliares_terminales[simbolo] = auxiliar
                    agregar(auxiliar, (simbolo,))

                normalizados.append(auxiliares_terminales[simbolo])

            # A → B C D se transforma en:
            # A → B X
            # X → C D
            actual = variable

            for indice in range(len(normalizados) - 2):
                auxiliar = nueva_variable()
                agregar(actual, (normalizados[indice], auxiliar))
                actual = auxiliar

            agregar(actual, tuple(normalizados[-2:]))

    # Copiamos las alternativas del inicial original.
    # No agregamos una producción unaria nuevo_inicial → inicial.
    for produccion in resultado.get(inicial, []):
        agregar(nuevo_inicial, produccion)

    if acepta_vacia:
        agregar(nuevo_inicial, ())

    return resultado, nuevo_inicial
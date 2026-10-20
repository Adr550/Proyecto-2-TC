"""Conversión a Chomsky mostrando las transformaciones."""


from remover_epsilon import simbolos_produccion


def convertir_a_chomsky(
    gramatica,
    inicial,
    acepta_vacia=False,
    mostrar_pasos=True,
):
    resultado = {}
    usados = set(gramatica)
    usados.add(inicial)
    contador = 0

    def informar(mensaje):
        if mostrar_pasos:
            print(mensaje)

    def representar(simbolos):
        return " ".join(simbolos) if simbolos else "ε"

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

    informar("\n========== CONVERSIÓN A CHOMSKY ==========")

    nuevo_inicial = nueva_variable()
    resultado[nuevo_inicial] = []

    informar("\nPaso 1: crear un nuevo símbolo inicial.")
    informar(f"  Símbolo original: {inicial}")
    informar(f"  Nuevo símbolo: {nuevo_inicial}")
    informar(
        "  Sus alternativas se copiarán al terminar, "
        "sin introducir una regla unaria."
    )

    auxiliares_terminales = {}

    informar("\nPaso 2: revisar y transformar las producciones.")

    for variable, producciones in gramatica.items():
        resultado.setdefault(variable, [])

        for produccion in producciones:
            simbolos = simbolos_produccion(
                produccion, gramatica
            )

            informar(
                f"\n  Analizando: "
                f"{variable} → {representar(simbolos)}"
            )

            if not simbolos:
                raise ValueError(
                    "Primero debes eliminar las producciones épsilon."
                )

            for simbolo in simbolos:
                if (
                    simbolo not in gramatica
                    and simbolo[0].isupper()
                ):
                    raise ValueError(
                        f"No terminal sin definición: {simbolo}"
                    )

            # A → palabra ya tiene la forma correcta.
            if len(simbolos) == 1:
                if simbolos[0] in gramatica:
                    raise ValueError(
                        "Primero debes eliminar las producciones unarias."
                    )

                agregar(variable, simbolos)
                informar(
                    "    Se conserva: produce un único terminal."
                )
                continue

            # Sustituir terminales dentro de reglas compuestas.
            normalizados = []

            for simbolo in simbolos:
                if simbolo in gramatica:
                    normalizados.append(simbolo)
                    continue

                if simbolo not in auxiliares_terminales:
                    auxiliar = nueva_variable()
                    auxiliares_terminales[simbolo] = auxiliar
                    agregar(auxiliar, (simbolo,))

                    informar(
                        f"    Crear auxiliar: {auxiliar} → {simbolo}"
                    )
                else:
                    auxiliar = auxiliares_terminales[simbolo]

                    informar(
                        f"    Reutilizar: {auxiliar} → {simbolo}"
                    )

                normalizados.append(auxiliar)

            if tuple(normalizados) != simbolos:
                informar(
                    f"    Sustituir terminales: "
                    f"{variable} → {representar(normalizados)}"
                )

            # A → B C ya cumple Chomsky.
            if len(normalizados) == 2:
                agregar(variable, tuple(normalizados))
                informar(
                    "    La regla queda con dos no terminales."
                )
                continue

            # Dividir producciones con más de dos símbolos.
            informar(
                "    Dividir la producción en reglas binarias:"
            )

            actual = variable

            for indice in range(len(normalizados) - 2):
                auxiliar = nueva_variable()
                regla = (normalizados[indice], auxiliar)

                agregar(actual, regla)
                informar(
                    f"      {actual} → {representar(regla)}"
                )

                actual = auxiliar

            ultima_regla = tuple(normalizados[-2:])
            agregar(actual, ultima_regla)

            informar(
                f"      {actual} → {representar(ultima_regla)}"
            )

    informar(
        "\nPaso 3: copiar las alternativas al nuevo inicial."
    )

    alternativas_iniciales = resultado.get(inicial, [])

    if not alternativas_iniciales:
        informar(
            "  El inicial original no tiene alternativas "
            "no vacías que copiar."
        )

    for produccion in alternativas_iniciales:
        agregar(nuevo_inicial, produccion)
        informar(
            f"  {nuevo_inicial} → {representar(produccion)}"
        )

    informar("\nPaso 4: comprobar la cadena vacía.")

    if acepta_vacia:
        agregar(nuevo_inicial, ())
        informar(
            f"  Se conserva la cadena vacía: "
            f"{nuevo_inicial} → ε"
        )
    else:
        informar(
            "  La gramática original no genera la cadena vacía."
        )

    informar("\n========== FIN DE CHOMSKY ==========")

    return resultado, nuevo_inicial
"""Eliminación de producciones unarias, inútiles e inalcanzables."""

from remover_epsilon import simbolos_produccion


def remover_unarias(gram):
    """Sustituye A → B por las producciones no unarias alcanzables desde B.

    Calcula el cierre de cada variable para resolver cadenas y ciclos.
    Una producción de un único terminal, como A → a, se conserva.
    """
    resultado = {letra: [] for letra in gram}
    for letra in gram:
        pendientes = [letra]
        visitados = set()
        while pendientes:
            actual = pendientes.pop()
            if actual in visitados:
                continue
            visitados.add(actual)
            for produccion in gram.get(actual, []):
                simbolos = simbolos_produccion(produccion, gram)
                if len(simbolos) == 1 and (
                    simbolos[0] in gram or simbolos[0][0].isupper()
                ):
                    pendientes.append(simbolos[0])
                elif produccion not in resultado[letra]:
                    resultado[letra].append(produccion)
    return resultado


def remover_inutiles(gram):
    """Elimina variables que no generan palabras terminales y sus referencias."""
    generadores = set()
    cambio = True
    while cambio:
        cambio = False
        for letra, producciones in gram.items():
            if letra in generadores:
                continue
            for produccion in producciones:
                simbolos = simbolos_produccion(produccion, gram)
                if all(s in generadores or (s not in gram and not s[0].isupper())
                       for s in simbolos):
                    generadores.add(letra)
                    cambio = True
                    break
    return {
        letra: [p for p in producciones if all(
            s in generadores or (s not in gram and not s[0].isupper())
            for s in simbolos_produccion(p, gram)
        )]
        for letra, producciones in gram.items() if letra in generadores
    }


def remover_inalcanzables(gram, inicial=None):
    """Conserva únicamente variables alcanzables desde el símbolo inicial."""
    if inicial is None:
        inicial = next(iter(gram), None)
    if inicial not in gram:
        return {}
    alcanzables = set()
    pendientes = [inicial]
    while pendientes:
        letra = pendientes.pop()
        if letra in alcanzables:
            continue
        alcanzables.add(letra)
        for produccion in gram[letra]:
            pendientes.extend(s for s in simbolos_produccion(produccion, gram)
                              if s in gram and s not in alcanzables)
    return {letra: list(producciones) for letra, producciones in gram.items()
            if letra in alcanzables}

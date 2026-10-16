from itertools import combinations
import re

patron = re.compile(r"^[A-Z][A-Za-z0-9 ]* → (?:[A-Za-z0-9]+(?: +[A-Za-z0-9]+)*|ϵ)(?: ?\| ?(?:[A-Za-z0-9]+(?: +[A-Za-z0-9]+)*|ϵ))*$")
f1 = open("gramatica.txt", "r")
f = f1.readlines()
f1.close()
gramatica = {}
epsilons = []
errores = False

for numero, line in enumerate(f, 1):
    if line.strip() == "":
        continue
    if not patron.match(line.rstrip("\n")):
        print(f"error en la línea {numero}: {line.rstrip()!r}")
        errores = True
        continue
    izquierda, derecha = line.split("→", 1)
    izquierda = izquierda.replace(" ", "")
    gramatica.setdefault(izquierda, []).extend(p.strip() for p in derecha.strip().split("|"))
    if "ϵ" in derecha and izquierda not in epsilons:
        epsilons.append(izquierda)

if errores:
    print("gramatica invalida")
    raise SystemExit(1)


def remover_epsilons(gram, lista):
    gramatica_epsilon = gram
    cambio = True
    while cambio:
        cambio = False
        for letra, prod in gramatica_epsilon.items():
            if letra in lista:
                continue

            for produccion in prod:
                es_epsilon = produccion in ("", "ϵ", "ε")
                produce_epsilon = (
                    produccion not in ("", "ϵ", "ε")
                    and all(simbolo in lista for simbolo in produccion)
                )
                if es_epsilon or produce_epsilon:
                    lista.append(letra)
                    cambio = True
                    break
        for letra, prod in gramatica_epsilon.items():
            nuevas = []
            for epsi in list(prod):
                if epsi in ("", "ϵ", "ε"):
                    continue

                posiciones = [
                    i for i, simbolo in enumerate(epsi)
                    if simbolo in lista
                ]
                N = len(posiciones)
                if N == 0:
                    continue
                res = [
                    "".join(
                        simbolo
                        for posicion, simbolo in enumerate(epsi)
                        if posicion not in comb
                    )
                    for i in range(1, N + 1)
                    for comb in combinations(posiciones, i)
                ]
                nuevas.extend(res)

            for produccion in nuevas:
                if produccion != "" and produccion not in prod:
                    prod.append(produccion)
                    cambio = True
    for letra, prod in gramatica_epsilon.items():
        while "ϵ" in prod:
            prod.remove("ϵ")
        while "ε" in prod:
            prod.remove("ε")
        while "" in prod:
            prod.remove("")

    return gramatica_epsilon



C = remover_epsilons(gramatica, epsilons)
print("Gramática sin producciones ϵ:", C)

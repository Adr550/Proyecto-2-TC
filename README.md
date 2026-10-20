# Proyecto 2 — Analizador de frases con CYK

Determina si una frase pertenece al lenguaje de una gramática.
Muestra SÍ o NO, el tiempo de CYK y, si se acepta, una explicación
de las reglas utilizadas y un árbol de análisis.

## Ejecución

Requiere Python 3.8 o superior, sin dependencias externas.

```powershell
python main.py
```

Para ingresar la frase directamente y mostrar la tabla:

```powershell
python main.py --frase "we drink water" --tabla
```

## Diseño de la aplicación

El procesamiento sigue este flujo:

```text
Frase → Normalización
Gramática → Simplificación → Chomsky
                     ↓
                    CYK
                     ↓
        Resultado, tiempo y árbol
```

La simplificación elimina épsilon, reglas unarias, variables
no generadoras e inalcanzables. La conversión a Chomsky prepara
las reglas para CYK.

CYK utiliza programación dinámica: guarda qué variables generan
cada subfrase y combina esos resultados hasta analizar la frase
completa. También guarda referencias para reconstruir un árbol.

Los módulos separan la lectura y simplificación, la conversión
a Chomsky, el análisis CYK y la presentación del resultado.

## Discusión

Los principales obstáculos fueron reconocer palabras completas
como terminales, conservar la separación entre variables como
NP y VP, y reconstruir el árbol desde la tabla CYK.

Se utilizaron tuplas para representar las producciones y
referencias de derivación para construir el árbol.

El programa comprueba la estructura según la gramática,
pero no el significado ni la concordancia. Por ejemplo,
`he run` se acepta con la gramática actual.

Se recomienda ampliar la gramática, incorporar concordancia
y agregar pruebas automatizadas. La explicación mostrada
corresponde a las reglas usadas para reconocer la frase,
no a todas las transformaciones de Chomsky.

## Ejemplos y pruebas realizadas

Resultados verificados con la gramática actual:

| Frase | Resultado |
|---|---|
| i eat pizza | SÍ |
| we drink water | SÍ |
| they order a coffee | SÍ |
| you eat pasta with cheese | SÍ |
| we eat pizza in the restaurant | SÍ |
| i pizza eat | NO |
| we drink the | NO |
| you order cake | NO |
| eat pizza | NO |
| Cadena vacía | NO |

Los rechazos corresponden a estructuras incompletas, orden
incorrecto o palabras fuera del vocabulario. Los resultados
pueden cambiar si se modifica `gramatica.txt`.
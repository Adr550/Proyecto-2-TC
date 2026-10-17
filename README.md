# Proyecto-2-TC

Ejecutar desde la carpeta del proyecto:

```sh
python3 main.py
```

También se puede indicar otro archivo:

```sh
python3 main.py otra_gramatica.txt
```

`main.py` muestra cada etapa: eliminación de épsilon, de producciones unarias,
de variables no generadoras y de variables inalcanzables. El símbolo inicial
es el primer lado izquierdo del archivo y se conserva como referencia durante
todo el proceso, incluso si resulta no generador.

- `remover_epsilon.py`: lectura, identificación de símbolos y eliminación de épsilon.
- `remover_unarias.py`: eliminación de unarias, inútiles e inalcanzables.

Las funciones reciben un diccionario `{no_terminal: [producciones]}` y devuelven
un diccionario nuevo. `remover_epsilons` también completa la lista de anulables.
Una producción es unaria si contiene un único **no terminal**; `A → a` permanece.
Las cadenas y ciclos de unarias se resuelven calculando las variables alcanzables.
Primero se eliminan las variables que no generan palabras terminales, y luego
las que no pueden alcanzarse desde el símbolo inicial.

Se usa la flecha `→` y `|` para separar alternativas; se aceptan `ϵ` y `ε`.
Como en la entrada original, los espacios son decorativos: `N P` se normaliza a
`NP`. Los nombres de no terminales empiezan en mayúscula. Cuando un nombre es
prefijo de otro, se reconoce primero el más largo (`NP`, `VP`, `Det`).
Así, `S → N P V P` representa `S → NP VP`.

Se mantiene la convención del eliminador original: se elimina épsilon incluso
si lo genera el símbolo inicial. Por ello, la gramática resultante representa
el lenguaje original sin la palabra vacía; si solo generaba épsilon, queda vacía.

No se necesitan dependencias externas. Importar los módulos no lee archivos ni
imprime resultados. `main.py` encuentra su `gramatica.txt` desde cualquier carpeta.

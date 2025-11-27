# Cálculo de CHSH en el ejemplo E91

En este ejemplo E91 estimamos la violación de la desigualdad CHSH a partir de los resultados de medición de Alice y Bob. El código relevante está en `run_simulation.py`, función `_chsh_statistics(...)`.

## Qué hace `_chsh_statistics`

Entrada:

- `alice_bases`, `bob_bases`: bases elegidas en cada disparo (strings como `"A0_Z"` o `"B0_plus22.5deg"`).
- `alice_bits`, `bob_bits`: resultados de medición (0/1) en cada disparo.

Pasos:

1. **Agrupar por pareja de bases CHSH**: se crean “buckets” para cada par definido en `CHSH_PAIRS`:
   - $a_0=$ Z de Alice con $b_0=$ +22.5° de Bob
   - $a_0=$ Z con $b_1=$ –22.5°
   - $a_1=$ 45° con $b_0=$ +22.5°
   - $a_1=$ 45° con $b_1=$ –22.5°
   Solo los disparos en los que Alice y Bob eligieron una de estas combinaciones se contabilizan.
2. **Correlación puntual**: cada resultado 0/1 se mapea a ±1 (`_bit_to_pm1`), y se acumula el producto $A_k B_k$ en el bucket de esa pareja de bases. Ese producto es +1 si los bits coinciden y –1 si difieren.
3. **Valor de correlación $E(a_i,b_j)$**: para cada pareja se hace el promedio de los productos ±1:
   $$
   E(a_i,b_j) = \frac{1}{n}\sum_k A_k B_k
   $$
   donde $n$ es el número de disparos con esa combinación de bases. También se guarda `counts` con ese $n$.
4. **Valor CHSH $S$**: se combinan las correlaciones en el orden estándar:
   $$
   S = E(a_0,b_0) + E(a_0,b_1) + E(a_1,b_0) - E(a_1,b_1)
   $$
   En la teoría cuántica, con bases óptimas y estado ideal, $S \le 2\sqrt{2}\approx 2.828$.

Salida de la función:

- `expectations`: diccionario $E(a_i,b_j)$ por pareja de bases.
- `counts`: cuántos disparos se usaron en cada pareja.
- `s_value`: el valor $S$ de CHSH.

## Para qué sirve

Medir $S$ > 2 demuestra correlaciones no locales (violación de CHSH) y, en el protocolo E91, evidencia contra un atacante clásico. Al mismo tiempo, la estimación de $E(a_i,b_j)$ permite verificar la calidad del entrelazamiento que se usa para generar clave (las mediciones en bases de clave se filtran aparte en `_sift_key`).

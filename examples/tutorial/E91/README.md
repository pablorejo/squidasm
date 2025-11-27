# Fuente central E91: paso de medida Bell y CNOT

Este ejemplo usa una fuente (`SourceProgram`) que recibe un par EPR con Alice y otro con Bob, y mediante una **medida Bell** traslada el entrelazamiento para que lo compartan Alice y Bob. El bloque relevante en `application.py` es:

```python
# Medida Bell para trasladar el entrelazamiento a (Alice, Bob).
qubit_a.cnot(qubit_b)  # control = qubit_a (Alice), target = qubit_b (Bob)
qubit_a.H()
m2 = qubit_a.measure()
m1 = qubit_b.measure()
yield from connection.flush()
```

## Qué hace cada paso
- `qubit_a` está entrelazado con Alice; `qubit_b` está entrelazado con Bob.
- `CNOT`: usa `qubit_a` como control y `qubit_b` como target.
- `H` sobre `qubit_a`.
- Se miden ambos qubits del Source, produciendo dos bits clásicos `m1` y `m2`.
- Esos bits se envían a Bob, que aplica correcciones: `X` si `m1 = 1` y `Z` si `m2 = 1`. Así se “arregla” la fase/bit-flip y el par (Alice, Bob) queda en el estado esperado (Φ⁺ idealmente).

## Matemática completa del swapping (más detallado)

Notación: $S_A, S_B$ son los qubits de la fuente; $A$ es el de Alice y $B$ el de Bob. La Bell de partida es $|\Phi^{+}\rangle = \tfrac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$.

1) **Estado inicial (producto de dos Bell):**
$$
|\Phi^{+}\rangle_{S_A A}\otimes|\Phi^{+}\rangle_{S_B B}
= \tfrac{1}{2}\Big(
|0_{S_A}0_A0_{S_B}0_B\rangle +
|0_{S_A}0_A1_{S_B}1_B\rangle +
|1_{S_A}1_A0_{S_B}0_B\rangle +
|1_{S_A}1_A1_{S_B}1_B\rangle
\Big)
$$

2) **CNOT con control $S_A$, target $S_B$** (solo cambia cuando $S_A=1$):
$$
\tfrac{1}{2}\Big(
|0\,0\,0\,0\rangle +
|0\,0\,1\,1\rangle +
|1\,1\,1\,0\rangle +
|1\,1\,0\,1\rangle
\Big)
$$

3) **Hadamard en $S_A$** (usando $H|0\rangle=\tfrac{|0\rangle+|1\rangle}{\sqrt{2}}$, $H|1\rangle=\tfrac{|0\rangle-|1\rangle}{\sqrt{2}}$). Factorizamos el $\tfrac{1}{\sqrt{2}}$:
$$
\tfrac{1}{2\sqrt{2}}\Big[
|0\rangle\big(|0\,0\,0\rangle+|0\,1\,1\rangle+|1\,1\,0\rangle+|1\,0\,1\rangle\big)
+
|1\rangle\big(|0\,0\,0\rangle+|0\,1\,1\rangle-|1\,1\,0\rangle-|1\,0\,1\rangle\big)
\Big]_{S_A S_B A B}
$$

4) **Reescritura por resultados de medida** $(m_2,m_1)=(S_A,S_B)$: el estado queda como suma de kets clásicos de la fuente y un estado Bell en $AB$:
$$
\tfrac{1}{2}\Big(
|00\rangle_{S_AS_B}\,|\Phi^{+}\rangle_{AB} +
|01\rangle_{S_AS_B}\,|\Psi^{+}\rangle_{AB} +
|10\rangle_{S_AS_B}\,|\Phi^{-}\rangle_{AB} +
|11\rangle_{S_AS_B}\,|\Psi^{-}\rangle_{AB}
\Big)
$$
donde
$$
|\Psi^{\pm}\rangle=\tfrac{1}{\sqrt{2}}(|01\rangle\pm|10\rangle),\qquad
|\Phi^{-}\rangle=\tfrac{1}{\sqrt{2}}(|00\rangle-|11\rangle).
$$

5) **Medición y correcciones**: al medir $S_A,S_B$ obtenemos $(m_2,m_1)$. El par $AB$ colapsa a la Bell indicada. Con las correcciones clásicas:
$$
\text{si } m_1=1 \Rightarrow X_B,\qquad
\text{si } m_2=1 \Rightarrow Z_B,
$$
Bob siempre llega a $|\Phi^{+}\rangle$. Así, Alice y Bob comparten el par EPR y los qubits de la fuente pueden desecharse.

## CNOT en notación de kets

Para control = primer qubit y target = segundo qubit:

$$
|00\rangle \rightarrow |00\rangle \\
|01\rangle \rightarrow |01\rangle \\
|10\rangle \rightarrow |11\rangle \\
|11\rangle \rightarrow |10\rangle
$$

Matricialmente (orden de base |00>, |01>, |10>, |11>):

$$
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0
\end{pmatrix}
$$

Aplicada a un estado general

$$
|\psi\rangle = \alpha_{00}|00\rangle + \alpha_{01}|01\rangle + \alpha_{10}|10\rangle + \alpha_{11}|11\rangle
$$

el resultado es

$$
\alpha_{00}|00\rangle + \alpha_{01}|01\rangle + \alpha_{10}|11\rangle + \alpha_{11}|10\rangle
$$

es decir, intercambia las amplitudes de $|10\rangle$ y $|11\rangle$; equivalente a aplicar $X$ en el target cuando el control es $|1\rangle$.

## Por qué esto hace swapping

La medida Bell (CNOT + H + medidas) proyecta los qubits de la fuente en uno de los cuatro estados de Bell. Según el resultado (m1, m2), Bob aplica correcciones de Pauli. Tras las correcciones, el entrelazamiento queda compartido entre Alice y Bob; la fuente puede descartar sus qubits. Este es el mismo principio que se usa en teletransporte y en entanglement swapping.

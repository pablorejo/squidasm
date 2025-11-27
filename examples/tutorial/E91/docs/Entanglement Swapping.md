# Entanglement Swapping con dos pares EPR

## 1. Estados iniciales

Tenemos dos pares EPR:

* Par 1: ($S_A$, A)
* Par 2: ($S_B$, B)

Cada par está en el estado de Bell:

$$
\lvert \Phi^+ \rangle = \frac{1}{\sqrt{2}}(\lvert 00\rangle + \lvert 11\rangle)
$$

Por tanto, el estado conjunto inicial es:

$$
\lvert \Psi_0 \rangle = \lvert \Phi^+ \rangle_{S_A A} \otimes \lvert \Phi^+ \rangle_{S_B B}.
$$

Expresado como kets en el orden (($S_A$, $A$, $S_B$, $B$)):

$$
\lvert \Psi_0 \rangle = \frac{1}{2}(\lvert 0000\rangle + \lvert 0011\rangle + \lvert 1100\rangle + \lvert 1111\rangle).
$$

---

## 2. Aplicar CNOT(($S_A \to S_B$))

La puerta CNOT actúa como:

$$
\text{CNOT}: \lvert c, t \rangle \mapsto \lvert c, t \oplus c \rangle.
$$

Aplicando sobre los estados:

* $\lvert 0000\rangle \to \lvert 0000\rangle$
* $\lvert 0011\rangle \to \lvert 0011\rangle$
* $\lvert 1100\rangle \to \lvert 1110\rangle$
* $\lvert 1111\rangle \to \lvert 1101\rangle$

Queda:

$$
\lvert \Psi_1 \rangle = \frac{1}{2}(\lvert 0000\rangle + \lvert 0011\rangle + \lvert 1110\rangle + \lvert 1101\rangle).
$$

---

## 3. Aplicar Hadamard a ($S_A$)

Recordamos:

$$
H\lvert 0\rangle = \frac{\lvert 0\rangle + \lvert 1\rangle}{\sqrt{2}}, \qquad
H\lvert 1\rangle = \frac{\lvert 0\rangle - \lvert 1\rangle}{\sqrt{2}}.
$$

Tras agrupar y aplicar (H), se obtiene:

$$
\lvert \Psi_2 \rangle = \frac{\sqrt{2}}{4}(\lvert 0000\rangle + \lvert 0011\rangle + \lvert 0101\rangle + \lvert 0110\rangle + \lvert 1000\rangle + \lvert 1011\rangle - \lvert 1101\rangle - \lvert 1110\rangle).
$$

---

## 4. Medida de ($S_A$) y ($S_B$)

Agrupamos los términos según los posibles resultados de medida:

| (($S_A$, $S_B$)) | Estado de (AB) obtenido                                       |
| ------------ | ------------------------------------------------------------- |
| (0,0)        | $\lvert 00\rangle + \lvert 11\rangle = \lvert \Phi^+ \rangle$ |
| (0,1)        | $\lvert 01\rangle + \lvert 10\rangle = \lvert \Psi^+ \rangle$ |
| (1,0)        | $\lvert 00\rangle - \lvert 11\rangle = \lvert \Phi^- \rangle$ |
| (1,1)        | $\lvert 01\rangle - \lvert 10\rangle = \lvert \Psi^- \rangle$ |

Cada resultado ocurre con probabilidad (1/4). En todos ellos, (A) y (B) quedan entrelazados.

---

## 5. Correcciones de Pauli en Bob

Las puertas necesarias para volver siempre al estado $\lvert \Phi^+ \rangle_{AB}$ son:

* Si ($S_A$ = 1), aplicar (Z) en (B).
* Si ($S_B$ = 1), aplicar (X) en (B).


---

## 6. Resultado final

Tras la CNOT, el Hadamard, la medida de (S_A, S_B) y el envío de los bits clásicos, Bob puede aplicar correcciones de Pauli y **obtener siempre un estado EPR perfecto entre (A) y (B)**:

$$
\lvert \Phi^+ \rangle_{AB} = \frac{1}{\sqrt{2}}(\lvert 00\rangle + \lvert 11\rangle).
$$

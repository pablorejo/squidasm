# Filtrado de bits de clave: función `_sift_key`

En el protocolo E91 solo ciertas combinaciones de bases se usan para generar la clave. La función `_sift_key` en `run_simulation.py` implementa ese filtrado y estima el QBER sobre los bits retenidos.

## Código relevante (resumen)

```python
def _sift_key(alice_bases, bob_bases, alice_bits, bob_bits):
    key_bits = []
    used_pairs = 0
    mismatches = 0

    for a_basis, b_basis, a_bit, b_bit in zip(alice_bases, bob_bases, alice_bits, bob_bits):
        if (a_basis, b_basis) != KEY_BASIS:
            continue  # solo guardamos los disparos en la base de clave, p.ej. X/X
        used_pairs += 1
        key_bits.append(a_bit)  # usamos el bit de Alice como bit crudo de clave
        if a_bit != b_bit:
            mismatches += 1

    error_rate = mismatches / used_pairs if used_pairs else 0.0
    return key_bits, used_pairs, error_rate
```

## Qué hace paso a paso

1. **Recorre todos los disparos** en paralelo: bases y resultados de Alice y Bob.
2. **Filtra por la base de clave**: solo se conservan los disparos cuya pareja de bases coincide con `KEY_BASIS` (en el ejemplo, `("A2_X", "B2_X")`, es decir, ambos midieron en X).
3. **Acumula bits de clave cruda**: añade el bit de Alice a `key_bits`.
4. **Cuenta discrepancias**: si el bit de Alice y el de Bob difieren, se incrementa `mismatches`.
5. **Calcula QBER**: `error_rate = mismatches / used_pairs` (o 0 si no hubo pares). Este es el Quantum Bit Error Rate en los bits de clave retenidos.

## Para qué sirve

- **Sifting**: descarta las mediciones que no se hicieron en la base de clave. En E91 las demás bases se usan para el test de CHSH, no para clave.
- **Estimación de errores**: el QBER sobre la base de clave indica la calidad del canal/entrelazamiento. Un QBER alto obliga a descartar la sesión o aplicar corrección de errores y privacidad.
- **Salida**: devuelve la lista de bits crudos de Alice (`key_bits`), cuántos pares se usaron (`used_pairs`) y el QBER (`error_rate`), que luego se muestran en la simulación.

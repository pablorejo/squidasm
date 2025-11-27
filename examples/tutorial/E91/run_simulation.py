from typing import Dict, List, Sequence, Tuple

from application import (
    ALICE_NAME,
    BOB_NAME,
    CHSH_PAIRS,
    KEY_BASIS,
    AliceProgram,
    BobProgram,
    SourceProgram,
)
from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run


def _bit_to_pm1(bit: int) -> int:
    return 1 if bit == 0 else -1


def _sift_key(
    alice_bases: Sequence[str],
    bob_bases: Sequence[str],
    alice_bits: Sequence[int],
    bob_bits: Sequence[int],
) -> Tuple[List[int], int, float]:
    key_bits: List[int] = []
    used_pairs = 0
    mismatches = 0

    for a_basis, b_basis, a_bit, b_bit in zip(alice_bases, bob_bases, alice_bits, bob_bits):
        if (a_basis, b_basis) != KEY_BASIS:
            continue
        used_pairs += 1
        key_bits.append(a_bit)
        if a_bit != b_bit:
            mismatches += 1

    error_rate = mismatches / used_pairs if used_pairs else 0.0
    return key_bits, used_pairs, error_rate


def _chsh_statistics(
    alice_bases: Sequence[str],
    bob_bases: Sequence[str],
    alice_bits: Sequence[int],
    bob_bits: Sequence[int],
) -> Tuple[Dict[Tuple[str, str], float], Dict[Tuple[str, str], int], float]:
    buckets: Dict[Tuple[str, str], List[int]] = {pair: [] for pair in CHSH_PAIRS}

    for a_basis, b_basis, a_bit, b_bit in zip(alice_bases, bob_bases, alice_bits, bob_bits):
        pair = (a_basis, b_basis)
        if pair not in buckets:
            continue
        buckets[pair].append(_bit_to_pm1(a_bit) * _bit_to_pm1(b_bit))

    expectations: Dict[Tuple[str, str], float] = {}
    counts: Dict[Tuple[str, str], int] = {}
    for pair, products in buckets.items():
        counts[pair] = len(products)
        expectations[pair] = sum(products) / len(products) if products else 0.0

    s_value = (
        expectations[CHSH_PAIRS[0]]
        + expectations[CHSH_PAIRS[1]]
        + expectations[CHSH_PAIRS[2]]
        - expectations[CHSH_PAIRS[3]]
    )

    return expectations, counts, s_value

def get_key(size):
    key = []

    while len(key) < size:
        key.extend(iteration())

    return key[:size-1]


def iteration() -> None:
    cfg = StackNetworkConfig.from_file("config.yaml")

    num_pairs = 256
    alice_program = AliceProgram(num_pairs=num_pairs, seed=42)
    bob_program = BobProgram(num_pairs=num_pairs, seed=1337)
    source_program = SourceProgram(num_pairs=num_pairs)

    results = run(
        config=cfg,
        programs={
            "Source": source_program,
            ALICE_NAME: alice_program,
            BOB_NAME: bob_program,
        },
        num_times=1,
    )

    node_names = [stack.name for stack in cfg.stacks]
    results_by_node = {name: results[i] for i, name in enumerate(node_names)}
    alice = results_by_node[ALICE_NAME][0]
    bob = results_by_node[BOB_NAME][0]

    alice_bases = alice["bases"]
    bob_bases = bob["bases"]
    alice_bits = alice["results"]
    bob_bits = bob["results"]

    key_bits, sifted_pairs, qber = _sift_key(alice_bases, bob_bases, alice_bits, bob_bits)
    expectations, counts, s_value = _chsh_statistics(alice_bases, bob_bases, alice_bits, bob_bits)

    print(f"Total entangled pairs: {len(alice_bits)}")
    print(f"Raw key bits kept (X/X basis): {len(key_bits)} from {sifted_pairs} pairs")
    print(f"QBER on kept bits: {qber * 100:.2f}%")
    print("CHSH expectation values per basis pair:")
    for pair in CHSH_PAIRS:
        exp_val = expectations[pair]
        print(f"  {pair[0]} vs {pair[1]} -> E={exp_val:.3f} (n={counts[pair]})")
    print(f"CHSH S value: {s_value:.3f} (ideal maximum is 2.828)")
    print(f"First 16 raw key bits: {key_bits[:16]}")

    return key_bits


def main() -> None:

    KEY = 256

    if KEY % 8 != 0:
        ValueError("La clave tiene que ser multiplo de 8")
    key = get_key(256)

    # Suponiendo que 'key' es una lista de bits (0/1)
    # Transformar los bits a bytes
    key_int = [
        int(''.join(str(b) for b in key[i:i+8]), 2)
        for i in range(0, len(key), 8)
    ]

    key_bytes = bytes(key_int)

    print(f"Clave obtenida: {key_bytes}")

if __name__ == "__main__":
    main()

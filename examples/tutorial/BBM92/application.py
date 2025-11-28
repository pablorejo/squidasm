from dataclasses import dataclass
import random
from typing import Dict, List, Optional, Sequence, Tuple

from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


ALICE_NAME = "Alice"
BOB_NAME = "Bob"
SOURCE_NAME = "Source"


@dataclass(frozen=True)
class Basis:
    name: str
    angle_n: int  # numerator in rotation expression n * pi / 2**d
    angle_d: int  # exponent d in rotation expression n * pi / 2**d

    def rotation(self) -> Tuple[int, int]:
        return self.angle_n, self.angle_d


def _apply_measurement_basis(qubit, basis: Basis) -> None:
    """Rotate the qubit so a Z measurement corresponds to the desired basis."""
    angle_n, angle_d = basis.rotation()
    if angle_n != 0:
        # NetQASM rotations require non-negative numerators; map negative angles modulo 2π.
        modulus = 2 ** (angle_d + 1)
        angle = (-angle_n) % modulus
        qubit.rot_Y(angle, angle_d)


# BBM92 usa dos bases complementarias: Z y X.
BASES: Tuple[Basis, ...] = (
    Basis("Z", 0, 1),  # Medición computacional
    Basis("X", 1, 1),  # Rotación π/2 hacia X antes de medir
)


class SourceProgram(Program):
    """Fuente central que distribuye entanglement a Alice y Bob."""

    PEER_ALICE = ALICE_NAME
    PEER_BOB = BOB_NAME

    def __init__(self, num_pairs: int = 256):
        self._num_pairs = num_pairs

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="bbm92_source",
            csockets=[self.PEER_ALICE, self.PEER_BOB],
            epr_sockets=[self.PEER_ALICE, self.PEER_BOB],
            max_qubits=2,
        )

    def run(self, context: ProgramContext) -> Dict[str, Sequence[int]]:
        csocket_alice: Socket = context.csockets[self.PEER_ALICE]
        csocket_bob: Socket = context.csockets[self.PEER_BOB]
        epr_socket_alice: EPRSocket = context.epr_sockets[self.PEER_ALICE]
        epr_socket_bob: EPRSocket = context.epr_sockets[self.PEER_BOB]
        connection: BaseNetQASMConnection = context.connection

        for _ in range(self._num_pairs):
            # Crear dos pares: (Source, Alice) y (Source, Bob).
            qubit_a = epr_socket_alice.create_keep()[0]
            qubit_b = epr_socket_bob.create_keep()[0]

            # Medida Bell para trasladar el entrelazamiento a (Alice, Bob).
            qubit_a.cnot(qubit_b)
            qubit_a.H()
            m2 = qubit_a.measure()
            m1 = qubit_b.measure()
            yield from connection.flush()

            # Avisar a Alice que el par está listo y mandar correcciones a Bob.
            csocket_alice.send("ready")
            csocket_bob.send(f"{int(m1)},{int(m2)}")

        return {}


class AliceProgram(Program):
    PEER_NAME = SOURCE_NAME

    def __init__(self, num_pairs: int = 256, seed: Optional[int] = None):
        self._num_pairs = num_pairs
        self._rng = random.Random(seed)

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="bbm92_alice",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=1,
        )

    def run(self, context: ProgramContext) -> Dict[str, Sequence[int]]:
        csocket: Socket = context.csockets[self.PEER_NAME]
        epr_socket: EPRSocket = context.epr_sockets[self.PEER_NAME]
        connection: BaseNetQASMConnection = context.connection

        bases: List[str] = []
        results: List[int] = []

        for _ in range(self._num_pairs):
            qubit = epr_socket.recv_keep()[0]
            yield from connection.flush()
            _ = yield from csocket.recv()

            basis = self._rng.choice(BASES)

            _apply_measurement_basis(qubit, basis)
            measurement = qubit.measure()

            bases.append(basis.name)
            results.append(measurement)
            yield from connection.flush()

        measurements = [int(r) for r in results]
        return {"bases": bases, "results": measurements}


class BobProgram(Program):
    PEER_NAME = SOURCE_NAME

    def __init__(self, num_pairs: int = 256, seed: Optional[int] = None):
        self._num_pairs = num_pairs
        self._rng = random.Random(seed)

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="bbm92_bob",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=1,
        )

    def run(self, context: ProgramContext) -> Dict[str, Sequence[int]]:
        csocket: Socket = context.csockets[self.PEER_NAME]
        epr_socket: EPRSocket = context.epr_sockets[self.PEER_NAME]
        connection: BaseNetQASMConnection = context.connection

        bases: List[str] = []
        results: List[int] = []

        for _ in range(self._num_pairs):
            qubit = epr_socket.recv_keep()[0]
            yield from connection.flush()
            corr_msg = yield from csocket.recv()
            m1_str, m2_str = corr_msg.split(",")
            m1, m2 = int(m1_str), int(m2_str)

            if m1:
                qubit.X()
            if m2:
                qubit.Z()

            basis = self._rng.choice(BASES)
            _apply_measurement_basis(qubit, basis)
            measurement = qubit.measure()

            bases.append(basis.name)
            results.append(measurement)
            yield from connection.flush()

        measurements = [int(r) for r in results]
        return {"bases": bases, "results": measurements}

import enum
from typing import List, Literal, Protocol, runtime_checkable

Bit = int
Bits = List[int]

Sample = float  # one sample of a signal (digital or analog)
Signal = List[Sample]  # sequence of samples

# Semantic aliases (all are just Signal/ Bits in code, but names document intent)
DigitalData = Bits  # abstract bit sequence (message, PCM output, etc.)
AnalogData = Signal  # e.g., "raw" analog waveform (simulated as samples)

DigitalSignal = Signal  # line-coded signal on a baseband digital link
AnalogSignal = Signal  # modulated bandpass signal on an analog link


class TransmissionMode(enum.Enum):
    D2D = 0
    D2A = 1
    A2D = 2
    A2A = 3


@runtime_checkable
class Encoder(Protocol):
    def encode(self, data: DigitalData | AnalogData) -> DigitalSignal:
        ...


@runtime_checkable
class Decoder(Protocol):
    def decode(self, signal: DigitalSignal | AnalogSignal) -> DigitalData:
        ...

@runtime_checkable
class Modulator(Protocol):
    def modulate(self, signal: DigitalSignal | AnalogSignal) -> AnalogSignal:
        ...

@runtime_checkable
class Demodulator(Protocol):
    def demodulate(self, signal: DigitalSignal | AnalogSignal) -> AnalogSignal:
        ...

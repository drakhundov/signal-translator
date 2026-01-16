import enum
from typing import List, Protocol, runtime_checkable

Bit = int
Bits = List[int]

Sample = float  # one sample of a signal (digital or analog)
Signal = List[Sample]  # sequence of samples

DigitalData = Bits
AnalogData = Signal

DigitalSignal = Signal
AnalogSignal = Signal


class TransmissionMode(enum.Enum):
    D2D = 0
    D2A = 1
    A2D = 2
    A2A = 3

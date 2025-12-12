from custom_types import TransmissionMode

from d2d_encoding import NRZ, ManchesterCode, AMI
from d2a_modulation import ASK, FSK, PSK
from a2d_modulation import PCM, DeltaModulation
from a2a_modulation import AM, PM, FM

schemes = {
    TransmissionMode.D2D: [NRZ, ManchesterCode, AMI],
    TransmissionMode.D2A: [ASK, FSK, PSK],
    TransmissionMode.A2D: [PCM, DeltaModulation],
    TransmissionMode.A2A: [AM, PM, FM],
}

from custom_types import TransmissionMode

from d2d_encoding import NRZ, ManchesterCode, AMI
from d2a_modulation import ASK, FSK, PSK
from a2d_encoding import PCM
# from a2a_modulation import

schemes = {
    TransmissionMode.D2D: [NRZ, ManchesterCode, AMI],
    TransmissionMode.D2A: [ASK, FSK, PSK],
    TransmissionMode.A2D: [PCM],
    TransmissionMode.A2A: [],
}

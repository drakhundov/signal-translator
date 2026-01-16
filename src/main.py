from matplotlib import pyplot as plt

import ASCIIEncoder
import cli
import registry
from custom_types import TransmissionMode, Bits, Signal, DigitalData, AnalogData

# ! main.py should not access encoders/modulators directly.

# Transmission mode selection (e.g. digital to digital).
mode_index = cli.user_select_from_list(
    msg="Select a transmission mode:",
    select=["Digital -> Digital",
            "Digital -> Analog",
            "Analog -> Digital",
            "Analog -> Analog"],
    req_type=int,
    end='\n'
)

TRANSMISSION_MODE = TransmissionMode(mode_index)

available_converters = registry.schemes.get(TRANSMISSION_MODE)
# Transmission algorithm selection (e.g. Manchester).
algo_idx = cli.user_select_from_list(
    msg="Select an encoding/modulation scheme:",
    select=[converter_cls.__name__ for converter_cls in available_converters],
    req_type=int,
    end='\n'
)

ConverterCLS = registry.schemes.get(TRANSMISSION_MODE)[algo_idx]

_input: DigitalData | AnalogData = None
if TRANSMISSION_MODE in (TransmissionMode.D2A, TransmissionMode.D2D):
    print(">>> Computer A <<<")
    option = cli.user_select_from_list(
        msg="Input source",
        select=["Text message", "Raw bit sequence"],
        req_type=int
    )
    if option == 0:
        msg_input = input("Enter message to transmit: ")
        encoded_usr_msg = ASCIIEncoder.encode_msg(msg_input)
        _input = encoded_usr_msg
    else:
        bit_string = input("Enter a bit sequence: ")
        bit_list: Bits = [int(raw_bit) for raw_bit in bit_string if raw_bit in ('0', '1')]
        _input = bit_list
else:  # A2D, A2A
    signal_string = input("Enter sampled analog signal values (space-separated): ")
    sample_list: Signal = [float(raw_sample) for raw_sample in signal_string.split(" ")]
    _input = sample_list

converted = ConverterCLS.forward(_input)

print()
if input("Show the transmitted signal? (y/n) ") == "y":
    plt.plot(converted)
    plt.title("Transmitted Signal")
    plt.axis("off")
    plt.show()

print(">>> Computer B <<<")
deconverted = ConverterCLS.reverse(converted)
cli.pretty_show_received(deconverted)

if TRANSMISSION_MODE in (TransmissionMode.D2D, TransmissionMode.D2A):
    decoded_received_msg = ASCIIEncoder.decode_msg(deconverted)
    print(f"ASCII: {decoded_received_msg}")

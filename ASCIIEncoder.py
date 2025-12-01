from typing import List

from custom_types import Bits


def unsigned_repr(decimal: int) -> Bits:
    if decimal < 0:
        raise ValueError("Error: n must be non-negative.")
    if decimal == 0:
        return [0]
    bits: Bits = []
    while decimal > 0:
        bits.append(decimal & 1)
        decimal >>= 1
    bits.reverse()
    return bits


def encode_msg(msg: str) -> Bits:
    bits: Bits = []
    for ch in msg:
        code_point = ord(ch)
        # ASCII only: 0..255
        if code_point > 0xFF:
            raise ValueError("Non-ASCII character not supported")
        char_bits = unsigned_repr(code_point)  # MSB-first, minimal length
        # Pad to 8 bits (add leading zeros)
        padding = [0] * (8 - len(char_bits))
        bits.extend(padding + char_bits)
    return bits


def decode_msg(bits: Bits) -> str:
    if not bits:
        return ""
    rem = len(bits) % 8
    chars: List[str] = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        value = 0
        for b in byte:
            value = (value << 1) | (1 if b else 0)
        chars.append(chr(value))
    return "".join(chars)

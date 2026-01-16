from typing import List, Type


def user_select_from_list(msg: str, select: List[str], req_type: Type, end: str = ''):
    print(msg)
    noptions = len(select)
    for i, item in enumerate(select):
        print(f"{i}: {item}")
    raw = None
    while True:
        raw = input("Select an option: ")
        if req_type == int and not raw.isdigit():
            print("Please enter a number")
            continue
        elif int(raw) > noptions:
            print("Please enter a valid option")
        else:
            break
    print(end, end='')
    return req_type(raw)


# python
import math
from typing import List, Iterable

# ANSI color constants
_CSI = "\033["
_RESET = _CSI + "0m"
_BOLD = _CSI + "1m"
_GREEN = _CSI + "92m"
_YELLOW = _CSI + "93m"
_RED = _CSI + "91m"

def _is_bits_list(x: Iterable) -> bool:
    return all(isinstance(v, int) and v in (0, 1) for v in x)

def _group_bits_to_bytes(bits: List[int]) -> List[int]:
    # group into 8-bit bytes, drop trailing incomplete byte
    nbytes = len(bits) // 8
    out = []
    for i in range(nbytes):
        byte = 0
        for b in bits[i*8:(i+1)*8]:
            byte = (byte << 1) | b
        out.append(byte)
    return out

def _print_boxed(title: str, lines: List[str], color: str = "") -> None:
    w = max(len(title), *(len(l) for l in lines))
    horiz = "─" * (w + 2)
    print(f"{color}{_BOLD}┌{horiz}┐{_RESET}")
    print(f"{color}│ {title.ljust(w)} │{_RESET}")
    print(f"{color}├{horiz}┤{_RESET}")
    for l in lines:
        print(f"{color}│ {l.ljust(w)} │{_RESET}")
    print(f"{color}└{horiz}┘{_RESET}")

def _make_printable_char(b: int) -> str:
    if 32 <= b <= 126:
        return chr(b)
    if b == 0x20:
        return "␠"
    return "·"

def pretty_show_received(deconverted):
    # bits (0/1)
    if isinstance(deconverted, list) and _is_bits_list(deconverted):
        bytes_list = _group_bits_to_bytes(deconverted)
        lines = []
        # show up to 16 bytes per line
        per_line = 8
        for i in range(0, len(bytes_list), per_line):
            chunk = bytes_list[i:i+per_line]
            bin_repr = " ".join(f"{b:08b}" for b in chunk)
            hex_repr = " ".join(f"{b:02X}" for b in chunk)
            ascii_repr = "".join(_make_printable_char(b) for b in chunk)
            lines.append(f"{bin_repr}    {hex_repr}    {ascii_repr}")
        if not lines:
            lines = ["(no full bytes - too few bits)"]
        _print_boxed(f"Received — {len(deconverted)} bits / {len(bytes_list)} bytes", lines, _CSI + "94m")
        return

    # integer bytes already (0-255)
    if isinstance(deconverted, list) and all(isinstance(v, int) for v in deconverted):
        chunk = deconverted[:64]
        hex_repr = " ".join(f"{b:02X}" for b in chunk)
        ascii_repr = "".join(_make_printable_char(b) for b in chunk)
        lines = [hex_repr, ascii_repr]
        _print_boxed(f"Received — {len(deconverted)} integers", lines, _CSI + "94m")
        return

    # analog samples / floats
    if isinstance(deconverted, list) and all(isinstance(v, (int, float)) for v in deconverted):
        short = " ".join(f"{v:.3f}" for v in deconverted[:32])
        lines = [short]
        if len(deconverted) > 32:
            lines.append(f"... (+{len(deconverted) - 32} more samples)")
        _print_boxed(f"Received — {len(deconverted)} samples", lines, _CSI + "95m")
        return

    # fallback: pretty print repr
    _print_boxed("Received", [repr(deconverted)], _CSI + "95m")

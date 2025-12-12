from ASCIIEncoder import encode_msg, decode_msg
import pytest

@pytest.mark.parametrize("s", ["", "A", "hello", "Å"])  # last case expects error
def test_roundtrip_or_error(s):
    if any(ord(ch) > 0xFF for ch in s):
        with pytest.raises(ValueError):
            encode_msg(s)
    else:
        bits = encode_msg(s)
        assert isinstance(bits, list)
        got = decode_msg(bits)
        assert got == s

def test_empty_bits_decodes_to_empty_string():
    assert decode_msg([]) == ""

def test_encode_produces_8bit_bytes():
    bits = encode_msg("A")
    assert len(bits) % 8 == 0
    # check ASCII 'A' == 65
    byte = bits[0:8]
    value = 0
    for b in byte:
        value = (value << 1) | (1 if b else 0)
    assert value == 65

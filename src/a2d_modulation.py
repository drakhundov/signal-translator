from custom_types import AnalogData, DigitalData, Bits


class PCM: # Pulse-code modulation (
    @staticmethod
    def forward(signal: AnalogData, bits_per_sample: int = 8) -> DigitalData:
        if bits_per_sample <= 0:
            raise ValueError("`bits_per_sample` must be positive")
        max_level = (1 << bits_per_sample) - 1
        bits: Bits = []
        for sample in signal:
            # Clamp to [-1.0, 1.0]
            x = max(-1.0, min(1.0, sample))
            # Normalize to [0, 1]
            norm = (x + 1.0) / 2.0
            # Quantize to integer level
            level = int(round(norm * max_level))
            if level < 0:
                level = 0
            elif level > max_level:
                level = max_level
            # Convert integer level to bits (MSB first)
            for shift in range(bits_per_sample - 1, -1, -1):
                bit = (level >> shift) & 1
                bits.append(bit)
        return bits

    @staticmethod
    def reverse(bits: Bits, bits_per_sample: int = 8) -> AnalogData:
        if bits_per_sample <= 0:
            raise ValueError("bits_per_sample must be positive")
        if len(bits) % bits_per_sample != 0:
            raise ValueError("Bitstream length is not a multiple of bits_per_sample")
        max_level = (1 << bits_per_sample) - 1
        signal: AnalogData = []
        for i in range(0, len(bits), bits_per_sample):
            chunk = bits[i: i + bits_per_sample]
            # Bits -> integer level
            level = 0
            for bit in chunk:
                level = (level << 1) | (1 if bit else 0)
            # Map back to [0,1]
            norm = level / max_level if max_level > 0 else 0.0
            # Map back to [-1, 1]
            sample = 2.0 * norm - 1.0
            signal.append(sample)
        return signal


class DM: # Delta Modulation
    @staticmethod
    def forward(signal: AnalogData, bits_per_sample: int = 8) -> Bits:
        if bits_per_sample <= 0:
            raise ValueError("bits_per_sample must be positive")
        step = 2.0 / (1 << bits_per_sample)  # full range [-1,1] has width 2.0
        bits: Bits = []
        y = 0.0
        for sample in signal:
            # Clamp input to [-1, 1]
            x = max(-1.0, min(1.0, sample))
            if x >= y:
                bits.append(1)
                y += step
            else:
                bits.append(0)
                y -= step
            if y > 1.0:
                y = 1.0
            elif y < -1.0:
                y = -1.0
        return bits

    @staticmethod
    def reverse(bits: Bits, bits_per_sample: int = 8) -> AnalogData:
        if bits_per_sample <= 0:
            raise ValueError("bits_per_sample must be positive")
        step = 2.0 / (1 << bits_per_sample)
        signal: AnalogData = []
        y = 0.0
        for bit in bits:
            if bit:
                y += step
            else:
                y -= step
            if y > 1.0:
                y = 1.0
            elif y < -1.0:
                y = -1.0
            signal.append(y)
        return signal

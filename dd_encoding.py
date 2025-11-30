from custom_types import Bits, DigitalSignal


class NRZ:
    def encode(bits: Bits) -> DigitalSignal:
        """
        - 1 -> +1.0
        - 0 -> -1.0
        """
        return [1.0 if b == 1 else -1.0 for b in bits]

    def decode(signal: DigitalSignal) -> Bits:
        """
        - > 0 -> 1
        - <= 0 -> 0
        """
        return [1 if s > 0.0 else 0 for s in signal]


class Manchester:
    def encode(bits: Bits) -> DigitalSignal:
        """
        - 0 -> low-to-high: [-1.0, +1.0]
        - 1 -> high-to-low: [+1.0, -1.0]
        """
        signal: DigitalSignal = []
        for b in bits:
            if b == 0:
                signal.extend([-1.0, +1.0])
            else:
                signal.extend([+1.0, -1.0])
        return signal

    def decode(signal: DigitalSignal) -> Bits:
        """
        Take them pair by pair:
        - first > second  -> interpret as 0 (high-to-low)
        - first < second  -> interpret as 1 (low-to-high)

        Length of signal must be even (2 samples per bit).
        """
        if len(signal) % 2 != 0:
            raise ValueError("Manchester signal length must be even (2 samples per bit).")

        bits: Bits = []
        for i in range(0, len(signal), 2):
            first = signal[i]
            second = signal[i + 1]
            if first > second:
                bits.append(0)
            else:
                bits.append(1)
        return bits


class AMI:
    def encode(bits: Bits) -> DigitalSignal:
        """
        - 0 -> 0.0 (no pulse)
        - 1 -> pulses that alternate: +1.0, -1.0, +1.0, -1.0, ...
        """
        signal: DigitalSignal = []
        last_pulse: float = -1.0  # so first '1' becomes +1.0
        for b in bits:
            if b == 0:
                signal.append(0.0)
            else:
                # alternate pulse polarity
                last_pulse = -last_pulse
                signal.append(last_pulse)
        return signal

    def decode(signal: DigitalSignal) -> Bits:
        """
        - 0.0 (or very close to 0) -> 0
        - non-zero (positive or negative pulse) -> 1
        * Ignore polarity when decoding.
        """
        bits: Bits = []
        for s in signal:
            if abs(s) < 1e-6:
                bits.append(0)
            else:
                bits.append(1)
        return bits

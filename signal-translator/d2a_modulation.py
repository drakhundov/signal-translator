import math
from typing import List

from custom_types import Bits, AnalogSignal, Sample


class ASK:  # Amplitude Shift Keying
    @staticmethod
    def modulate(bits: Bits,
                 carrier_freq: float = 1.0,
                 samples_per_bit: int = 50,
                 amp_low: float = 0.0,
                 amp_high: float = 1.0) -> AnalogSignal:
        """
        - 0 -> low amplitude
        - 1 -> high amplitude
        """
        signal: List[Sample] = []
        for b in bits:
            amp = amp_high if b == 1 else amp_low
            for n in range(samples_per_bit):
                t = n / samples_per_bit
                sample = amp * math.sin(2 * math.pi * carrier_freq * t)
                signal.append(sample)
        return signal

    @staticmethod
    def demodulate(signal: AnalogSignal,
                   carrier_freq: float = 1.0,
                   samples_per_bit: int = 50,
                   threshold: float = 0.5) -> Bits:
        """
        For each bit interval, compute average absolute amplitude.
        - above threshold → 1
        - else → 0
        """
        bits: Bits = []
        signal_lengths = len(signal)
        if signal_lengths % samples_per_bit != 0:
            raise ValueError("Signal length is not a multiple of `samples_per_bit`")
        for i in range(0, signal_lengths, samples_per_bit):
            chunk = signal[i: i + samples_per_bit]
            avg = sum(abs(s) for s in chunk) / samples_per_bit
            bits.append(1 if avg >= threshold else 0)
        return bits


class FSK:  # Frequency Shift Keying
    @staticmethod
    def modulate(bits: Bits,
                 f0: float = 1.0,
                 f1: float = 2.0,
                 samples_per_bit: int = 50) -> AnalogSignal:
        """
        - 0 -> carrier at f0
        - 1 -> carrier at f1
        """
        signal: List[Sample] = []
        for b in bits:
            freq = f1 if b == 1 else f0
            for n in range(samples_per_bit):
                t = n / samples_per_bit
                sample = math.sin(2 * math.pi * freq * t)
                signal.append(sample)
        return signal

    @staticmethod
    def demodulate(signal: AnalogSignal,
                   f0: float = 1.0,
                   f1: float = 2.0,
                   samples_per_bit: int = 50) -> Bits:
        bits: Bits = []
        signal_length = len(signal)
        if signal_length % samples_per_bit != 0:
            raise ValueError("Signal length is not a multiple of samples_per_bit")
        for i in range(0, signal_length, samples_per_bit):
            chunk = signal[i: i + samples_per_bit]
            corr0 = sum(chunk[n] * math.sin(2 * math.pi * f0 * (n / samples_per_bit))
                        for n in range(samples_per_bit))
            corr1 = sum(chunk[n] * math.sin(2 * math.pi * f1 * (n / samples_per_bit))
                        for n in range(samples_per_bit))
            bits.append(1 if corr1 > corr0 else 0)
        return bits


class PSK:
    @staticmethod
    def modulate(bits: Bits,
                 carrier_freq: float = 1.0,
                 samples_per_bit: int = 50) -> AnalogSignal:
        """
        - 0 => phase 0
        - 1 => phase π
        """
        signal: List[Sample] = []
        for b in bits:
            phase = 0.0 if b == 0 else math.pi
            for n in range(samples_per_bit):
                t = n / samples_per_bit
                sample = math.sin(2 * math.pi * carrier_freq * t + phase)
                signal.append(sample)
        return signal

    @staticmethod
    def demodulate(signal: AnalogSignal,
                   carrier_freq: float = 1.0,
                   samples_per_bit: int = 50) -> Bits:
        bits: Bits = []
        total = len(signal)
        if total % samples_per_bit != 0:
            raise ValueError("Signal length is not a multiple of samples_per_bit")

        for i in range(0, total, samples_per_bit):
            chunk = signal[i: i + samples_per_bit]
            corr = sum(chunk[n] * math.sin(2 * math.pi * carrier_freq * (n / samples_per_bit))
                       for n in range(samples_per_bit))
            bits.append(0 if corr >= 0 else 1)
        return bits

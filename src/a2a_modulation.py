from math import cos, pi, acos
from typing import Optional

from custom_types import AnalogData


class AM:
    @staticmethod
    def forward(
            message: AnalogData,
            carrier_freq: float = 100.0,
            sample_rate: float = 1000.0,
            modulation_index: float = 0.5
    ) -> AnalogData:
        if sample_rate <= 0.0:
            raise ValueError("sample_rate must be positive")
        if carrier_freq <= 0.0:
            raise ValueError("carrier_freq must be positive")

        out: AnalogData = []
        dt = 1.0 / sample_rate
        t = 0.0

        for m in message:
            m_clamped = min(max(m, -1.0), 1.0)
            carrier = cos(2.0 * pi * carrier_freq * t)
            s = (1.0 + modulation_index * m_clamped) * carrier
            out.append(s)
            t += dt

        return out

    @staticmethod
    def reverse(
            signal: AnalogData,
            carrier_freq: float = 100.0,
            sample_rate: float = 1000.0,
            modulation_index: float = 0.5
    ) -> AnalogData:
        if sample_rate <= 0.0:
            raise ValueError("sample_rate must be positive")
        if carrier_freq <= 0.0:
            raise ValueError("carrier_freq must be positive")
        if modulation_index == 0.0:
            raise ValueError("modulation_index must be non-zero")

        out: AnalogData = []
        dt = 1.0 / sample_rate
        t = 0.0
        prev_m = 0.0
        eps = 1e-6

        for s in signal:
            carrier = cos(2.0 * pi * carrier_freq * t)
            if abs(carrier) < eps:
                m_hat = prev_m
            else:
                m_hat = (s / carrier - 1.0) / modulation_index
                m_hat = min(max(m_hat, -1.0), 1.0)

            out.append(m_hat)
            prev_m = m_hat
            t += dt

        return out


class FM:
    @staticmethod
    def forward(
            message: AnalogData,
            carrier_freq: float = 100.0,
            sample_rate: float = 1000.0,
            freq_deviation: float = 50.0
    ) -> AnalogData:
        if sample_rate <= 0.0:
            raise ValueError("sample_rate must be positive")
        if carrier_freq <= 0.0:
            raise ValueError("carrier_freq must be positive")
        if freq_deviation <= 0.0:
            raise ValueError("freq_deviation must be positive")

        out: AnalogData = []
        dt = 1.0 / sample_rate
        phi = 0.0

        for m in message:
            m_clamped = min(max(m, -1.0), 1.0)
            f_inst = carrier_freq + freq_deviation * m_clamped
            phi += 2.0 * pi * f_inst * dt
            out.append(cos(phi))

        return out

    @staticmethod
    def _unwrap_phase(prev_phi: Optional[float], s: float) -> float:
        x = s
        if x > 1.0:
            x = 1.0

        elif x < -1.0:
            x = -1.0

        raw = acos(x)

        if prev_phi is None:
            return raw

        cand1 = raw
        cand2 = -raw

        def wrap_close(c: float, ref: float) -> float:
            while c - ref > pi:
                c -= 2.0 * pi
            while c - ref < -pi:
                c += 2.0 * pi
            return c

        cand1 = wrap_close(cand1, prev_phi)
        cand2 = wrap_close(cand2, prev_phi)

        if abs(cand1 - prev_phi) <= abs(cand2 - prev_phi):
            return cand1
        return cand2

    @staticmethod
    def reverse(
            signal: AnalogData,
            carrier_freq: float = 100.0,
            sample_rate: float = 1000.0,
            freq_deviation: float = 50.0
    ) -> AnalogData:
        if sample_rate <= 0.0:
            raise ValueError("sample_rate must be positive")
        if carrier_freq <= 0.0:
            raise ValueError("carrier_freq must be positive")
        if freq_deviation <= 0.0:
            raise ValueError("freq_deviation must be positive")

        out: AnalogData = []
        dt = 1.0 / sample_rate

        prev_phi: Optional[float] = None
        prev_inst_freq = carrier_freq

        for s in signal:
            phi = FM._unwrap_phase(prev_phi, s)

            if prev_phi is None:
                inst_freq = carrier_freq
            else:
                dphi = phi - prev_phi
                inst_freq = dphi / (2.0 * pi * dt)

            prev_phi = phi
            inst_freq = 0.5 * inst_freq + 0.5 * prev_inst_freq
            prev_inst_freq = inst_freq

            m_hat = (inst_freq - carrier_freq) / freq_deviation
            m_hat = min(max(m_hat, -1.0), 1.0)
            out.append(m_hat)

        return out


class PM:
    @staticmethod
    def forward(
            message: AnalogData,
            carrier_freq: float = 100.0,
            sample_rate: float = 1000.0,
            phase_deviation: float = pi / 4.0
    ) -> AnalogData:
        if sample_rate <= 0.0:
            raise ValueError("sample_rate must be positive")
        if carrier_freq <= 0.0:
            raise ValueError("carrier_freq must be positive")
        if phase_deviation <= 0.0:
            raise ValueError("phase_deviation must be positive")

        out: AnalogData = []
        dt = 1.0 / sample_rate
        t = 0.0

        for m in message:
            m_clamped = min(max(m, -1.0), 1.0)
            phi = 2.0 * pi * carrier_freq * t + phase_deviation * m_clamped
            out.append(cos(phi))
            t += dt

        return out

    @staticmethod
    def reverse(
            signal: AnalogData,
            carrier_freq: float = 100.0,
            sample_rate: float = 1000.0,
            phase_deviation: float = pi / 4.0
    ) -> AnalogData:
        if sample_rate <= 0.0:
            raise ValueError("sample_rate must be positive")
        if carrier_freq <= 0.0:
            raise ValueError("carrier_freq must be positive")
        if phase_deviation <= 0.0:
            raise ValueError("phase_deviation must be positive")

        out: AnalogData = []
        dt = 1.0 / sample_rate

        prev_phi: Optional[float] = None
        t = 0.0

        for s in signal:
            phi = FM._unwrap_phase(prev_phi, s)
            prev_phi = phi

            phi_c = 2.0 * pi * carrier_freq * t
            base_phi = phi - phi_c

            while base_phi > pi:
                base_phi -= 2.0 * pi
            while base_phi < -pi:
                base_phi += 2.0 * pi

            m_hat = base_phi / phase_deviation
            m_hat = min(max(m_hat, -1.0), 1.0)
            out.append(m_hat)

            t += dt

        return out

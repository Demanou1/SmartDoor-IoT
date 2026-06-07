# adc_ads7830.py
# Smart Door System — ADS7830 lesen (LDR -> Tag/Nacht)
# Autor: Ydriss Armel Demanou | Westfälische Hochschule Gelsenkirchen 2026

from smbus2 import SMBus

class ADS7830:
    """
    ADS7830: 8-Bit ADC via I2C.
    Liefert Werte 0..255.
    Hoeher = dunkler (LDR-Widerstand steigt bei Dunkelheit).
    """

    def __init__(self, bus_id: int, addr: int = 0x4B):
        self.addr = addr
        self.bus  = SMBus(bus_id)

    def read_channel(self, ch: int = 0) -> int:
        """
        Kanal lesen (ch: 0..7).
        Command: Single-ended, internal ref, power-down between conversions.
        """
        if not (0 <= ch <= 7):
            raise ValueError("Channel must be 0..7")

        # ADS7830 Command Byte (TI Datasheet):
        # Bit 7-6: 1 0 (Single-ended)
        # Bit 5-4: C2 C1 C0 (Kanal)
        # Bit 3-0: PD1 PD0 (Power-Down)
        cmd = 0x84 | ((ch & 0x07) << 4)

        self.bus.write_byte(self.addr, cmd)
        return self.bus.read_byte(self.addr)

    def is_night(self, threshold: int = 210) -> bool:
        """
        Gibt True zurueck wenn Dunkelheit erkannt (ADC-Wert > Schwellenwert).
        """
        wert = self.read_channel(0)
        return wert > threshold

    def close(self):
        self.bus.close()

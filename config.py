# config.py
# Smart Door System — Konfiguration & GPIO-Zuordnung
# Autor: Ydriss Armel Demanou | Westfälische Hochschule Gelsenkirchen 2026

from dataclasses import dataclass

@dataclass(frozen=True)
class GPIOPins:
    PIR:         int = 16   # PIR-Sensor HC-SR501 — Bewegungserkennung
    SERVO:       int = 13   # SG90 Servomotor — PWM 50 Hz
    BUZZER:      int = 17   # Passiver Piezo-Buzzer
    BUTTON_BELL: int = 6    # Klingeltaster (interner Pull-Up)
    LED_R:       int = 19   # RGB-LED Rot
    LED_G:       int = 20   # RGB-LED Gruen
    LED_B:       int = 21   # RGB-LED Blau

@dataclass(frozen=True)
class I2CConfig:
    BUS:      int = 1
    ADC_ADDR: int = 0x4B   # ADS7830 ADC (LDR -> Tag/Nacht-Erkennung)
    LCD_ADDR: int = 0x27   # LCD1602 via PCF8574 I2C-Adapter

@dataclass(frozen=True)
class WebConfig:
    HOST:     str = "0.0.0.0"
    PORT:     int = 8080
    USERNAME: str = "admin"
    PASSWORD: str = "admin"   # Im Produktivbetrieb unbedingt aendern!

@dataclass(frozen=True)
class TelegramConfig:
    BOT_TOKEN: str = "PASTE_YOUR_TOKEN_HERE"
    CHAT_ID:   str = "PASTE_YOUR_CHAT_ID_HERE"

@dataclass(frozen=True)
class SystemConfig:
    NIGHT_THRESHOLD: int = 210   # ADC-Schwellenwert (0..255) fuer Tag/Nacht
    RFID_TIMEOUT_S:  int = 8     # Wartezeit auf RFID nach Bewegungserkennung
    DOOR_OPEN_S:     int = 3     # Dauer Tueroeffnung in Sekunden
    PIR_COOLDOWN_S:  int = 5     # Mindestpause zwischen zwei PIR-Ereignissen

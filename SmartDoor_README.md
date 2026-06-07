# Smart Door System — Intelligentes Zugangskontrollsystem

![Status](https://img.shields.io/badge/Status-Abgeschlossen%202026-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%204B-red)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Webserver-Flask-orange)
![Protokoll](https://img.shields.io/badge/Protokoll-I%C2%B2C%20%7C%20SPI%20%7C%20GPIO-lightgrey)
![Hochschule](https://img.shields.io/badge/Westf%C3%A4lische%20Hochschule-Gelsenkirchen-green)

> **Intelligentes, lokal betriebenes Türüberwachungssystem auf Basis eines Raspberry Pi 4 — mit RFID-Zugangskontrolle, PIR-Bewegungssensor, Tag-/Nacht-Erkennung, Flask-Webserver und Telegram-Benachrichtigung mit Foto. Realisiert als funktionsfähiger Prototyp in einem Mini-Haus-Modell.**

---

## Projektinfo

| | |
|---|---|
| **Hochschule** | Westfälische Hochschule Gelsenkirchen |
| **Studiengang** | Elektrotechnik |
| **Betreuer** | Prof. Dr. Christos Georgiadis |
| **Autor** | Ydriss Armel Demanou  |
| **Datum** | Februar 2026 |

---

## Inhaltsverzeichnis

- [Projektübersicht](#projektübersicht)
- [Systemarchitektur](#systemarchitektur)
- [Hardware & Komponenten](#hardware--komponenten)
- [GPIO-Belegung](#gpio-belegung)
- [Softwarearchitektur](#softwarearchitektur)
- [Funktionsablauf](#funktionsablauf)
- [Demonstrationsmodell](#demonstrationsmodell-mini-haus)
- [Testergebnisse](#testergebnisse)
- [Installation](#installation)
- [Projektstruktur](#projektstruktur)
- [Autor](#autor)

---

## Projektübersicht

Ziel des Projekts ist die Entwicklung eines intelligenten, **lokal betriebenen** Smart-Door-Systems ohne Cloud-Anbindung. Das System kombiniert mehrere Sensoren und Aktoren zu einer vollautomatischen Türüberwachung mit folgenden Kernfunktionen:

- Bewegungserkennung via PIR-Sensor (HC-SR501)
- Tag-/Nacht-Unterscheidung via LDR + ADS7830 ADC (I²C)
- RFID-Zugangskontrolle (MFRC522, SPI)
- Automatische Türöffnung via Servomotor (SG90, PWM)
- Akustische & visuelle Statusanzeige (RGB-LED + Buzzer)
- Lokales LCD1602-Display (I²C, PCF8574)
- Webbasierte Steuerung via Flask-Webserver (Port 8080)
- Telegram-Benachrichtigung mit Foto bei Klingelereignis

**Design-Prinzip:** Alle Daten werden lokal verarbeitet — keine Cloud, keine externen Dienste außer Telegram-API.

---

## Systemarchitektur

```
                        ┌─────────────────────┐
                        │    Telegram Bot      │
                        │  Benachrichtigung    │
                        │  bei Klingel + Foto  │
                        └──────────┬──────────┘
                                   │ HTTPS
┌──────────────────────────────────▼──────────────────────────────────┐
│                        Raspberry Pi 4B                               │
│                   (Zentrale Steuereinheit)                           │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  ┌──────────┐  │
│  │ Hauptlogik  │  │  Webserver  │  │  Telegram-   │  │  Bild-   │  │
│  │  main.py    │  │  Flask:8080 │  │  notify.py   │  │speicher  │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────────┘  └──────────┘  │
│         │                │                                           │
│  ┌──────▼──────────────────────────────────────────┐               │
│  │            GPIO / I²C / SPI Abstraktionsschicht  │               │
│  └──────┬──────────────────────────────────────────┘               │
└─────────┼───────────────────────────────────────────────────────────┘
          │
    ┌─────┴──────────────────────────────────────────────┐
    │                   Feldebene                         │
    │                                                     │
    │  EINGABEN (Sensoren):          AUSGABEN (Aktoren):  │
    │  PIR HC-SR501 → GPIO 16        Servo SG90 → GPIO 13 │
    │  LDR + ADS7830 → I²C (0x4B)   RGB-LED → GPIO 19/20/21│
    │  RFID MFRC522 → SPI            Buzzer → GPIO 17    │
    │  Klingel-Taster → GPIO 6       LCD1602 → I²C (0x27)│
    │  Pi-Kamera OV5647 → CSI                            │
    └─────────────────────────────────────────────────────┘
          │
    ┌─────▼───────────────┐
    │  Flask Webserver     │
    │  http://<IP>:8080    │
    │  • Tür öffnen/schließen│
    │  • Status anzeigen   │
    │  • Fotos anzeigen    │
    │  • Passwortschutz    │
    └─────────────────────┘
```

---

## Hardware & Komponenten

| Komponente | Modell | Schnittstelle | Funktion |
|---|---|---|---|
| **Einplatinencomputer** | Raspberry Pi 4B | — | Zentrale Steuereinheit, Linux, Multithreading |
| **Kamera** | Pi Camera OV5647 | CSI | Fotoaufnahme bei Ereignissen |
| **Bewegungssensor** | HC-SR501 PIR | GPIO 16 | Personenerkennung, Infrarot |
| **Helligkeitssensor** | LDR + ADS7830 | I²C (0x4B) | Tag-/Nacht-Erkennung (ADC 8-Bit, 0–255) |
| **RFID-Leser** | MFRC522 | SPI | Zugangskontrolle via MIFARE-Karte |
| **Servomotor** | SG90 | GPIO 13 (PWM, 50Hz) | Mechanische Türöffnung (0°–90°) |
| **RGB-LED** | Common Cathode | GPIO 19/20/21 | Visuelles Feedback (Grün/Rot/Blau/Weiß) |
| **Buzzer** | Passiv Piezo | GPIO 17 | Akustisches Feedback |
| **Display** | LCD1602 + PCF8574 | I²C (0x27) | Statusanzeige lokal |
| **Klingeltaster** | Taktschalter | GPIO 6 | Besucher-Anfrage |

### Entwicklungsverlauf: ESP32-CAM → Raspberry Pi

Das System startete mit einem ESP32-CAM (Dual-Core Xtensa, integrierte OV2640-Kamera, WLAN). Begrenzte GPIO-Pins und Stabilitätsprobleme bei paralleler Kamera-/WLAN-Nutzung führten zur Migration auf den Raspberry Pi 4B, der Linux-Multithreading, vollständige I²C/SPI/GPIO-Unterstützung und eine dedizierte CSI-Kameraschnittstelle bietet.

---

## GPIO-Belegung

```python
# config.py — GPIO-Konfiguration (BCM-Nummerierung)
@dataclass(frozen=True)
class GPIOPins:
    PIR:         int = 16   # PIR HC-SR501 — Bewegungserkennung
    SERVO:       int = 13   # SG90 Servomotor — PWM 50 Hz
    BUZZER:      int = 17   # Passiver Piezo-Buzzer
    BUTTON_BELL: int = 6    # Klingeltaster (Pull-Up)
    LED_R:       int = 19   # RGB-LED Rot
    LED_G:       int = 20   # RGB-LED Grün
    LED_B:       int = 21   # RGB-LED Blau

@dataclass(frozen=True)
class I2CConfig:
    BUS:      int = 1
    ADC_ADDR: int = 0x4B   # ADS7830 (LDR → Tag/Nacht)
    LCD_ADDR: int = 0x27   # LCD1602 via PCF8574

@dataclass(frozen=True)
class SystemConfig:
    NIGHT_THRESHOLD: int = 210   # ADC 0–255, Schwellenwert Tag/Nacht
    RFID_TIMEOUT_S:  int = 8     # Wartezeit auf RFID nach Bewegung
    DOOR_OPEN_S:     int = 3     # Tür bleibt 3 Sekunden geöffnet
    PIR_COOLDOWN_S:  int = 5     # Pause nach Bewegungserkennung
```

---

## Softwarearchitektur

Das System ist **modular** und **ereignisorientiert** aufgebaut:

```
src/
├── main.py              ← Hauptlogik + GPIO-Setup + Multithreading
├── config.py            ← Konfiguration (GPIO, I²C, Web, Telegram)
├── adc_ads7830.py       ← LDR-Auswertung via ADS7830 (I²C)
├── telegram_notify.py   ← Telegram Bot API (Foto + Nachricht)
└── webserver.py         ← Flask Webserver (REST API + Webinterface)
```

### Multithreading-Struktur

```
Thread 1: Hauptlogik      → PIR, RFID, LDR, Servo, LED, Buzzer
Thread 2: Flask Webserver → /api/status, /api/door/open, /api/allow
Thread 3: Telegram Bot    → Benachrichtigungen asynchron senden
```

### Flask Webserver (REST API)

```python
GET  /api/status      → Systemstatus (Tür, LDR, pending_bell, Log)
POST /api/door/open   → Tür öffnen (Auth erforderlich)
POST /api/door/close  → Tür schließen
POST /api/allow       → Klingel-Freigabe (Besucher einlassen)
```

Passwortschutz via HTTP Basic Auth (`admin / admin` — im Produktivbetrieb ändern).

---

## Funktionsablauf

### 1. Bewegungserkennung (PIR → GPIO 16)
PIR erkennt Infrarotänderung → Mehrfachabfrage zur Entprellung → Ereignis bestätigt

### 2. Tag-/Nacht-Entscheidung (LDR → ADS7830 → I²C)
```python
# adc_ads7830.py
cmd = 0x84 | ((ch & 0x07) << 4)
bus.write_byte(addr, cmd)
wert = bus.read_byte(addr)   # 0–255
nacht = wert > NIGHT_THRESHOLD  # Standard: 210
# Nacht = True → RGB-LED Weiß (Beleuchtung)
```

### 3. RFID-Zugangskontrolle (MFRC522 → SPI)
```
Karte lesen → UID auslesen → Vergleich mit autorisierter UID-Liste
  ✓ Autorisiert: Servo 0°→90°, LED Grün, Buzzer OK-Ton, Log-Eintrag
  ✗ Abgelehnt:   LED Rot blinkt, Buzzer Alarm, Foto + Log-Eintrag
```

### 4. Klingel-Logik (GPIO 6)
```
Klingel gedrückt → Foto aufnehmen (CSI-Kamera) →
Telegram senden (Bild + "Klingel! Besucher an der Tür.") →
Webinterface zeigt "Freigabe erforderlich" →
Nutzer kann via Web Tür öffnen (innerhalb Timeout)
```

### 5. Telegram-Benachrichtigung
```python
# telegram_notify.py
def send_photo(self, photo_path: str, caption: str = ""):
    with open(photo_path, "rb") as f:
        files = {"photo": f}
        data  = {"chat_id": self.chat_id, "caption": caption}
        r = requests.post(f"{self.base}/sendPhoto", data=data,
                          files=files, timeout=20)
        r.raise_for_status()
```

---

## Demonstrationsmodell Mini-Haus

Das System wurde als vollständiger Prototyp in einem **selbstgebauten Mini-Haus aus 3mm Holz** realisiert:

- Tür mit SG90-Servoantrieb
- PIR-Sensor im Frontbereich (Erfassungswinkel 120°)
- LCD1602-Display in der Fassade
- RGB-LED als Statussignal
- Klingeltaster an der Tür
- Raspberry Pi + RFID + LDR im Innenraum
- Verdrahtung über WAGO-Klemmen (wartungsfreundlich)

**Herausforderungen & Lösungen:**
- Stromspitzen Servomotor → optimierte GND-Führung, kurze Leitungen
- PIR-Fehltrigger → softwareseitige Mehrfachabfrage + Cooldown
- Platzmangel → strukturiertes Kabelmanagement, WAGO-Klemmen

---

## Testergebnisse

| Test | Komponente | Ergebnis |
|---|---|---|
| Bewegungserkennung | PIR HC-SR501 | Stabil bei 3–5 m, Fehltrigger durch Mehrfachabfrage reduziert |
| Tag-/Nacht-Erkennung | LDR + ADS7830 | Reproduzierbar, natürliches & künstliches Licht korrekt erkannt |
| RFID-Zugangskontrolle | MFRC522 | Erkennung bei 2–4 cm, 0 Falsch-Positiv/Negativ im Test |
| Klingel + Telegram | GPIO + Bot API | Foto + Nachricht zuverlässig gesendet |
| Webserver | Flask | Stabil unter Parallellast (Multithreading, kein Deadlock) |
| Servomotor | SG90 | Tür öffnet/schließt stabil (0° → 90° → 0°) |
| Reaktionszeit gesamt | System | **< 1 Sekunde** für alle Ereignisse |

---

## Installation

### Voraussetzungen

```bash
# Raspberry Pi OS (Bookworm oder Bullseye) auf RPi 4B
# Python 3.x, pip, I²C und SPI aktiviert

# I²C + SPI aktivieren
sudo raspi-config
# → Interface Options → I2C → Enable
# → Interface Options → SPI → Enable
```

### Abhängigkeiten installieren

```bash
git clone https://github.com/Demanou1/SmartDoor-IoT.git
cd SmartDoor-IoT

pip install RPi.GPIO smbus2 mfrc522 flask picamera2 requests
sudo apt install python3-flask -y
```

### Konfiguration anpassen (`src/config.py`)

```python
class TelegramConfig:
    BOT_TOKEN: str = "DEIN_BOT_TOKEN_HIER"
    CHAT_ID:   str = "DEINE_CHAT_ID_HIER"

class WebConfig:
    PASSWORD: str = "sicheres_passwort"  # Standard: "admin"
```

### System starten

```bash
cd src
python3 main.py

# Webinterface erreichbar unter:
# http://<Raspberry-Pi-IP>:8080
# Login: admin / admin
```

### Als Systemdienst (Autostart)

```bash
sudo nano /etc/systemd/system/smartdoor.service
# [Unit] Description=Smart Door System
# [Service] ExecStart=/usr/bin/python3 /home/pi/SmartDoor-IoT/src/main.py
# [Install] WantedBy=multi-user.target

sudo systemctl enable smartdoor
sudo systemctl start smartdoor
```

---

## Projektstruktur

```
SmartDoor-IoT/
├── README.md
├── src/
│   ├── main.py                  ← Hauptlogik + GPIO + Multithreading
│   ├── config.py                ← GPIO-Pins, I²C, Web, Telegram, System
│   ├── adc_ads7830.py           ← LDR-Auswertung (Tag/Nacht)
│   ├── telegram_notify.py       ← Telegram Bot (Foto + Nachricht)
│   └── webserver.py             ← Flask REST API + Webinterface
├── docs/
│   ├── Projektbericht.pdf       ← Vollständiger Bericht (57 Seiten)
│   ├── Schaltplan_Fritzing.png  ← Vollständiger Schaltplan
│   └── GPIO_Belegung.md         ← Pin-Belegungsplan
└── media/
    ├── minihaus_front.jpg       ← Foto Mini-Haus Frontansicht
    ├── elektronik_intern.jpg    ← Foto interne Verdrahtung
    ├── webinterface.png         ← Screenshot Flask Webserver
    └── telegram_screenshot.png  ← Screenshot Telegram-Benachrichtigung
```

---

## Sicherheit & Datenschutz

- Lokale Verarbeitung — keine Cloud-Anbindung
- Fotos ausschließlich lokal auf dem Raspberry Pi gespeichert
- Passwortschutz für das Webinterface (HTTP Basic Auth)
- Telegram-Benachrichtigung nur bei Klingelereignissen
- Keine permanente Videoüberwachung

---

## Mögliche Erweiterungen

- Fingerabdrucksensor als zweiter Faktor
- HTTPS-Verschlüsselung für den Webserver
- Gesichtserkennung via OpenCV / KI
- Digitaler Lux-Sensor BH1750 (genauer als LDR)
- Mobile App mit direkter Push-Funktion
- Integration in Home Assistant / openHAB

---

## Autor

**Ydriss Armel Demanou**
M.Eng. Elektrotechnik — Automatisierung & Energiesysteme
Westfälische Hochschule Gelsenkirchen | Matrikel: 202523503

- Email: demanouarmel@yahoo.com
- LinkedIn: [linkedin.com/in/ydriss-armel-demanou](https://www.linkedin.com/in/ydriss-armel-demanou-4)
- GitHub: [github.com/Demanou1](https://github.com/Demanou1)

---
*Betreut von Prof. Dr. Christos Georgiadis — Westfälische Hochschule Gelsenkirchen, Campus Gelsenkirchen, Februar 2026*

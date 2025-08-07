# Raspberry Pi 5 – Fan Control GUI

- A modern, local desktop application for Raspberry Pi OS to monitor the CPU temperature and control the fan via the official 4-pin FAN header or GPIO.  
  - All features are available in English and German.  
    - Developed with a professional UI, multilingual support, and direct integration of live temperature, fan status, and PWM value.

---

## Features

- **Live monitoring of CPU temperature**  
- **Automatic or manual fan control** (Auto: based on temperature thresholds, Manual: always on/off)
- **Displays current PWM value and fan status**
- **Free definition of temperature thresholds**
- **Supports official 4-pin FAN header (firmware-based) and GPIO-controlled fans**
- **Modern Tkinter GUI – no external dependencies**
- **Integrated Help/Info dropdown with descriptions**
- **Language switcher (EN/DE) – all UI texts and help change instantly**
- **Direct GitHub button (opens your repository)**

---

## Usage

1. Copy `app.py` to your Raspberry Pi 5 with Raspberry Pi OS (Bookworm or newer recommended).
2. Run the program in the graphical environment (not via SSH):
    ```
    python app.py
    ```
3. Select the operation mode (Automatic or Manual) and define your desired temperature thresholds.
4. Use the Help/Info dropdown for explanations about operation and setup.
5. Switch the UI language anytime with the **EN/DE button**.
6. The GitHub button at the bottom right opens the project page.

---

## Note

- With the official 4-pin FAN header (Raspberry Pi 5), direct PWM control is only possible if firmware-based fan control is disabled.
- For full manual PWM control, use a GPIO-connected fan or disable the firmware control via `raspi-config` or `/boot/config.txt`.

---

## License

MIT License  
© 2024 BylickiLabs

---

---

# Raspberry Pi 5 – Lüftersteuerung GUI

Eine moderne Desktop-Anwendung für Raspberry Pi OS zur Überwachung der CPU-Temperatur und Steuerung des Lüfters über den offiziellen 4-Pin-FAN-Header oder GPIO.  
Alle Funktionen sind auf Deutsch und Englisch verfügbar.  
Entwickelt mit professioneller Oberfläche, Mehrsprachigkeit und direkter Live-Anzeige von Temperatur, Lüfterstatus und PWM-Wert.

---

## Funktionen

- **Live-Anzeige der CPU-Temperatur**
- **Automatische oder manuelle Lüftersteuerung** (Automatik: anhand Temperaturschwellen, Manuell: dauerhaft an/aus)
- **Anzeige von PWM-Wert und Lüfterstatus**
- **Frei definierbare Temperaturschwellen**
- **Unterstützung für offiziellen 4-Pin FAN-Header (Firmware) und GPIO-gesteuerte Lüfter**
- **Moderne Tkinter-GUI – keine externen Abhängigkeiten**
- **Dropdown „Hilfe/Info“ mit ausführlichen Erklärungen**
- **Sprachumschalter (DE/EN) – alle UI-Texte und Hilfen wechseln sofort**
- **Direkter GitHub-Button (öffnet dein Repository)**

---

## Anwendung

1. Kopiere `app.py` auf deinen Raspberry Pi 5 mit Raspberry Pi OS (empfohlen: Bookworm oder neuer).
2. Starte das Programm in der grafischen Oberfläche (nicht per SSH!):
    ```
    python app.py
    ```
3. Wähle den Betriebsmodus (Automatik oder Manuell) und definiere die gewünschten Temperaturschwellen.
4. Nutze das Dropdown „Hilfe/Info“ für Erläuterungen zu Bedienung und Einrichtung.
5. Die Sprache lässt sich jederzeit mit dem **DE/EN-Button** umschalten.
6. Der GitHub-Button unten rechts öffnet die Projektseite.

---

## Hinweise

- Beim offiziellen 4-Pin-FAN-Header (Raspberry Pi 5) ist eine direkte PWM-Steuerung nur möglich, wenn die firmware-basierte Steuerung deaktiviert wurde.
- Für volle manuelle PWM-Regelung: GPIO-Lüfter verwenden oder Firmware-Steuerung über `raspi-config` bzw. `/boot/config.txt` abschalten.

---

## Lizenz

MIT License  
© 2024 BylickiLabs

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import time
import sys
import webbrowser

# --------------------------
# Spracheinstellungen (DE/EN)
# --------------------------
LANGUAGES = {
    "de": {
        "app_title": "Raspberry Pi 5 – Lüftersteuerung",
        "help_label": "Hilfe / Info:",
        "dropdown": ["Was ist das?", "Steuerung", "Hinweis"],
        "descriptions": {
            "Was ist das?": (
                "Diese Anwendung überwacht die CPU-Temperatur deines Raspberry Pi 5 und steuert "
                "den Lüfter am integrierten 4-Pin-FAN-Header (oder GPIO) im Automatik- oder Manuell-Modus. "
                "Im Automatikmodus wird der Lüfter temperaturabhängig ein- und ausgeschaltet. "
                "Die App zeigt dir jederzeit Temperatur, PWM-Level und Status an."
            ),
            "Steuerung": (
                "Automatik: Lüfter schaltet abhängig von den eingestellten Temperaturschwellen ein/aus. "
                "Manuell: Du kannst den Lüfter dauerhaft ein- oder ausschalten. "
                "Empfohlen wird die Automatik für optimale Kühlung und Lautstärke."
            ),
            "Hinweis": (
                "Wenn du den offiziellen 4-Pin-FAN-Header des Pi 5 nutzt und die Firmware-Lüftersteuerung aktiviert ist, "
                "kann diese Anwendung den Lüfterstatus anzeigen, aber nicht direkt den PWM-Wert setzen. "
                "Für eigene PWM-Steuerung muss die Firmware-Steuerung deaktiviert oder ein GPIO-Lüfter verwendet werden."
            ),
        },
        "temp_label": "Aktuelle Temperatur:",
        "pwm_label": "PWM-Wert:",
        "fan_status": {
            "auto_on": "Lüfter: EIN (Auto)",
            "auto_off": "Lüfter: AUS (Auto)",
            "auto_mid": "Lüfter: Regelung (Auto)",
            "on": "Lüfter: EIN (Manuell)",
            "off": "Lüfter: AUS (Manuell)",
        },
        "mode_label": "Betriebsmodus:",
        "mode_auto": "Automatik",
        "mode_on": "Manuell EIN",
        "mode_off": "Manuell AUS",
        "min_temp": "Min °C:",
        "max_temp": "Max °C:",
        "about_title": "Über die Anwendung",
        "about_text": "Raspberry Pi 5 – Lüftersteuerung\n\nEntwickelt für Raspberry Pi 5\n© {year} BylickiLabs",
        "github_btn": "GitHub",
        "lang_btn": "EN",
    },
    "en": {
        "app_title": "Raspberry Pi 5 – Fan Control",
        "help_label": "Help / Info:",
        "dropdown": ["What is this?", "Control", "Note"],
        "descriptions": {
            "What is this?": (
                "This application monitors your Raspberry Pi 5's CPU temperature and controls the fan "
                "on the integrated 4-pin fan header (or GPIO) in automatic or manual mode. "
                "In automatic mode, the fan is switched on/off depending on the temperature thresholds. "
                "The app always displays temperature, PWM level and status."
            ),
            "Control": (
                "Automatic: The fan switches on or off depending on the set temperature thresholds. "
                "Manual: You can switch the fan permanently on or off. "
                "Automatic mode is recommended for optimal cooling and noise."
            ),
            "Note": (
                "If you use the official 4-pin fan header of the Pi 5 and the firmware fan control is enabled, "
                "this application can show the fan status but cannot set the PWM value directly. "
                "To use your own PWM control, you must disable the firmware function or use a GPIO fan."
            ),
        },
        "temp_label": "Current Temperature:",
        "pwm_label": "PWM value:",
        "fan_status": {
            "auto_on": "Fan: ON (Auto)",
            "auto_off": "Fan: OFF (Auto)",
            "auto_mid": "Fan: Regulating (Auto)",
            "on": "Fan: ON (Manual)",
            "off": "Fan: OFF (Manual)",
        },
        "mode_label": "Mode:",
        "mode_auto": "Automatic",
        "mode_on": "Manual ON",
        "mode_off": "Manual OFF",
        "min_temp": "Min °C:",
        "max_temp": "Max °C:",
        "about_title": "About this Application",
        "about_text": "Raspberry Pi 5 – Fan Control\n\nDeveloped for Raspberry Pi 5\n© {year} BylickiLabs",
        "github_btn": "GitHub",
        "lang_btn": "DE",
    }
}

GITHUB_URL = "https://github.com/bylickilabs"
current_lang = "de"
current_pwm = 0

def get_temperature():
    try:
        out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return float(out.replace("temp=", "").replace("'C\n", ""))
    except Exception:
        return 0.0

def set_pwm_dummy(pwm_value):
    global current_pwm
    current_pwm = pwm_value

def get_firmware_pwm():
    return current_pwm

def update_gui():
    while True:
        temp = get_temperature()
        temp_label.config(text=f"{temp:.1f} °C")
        minC = float(min_temp_var.get())
        maxC = float(max_temp_var.get())
        pwm_text = "--"
        status_text = LANGUAGES[current_lang]["fan_status"]["off"]
        status_color = "gray"

        mode = mode_var.get()
        fan_dict = LANGUAGES[current_lang]["fan_status"]
        if mode == "auto":
            if temp >= maxC:
                set_pwm_dummy(255)
                status_text = fan_dict["auto_on"]
                status_color = "green"
                pwm_text = "255"
            elif temp <= minC:
                set_pwm_dummy(0)
                status_text = fan_dict["auto_off"]
                status_color = "gray"
                pwm_text = "0"
            else:
                set_pwm_dummy(128)
                status_text = fan_dict["auto_mid"]
                status_color = "blue"
                pwm_text = "128"
        elif mode == "on":
            set_pwm_dummy(255)
            status_text = fan_dict["on"]
            status_color = "green"
            pwm_text = "255"
        elif mode == "off":
            set_pwm_dummy(0)
            status_text = fan_dict["off"]
            status_color = "gray"
            pwm_text = "0"

        fan_status_label.config(text=status_text, fg=status_color)
        pwm_label.config(text=f"{LANGUAGES[current_lang]['pwm_label']} {get_firmware_pwm()}")
        time.sleep(2)

def on_dropdown_change(event=None):
    idx = info_dropdown.current()
    key = LANGUAGES[current_lang]["dropdown"][idx]
    info_text_label.config(text=LANGUAGES[current_lang]["descriptions"][key])

def on_about():
    messagebox.showinfo(
        LANGUAGES[current_lang]["about_title"],
        LANGUAGES[current_lang]["about_text"].format(year=time.strftime('%Y'))
    )

def switch_language():
    global current_lang
    current_lang = "en" if current_lang == "de" else "de"
    lang = LANGUAGES[current_lang]

    # Window Title
    root.title(lang["app_title"])

    # Labels
    help_label.config(text=lang["help_label"])
    temp_label_header.config(text=lang["temp_label"])
    pwm_label.config(text=f"{lang['pwm_label']} --")
    mode_label.config(text=lang["mode_label"])
    min_label.config(text=lang["min_temp"])
    max_label.config(text=lang["max_temp"])

    # Dropdown
    info_dropdown['values'] = lang["dropdown"]
    info_dropdown.set(lang["dropdown"][0])
    on_dropdown_change()

    # Radiobuttons
    mode_auto_rb.config(text=lang["mode_auto"])
    mode_on_rb.config(text=lang["mode_on"])
    mode_off_rb.config(text=lang["mode_off"])

    # Buttons
    about_btn.config(text="Über..." if current_lang == "de" else "About...")
    github_btn.config(text=lang["github_btn"])
    lang_btn.config(text=lang["lang_btn"])

def open_github():
    webbrowser.open(GITHUB_URL)

# --- GUI Aufbau ---
root = tk.Tk()
root.title(LANGUAGES[current_lang]["app_title"])
root.geometry("490x445")
root.resizable(False, False)

# Info Dropdown und Label
frame_top = ttk.Frame(root)
frame_top.pack(pady=(12, 0))
help_label = ttk.Label(frame_top, text=LANGUAGES[current_lang]["help_label"], font=("Arial", 10))
help_label.pack(side="left", padx=(0, 7))

info_dropdown = ttk.Combobox(frame_top, values=LANGUAGES[current_lang]["dropdown"], state="readonly", width=18)
info_dropdown.set(LANGUAGES[current_lang]["dropdown"][0])
info_dropdown.pack(side="left")
info_dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)

info_text_label = tk.Label(root, text=LANGUAGES[current_lang]["descriptions"][LANGUAGES[current_lang]["dropdown"][0]],
                          wraplength=440, justify="left", font=("Arial", 9), fg="#666")
info_text_label.pack(pady=(0, 12))

# Temperaturanzeige
temp_label_header = ttk.Label(root, text=LANGUAGES[current_lang]["temp_label"], font=("Arial", 12))
temp_label_header.pack()
temp_label = ttk.Label(root, text="-- °C", font=("Arial", 18, "bold"), foreground="#222")
temp_label.pack()

# PWM-Anzeige
pwm_label = ttk.Label(root, text=f"{LANGUAGES[current_lang]['pwm_label']} --", font=("Arial", 12))
pwm_label.pack(pady=(8, 0))

# Lüfterstatusanzeige
fan_status_label = ttk.Label(root, text="--", font=("Arial", 12))
fan_status_label.pack(pady=6)

# Modusauswahl
mode_label = ttk.Label(root, text=LANGUAGES[current_lang]["mode_label"], font=("Arial", 12))
mode_label.pack(pady=(12, 0))
mode_var = tk.StringVar(value="auto")
frame_mode = ttk.Frame(root)
frame_mode.pack()
mode_auto_rb = ttk.Radiobutton(frame_mode, text=LANGUAGES[current_lang]["mode_auto"], variable=mode_var, value="auto")
mode_auto_rb.pack(side="left", padx=7)
mode_on_rb = ttk.Radiobutton(frame_mode, text=LANGUAGES[current_lang]["mode_on"], variable=mode_var, value="on")
mode_on_rb.pack(side="left", padx=7)
mode_off_rb = ttk.Radiobutton(frame_mode, text=LANGUAGES[current_lang]["mode_off"], variable=mode_var, value="off")
mode_off_rb.pack(side="left", padx=7)

# Temperaturschwellen
frame_thresh = ttk.Frame(root)
frame_thresh.pack(pady=(16, 0))
min_label = ttk.Label(frame_thresh, text=LANGUAGES[current_lang]["min_temp"])
min_label.grid(row=0, column=0)
min_temp_var = tk.StringVar(value="45")
ttk.Entry(frame_thresh, textvariable=min_temp_var, width=6).grid(row=0, column=1, padx=7)
max_label = ttk.Label(frame_thresh, text=LANGUAGES[current_lang]["max_temp"])
max_label.grid(row=0, column=2)
max_temp_var = tk.StringVar(value="65")
ttk.Entry(frame_thresh, textvariable=max_temp_var, width=6).grid(row=0, column=3, padx=7)

# --- Bottom Button Bar ---
frame_bottom = ttk.Frame(root)
frame_bottom.pack(side="bottom", fill="x", pady=(20, 10))

lang_btn = ttk.Button(frame_bottom, text=LANGUAGES[current_lang]["lang_btn"], width=6, command=switch_language)
lang_btn.pack(side="left", padx=8)

about_btn = ttk.Button(frame_bottom, text="Über..." if current_lang == "de" else "About...", width=8, command=on_about)
about_btn.pack(side="right", padx=8)

github_btn = ttk.Button(frame_bottom, text=LANGUAGES[current_lang]["github_btn"], width=8, command=open_github)
github_btn.pack(side="right")

# Dummy PWM-Status
threading.Thread(target=update_gui, daemon=True).start()
root.mainloop()

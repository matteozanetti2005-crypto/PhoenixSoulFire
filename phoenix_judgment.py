#!/usr/bin/env python3
"""
PhoenixSoulfire - Judgment Layer
Tool privato per registrare il giudizio umano prima che l'AI prenda il sopravvento.
"""

import os
from datetime import datetime
from pathlib import Path

INCOMING_DIR = Path.home() / "phoenixsoulfire" / "incoming"
LOGS_DIR = Path.home() / "phoenixsoulfire" / "logs"

JUDGMENT_QUESTIONS = [
    "Quale decisione stavi già per prendere prima di vedere questo output?",
    "Cosa in questi numeri ti fa sentire a disagio, anche se 'sembra corretto'?",
    "Se questo report fosse sbagliato, dove sarebbe più probabile che si sbagli?",
    "Quanto ti fideresti di questa analisi se dovessi firmarla con il tuo nome?"
]

def get_new_files():
    if not INCOMING_DIR.exists():
        return []
    return [f for f in INCOMING_DIR.iterdir() if f.is_file()]

def generate_judgment_prompt(filename, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    prompt = f"\n[PhoenixSoulfire] {timestamp}\n"
    prompt += f"File analizzato: {filename}\n\n"
    prompt += "Domande per il tuo giudizio:\n\n"
    for i, q in enumerate(JUDGMENT_QUESTIONS, 1):
        prompt += f"{i}. {q}\n"
    prompt += "\nRispondi con il numero + la tua risposta breve.\n"
    return prompt

def log_interaction(filename, prompt):
    log_file = LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"File: {filename}\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(prompt)
        f.write("\n")

def main():
    files = get_new_files()
    if not files:
        print("Nessun nuovo file da analizzare.")
        return

    for file in files:
        try:
            content = file.read_text(encoding="utf-8")
            prompt = generate_judgment_prompt(file.name, content)
            print(prompt)
            log_interaction(file.name, prompt)

            # Sposta il file dopo l'elaborazione
            processed = INCOMING_DIR / "processed"
            processed.mkdir(exist_ok=True)
            file.rename(processed / file.name)

        except Exception as e:
            print(f"Errore con {file.name}: {e}")

if __name__ == "__main__":
    main()
# ===============================================
# Title: Clouded Judgements - Prototype v1
# Author: Luca Brusasco
# Email: s4518846@studenti.unige.it
# Created on: 2025-05-21
# © 2025 Luca Brusasco. All rights reserved.
#
# This prototype is provided exclusively for internal testing by authorized partners.
# Redistribution, commercial use, or modification without written permission is prohibited.
# ===============================================

import random
import pandas as pd
import IPython.display as disp

# --- PLAYER CONFIGURATION ---
token_reliability = 5      # Permanent reliability
base_threshold = 0         # Base threshold (can be adjusted if needed)

# --- AVAILABLE WEATHER CATEGORIES ---
time_slots = ["Morning", "Afternoon", "Evening"]
event_types = ["Rain", "Wind", "Snow", "Sunny"]
event_intensity = ["Light", "Moderate", "Heavy"]

# --- REAL WEATHER EVENT GENERATION ---
real_event = {
    "time_slot": random.choice(time_slots),
    "type": random.choice(event_types),
    "intensity": random.choice(event_intensity)
}

# --- WEATHER DESCRIPTION WITH POSSIBLE ERRORS ---
def generate_random_description(event, error_level):
    """
    Returns a description of the weather event.
    Introduces random errors based on the specified level.
    """
    time_slot = event["time_slot"]
    event_type = event["type"]
    intensity = event["intensity"]

    # Randomly select fields to alter
    fields = ["time_slot", "type", "intensity"]
    fields_to_alter = random.sample(fields, error_level) if error_level > 0 else []

    if "time_slot" in fields_to_alter:
        time_slot = random.choice([f for f in time_slots if f != time_slot])
    if "type" in fields_to_alter:
        event_type = random.choice([t for t in event_types if t != event_type])
    if "intensity" in fields_to_alter:
        intensity = random.choice([i for i in event_intensity if i != intensity])

    return f"{event_type} {intensity.lower()} expected in the {time_slot.lower()}"

# --- SIMULATION (5 TURNS) ---
received_info = []

print(f"\n🎯 Reliability Tokens: {token_reliability}")
print("\n--- SIMULATION STARTED (5 TURNS) ---")

for turn in range(1, 6):
    temporary_tokens = turn - 1                    # Increases each turn: 0, 1, 2, 3, 4
    threshold = base_threshold + token_reliability + temporary_tokens

    dice_roll = sum(random.randint(1, 6) for _ in range(3))  # 3d6 roll
    diff = dice_roll - threshold

    # Determine error level based on difference
    if diff <= 0:
        error = 0
        symbol = "🔵"  # No error
    elif 1 <= diff <= 3:
        error = 1
        symbol = "🟡"  # Minor error
    elif 4 <= diff <= 6:
        error = 2
        symbol = "🟠"  # Moderate error
    else:
        error = 3
        symbol = "🔴"  # Major error

    sentence = generate_random_description(real_event, error)
    received_info.append((f"Day {turn}", symbol, sentence, dice_roll, threshold, error))

    print(f"\nDay {turn}:")
    print(f"  ℹ️ Info received: {sentence}")

# --- CREATE TABLE WITH RESULTS ---
df = pd.DataFrame(received_info, columns=["Turn", "Level", "Information", "Dice Roll", "Threshold", "Error"])

# --- FINAL EVALUATION ---
correct = [s for _, s, _, _, _, e in received_info if e == 0]
serious = [s for _, s, _, _, _, e in received_info if e == 3]

if len(correct) >= 2:
    evaluation = "✅ Likely correct forecast"
elif len(serious) >= 2:
    evaluation = "❌ Likely wrong forecast"
else:
    evaluation = "❓ Uncertain forecast"

# --- VISUAL OUTPUT ---
disp.display(disp.Markdown("### 🌦️ Real Event:"))
disp.display(disp.Markdown(
    f"- Time slot: **{real_event['time_slot']}**\n"
    f"- Type: **{real_event['type']}**\n"
    f"- Intensity: **{real_event['intensity']}**"
))

disp.display(disp.Markdown("### 📋 Received Info"))
disp.display(df)

disp.display(disp.Markdown(f"### 🔍 Final Evaluation: {evaluation}"))

# som.py
import numpy as np

sample_rate = 44100

# 🎸 Violão — Harmônicos + decaimento suave
def instrumento_1(r, g, b):
    freq = 220 + (r / 255) * 440
    dur = 0.3  # reduzido para ser mais rápido
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = np.exp(-5 * t)
    wave = (np.sin(2 * np.pi * freq * t) +
            0.5 * np.sin(2 * np.pi * 2 * freq * t) +
            0.25 * np.sin(2 * np.pi * 3 * freq * t))
    return 0.3 * wave * envelope

# 🎹 Piano — Ataque rápido, som brilhante
def instrumento_2(r, g, b):
    freq = 220 + (g / 255) * 660
    dur = 0.2
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = np.exp(-8 * t) * (1 - np.exp(-40 * t))
    wave = (np.sin(2 * np.pi * freq * t) +
            0.3 * np.sin(2 * np.pi * 2.5 * freq * t))
    return 0.3 * wave * envelope * (r / 255)

# 🎶 Flauta — Som suave com leve vibração
def instrumento_3(r, g, b):
    freq = 440 + (b / 255) * 220
    dur = 0.3
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    tremolo = 1 + 0.1 * np.sin(2 * np.pi * 5 * t)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-4 * t)
    return 0.3 * wave * envelope * tremolo * (g / 255)

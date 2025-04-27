# som.py
import numpy as np

sample_rate = 44100

# Frequências da escala de C maior (4ª e 5ª oitava)
escalas = {
    "C_maior": np.array([261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]),
    "G_maior": np.array([196.00, 220.00, 246.94, 293.66, 329.63, 369.99, 415.30]),
    "A_menor": np.array([220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 392.00]),
}


def quantizar_para_escala(freq, escala):
    idx = np.abs(escala - freq).argmin()
    return escala[idx]


def criar_envelope(dur, tipo='padrão'):
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    if tipo == 'padrão':
        attack_time = 0.03
        attack = np.clip(t / attack_time, 0, 1)
        decay = np.exp(-3 * (t - attack_time))
        decay[t < attack_time] = 1
        envelope = attack * decay
    elif tipo == 'percussivo':
        envelope = np.exp(-8 * t) * (1 - np.exp(-40 * t))
    else:
        envelope = np.exp(-5 * t)  # fallback
    return envelope

# 🎸 Violão — Harmônicos + decaimento suave
def instrumento_1(r, g, b):
    freq = 220 + (r / 255) * 440
    freq = quantizar_para_escala(freq, escalas["C_maior"])
    dur = 0.4
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = criar_envelope(dur, 'padrão')
    wave = (np.sin(2 * np.pi * freq * t) +
            0.5 * np.sin(2 * np.pi * 2 * freq * t) +
            0.25 * np.sin(2 * np.pi * 3 * freq * t))
    return 0.3 * wave * envelope

# 🎹 Piano — Ataque rápido, som brilhante
def instrumento_2(r, g, b):
    freq = 220 + (g / 255) * 660
    freq = quantizar_para_escala(freq, escalas["G_maior"])
    dur = 0.3
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = criar_envelope(dur, 'percussivo')
    wave = (np.sin(2 * np.pi * freq * t) +
            0.3 * np.sin(2 * np.pi * 2.5 * freq * t))
    return 0.3 * wave * envelope * (r / 255)

# 🎶 Flauta — Som suave com leve vibração
def instrumento_3(r, g, b):
    freq = 440 + (b / 255) * 220
    freq = quantizar_para_escala(freq, escalas["A_menor"])
    dur = 0.5
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    tremolo = 1 + 0.1 * np.sin(2 * np.pi * 5 * t)
    envelope = criar_envelope(dur, 'padrão')
    wave = np.sin(2 * np.pi * freq * t)
    return 0.3 * wave * envelope * tremolo * (g / 255)

# 🎸 Baixo — Som grave e encorpado
def instrumento_4(r, g, b):
    freq = 40 + (r / 255) * 80
    freq = quantizar_para_escala(freq, escalas["C_maior"])
    dur = 0.6
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = criar_envelope(dur, 'padrão')
    wave = (np.sin(2 * np.pi * freq * t) +
            0.2 * np.sign(np.sin(2 * np.pi * freq * t)))
    return 0.3 * wave * envelope * (b / 255)

# som.py atualizado 🎶
import numpy as np

sample_rate = 44100

# Frequências da escala de C maior (várias oitavas)
escalas = {
    "C_maior": np.array([
        65.41, 73.42, 82.41, 87.31, 98.00, 110.00, 123.47,  # 2ª oitava (baixo)
        130.81, 146.83, 164.81, 174.61, 196.00, 220.00, 246.94,  # 3ª oitava
        261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88,  # 4ª oitava
        523.25, 587.33, 659.25, 698.46, 783.99, 880.00, 987.77,  # 5ª oitava
        1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53  # 6ª oitava
    ])
}

def quantizar_para_escala(freq):
    idx = np.abs(escalas["C_maior"] - freq).argmin()
    return escalas["C_maior"][idx]

def criar_envelope(dur, tipo='padrão'):
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    if tipo == 'padrão':
        attack = np.clip(t / 0.03, 0, 1)
        decay = np.exp(-3 * (t - 0.03))
        decay[t < 0.03] = 1
        envelope = attack * decay
    elif tipo == 'percussivo':
        envelope = np.exp(-8 * t) * (1 - np.exp(-40 * t))
    else:
        envelope = np.exp(-5 * t)
    return envelope

# Cria acordes
def criar_acorde(fundamental, tipo="maior"):
    if tipo == "maior":
        freqs = [fundamental, fundamental * (5/4), fundamental * (3/2)]
    elif tipo == "menor":
        freqs = [fundamental, fundamental * (6/5), fundamental * (3/2)]
    elif tipo == "diminuto":
        freqs = [fundamental, fundamental * (6/5), fundamental * (7/5)]
    else:
        freqs = [fundamental]
    return freqs

# 🎸 Violão — médio, acordes, harmônicos
def instrumento_1(r, g, b):
    base_freq = 400 + (r / 255) * 1600
    base_freq = quantizar_para_escala(base_freq)
    dur = 0.5
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = criar_envelope(dur, 'padrão')

    tipo = "maior" if r > g and r > b else "menor" if g > r and g > b else "diminuto"
    freqs = criar_acorde(base_freq, tipo)

    wave = sum(np.sin(2 * np.pi * f * t) + 0.3*np.sin(2 * np.pi * 2*f * t) + 0.2*np.sin(2 * np.pi * 3*f * t) for f in freqs)
    wave /= len(freqs)  # Normalizar
    return 0.3 * wave * envelope

# 🎹 Piano — médio/agudo, percussivo, acordes
def instrumento_2(r, g, b):
    base_freq = 600 + (g / 255) * 1400
    base_freq = quantizar_para_escala(base_freq)
    dur = 0.3
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = criar_envelope(dur, 'percussivo')

    tipo = "maior" if g > r and g > b else "menor" if r > g and r > b else "diminuto"
    freqs = criar_acorde(base_freq, tipo)

    wave = sum(np.sin(2 * np.pi * f * t) + 0.2*np.sin(2 * np.pi * 2.5*f * t) for f in freqs)
    wave /= len(freqs)
    return 0.3 * wave * envelope * (r / 255)

# 🎶 Flauta — agudos, tremolo, harmônicos leves
def instrumento_3(r, g, b):
    base_freq = 2000 + (b / 255) * 4000
    base_freq = quantizar_para_escala(base_freq)
    dur = 0.5
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = criar_envelope(dur, 'padrão')
    tremolo = 1 + 0.1 * np.sin(2 * np.pi * 5 * t)

    tipo = "maior" if b > r and b > g else "menor" if g > r and g > b else "diminuto"
    freqs = criar_acorde(base_freq, tipo)

    wave = sum(np.sin(2 * np.pi * f * t) + 0.15*np.sin(2 * np.pi * 1.5*f * t) for f in freqs)
    wave /= len(freqs)
    return 0.3 * wave * envelope * tremolo * (g / 255)

# 🎸 Baixo — graves puros
def instrumento_4(r, g, b):
    base_freq = 50 + (r / 255) * 100
    base_freq = quantizar_para_escala(base_freq)
    dur = 0.7
    t = np.linspace(0, dur, int(sample_rate * dur), False)
    envelope = criar_envelope(dur, 'padrão')

    tipo = "maior" if r > g and r > b else "menor" if b > r and b > g else "diminuto"
    freqs = criar_acorde(base_freq, tipo)

    wave = sum(np.sin(2 * np.pi * f * t) + 0.2*np.sign(np.sin(2 * np.pi * f * t)) for f in freqs)
    wave /= len(freqs)
    return 0.3 * wave * envelope * (b / 255)

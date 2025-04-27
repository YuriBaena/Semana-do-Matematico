import numpy as np
import sounddevice as sd
import pygame
import math
import sys
from som import instrumento_1, instrumento_2, instrumento_3, instrumento_4
from functions import Pixels, analisar_imagem

sample_rate = 44100
chunk = 1024  # Tamanho do bloco de áudio que será processado e visualizado

# Função para transformar a frequência em cor (Hue)
def freq_para_hue(freq):
    freq = np.clip(freq, 20, 20000)
    escala_log = np.log10(freq / 20) / np.log10(20000 / 20)
    hue = (1 - escala_log) * 270  # 0 = vermelho, 270 = violeta
    return hue

# Função para configurar o estilo musical com base na análise da imagem
def configurar_estilo(brilho, saturacao, variedade, cor_media):
    estilo = {}

    # Define a base da música
    if brilho > 0.5:
        estilo['base_freq'] = 440  # mais agudo
    else:
        estilo['base_freq'] = 220  # mais grave

    if saturacao > 0.5:
        estilo['intensidade'] = 1.0
    else:
        estilo['intensidade'] = 0.6

    if variedade > 0.3:
        estilo['instrumento'] = 'rico'
    else:
        estilo['instrumento'] = 'simples'

    r, g, b = cor_media
    if r > g and r > b:
        estilo['tipo'] = 'agressivo'
    elif g > r and g > b:
        estilo['tipo'] = 'suave'
    elif b > r and b > g:
        estilo['tipo'] = 'misterioso'
    else:
        estilo['tipo'] = 'equilibrado'

    return estilo

# Função para gerar música com base nos pixels e no estilo configurado
def gerar_musica(pixels, estilo):
    ondas = []
    base_freq = estilo['base_freq']
    intensidade = estilo['intensidade']
    instrumento_tipo = estilo['instrumento']
    tipo = estilo['tipo']

    for i in range(0, len(pixels) - 2, 3):
        pixel1 = pixels[i]
        pixel2 = pixels[i + 1]
        pixel3 = pixels[i + 2]
        pixel4 = pixels[i - 1]

        if instrumento_tipo == 'rico':
            onda1 = instrumento_1(*pixel1)
            onda2 = instrumento_2(*pixel2)
            onda3 = instrumento_3(*pixel3)
            onda4 = instrumento_4(*pixel4)
        else:
            # Se simples, use só duas ondas
            onda1 = instrumento_1(*pixel1)
            onda2 = instrumento_2(*pixel2)
            onda3 = np.zeros_like(onda1)
            onda4 = np.zeros_like(onda2)

        # Aplicar variação na frequência
        if tipo == 'agressivo':
            onda1 *= intensidade * 1.2
            onda2 *= intensidade * 1.2
        elif tipo == 'suave':
            onda1 *= intensidade * 0.8
            onda2 *= intensidade * 0.8
        elif tipo == 'misterioso':
            onda1 = np.flip(onda1)  # inverter o som
            onda2 = np.flip(onda2)

        min_len = min(len(onda1), len(onda2), len(onda3), len(onda4))
        combinada = onda1[:min_len] + onda2[:min_len] + onda3[:min_len] + onda4[:min_len]

        # Não normalizar fortemente
        combinada /= max(1, np.max(np.abs(combinada)))

        ondas.append(combinada)

    musica = np.concatenate(ondas)
    musica /= max(1, np.max(np.abs(musica)))
    return musica.astype(np.float32)

# Função para visualizar a música em tempo real
def visualizar_em_tempo_real(musica):
    pygame.init()
    largura, altura = 800, 400
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Visualizador de Espectro 🎧")
    relogio = pygame.time.Clock()

    num_barras = 200
    pos = 0
    rodando = True

    def audio_callback(outdata, frames, time, status):
        nonlocal pos, rodando
        if status:
            print(status)
        end = pos + frames
        if end > len(musica):
            outdata[:] = np.zeros((frames, 1), dtype=np.float32)
            rodando = False
            return
        outdata[:, 0] = musica[pos:end]
        pos = end

    stream = sd.OutputStream(
        samplerate=sample_rate,
        blocksize=chunk,
        channels=1,
        dtype='float32',
        callback=audio_callback
    )
    stream.start()

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        if pos + chunk >= len(musica):
            rodando = False
            continue

        bloco = musica[pos:pos + chunk]
        fft = np.abs(np.fft.rfft(bloco * np.hanning(len(bloco))))
        fft = fft[:num_barras]  # usar só as frequências mais baixas
        if np.max(fft) != 0:
            fft /= np.max(fft)

        tela.fill((10, 10, 10))
        largura_barra = largura / num_barras
        for i in range(num_barras):
            altura_barra = fft[i] * altura
            x = i * largura_barra
            y = altura - altura_barra
            hue = int((i / num_barras) * 360)
            cor = pygame.Color(0)
            cor.hsva = (hue, 100, 100, 100)
            pygame.draw.rect(tela, cor, (x, y, largura_barra - 2, altura_barra))

        pygame.display.flip()
        relogio.tick(60)

    stream.stop()
    stream.close()
    pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, forneça o caminho da imagem como argumento.")
        sys.exit(1)

    caminho_imagem = sys.argv[1]

    print(f"Carregando pixels da imagem: {caminho_imagem}")
    brilho, saturacao, variedade, cor_media = analisar_imagem(caminho_imagem)
    pixels = Pixels(caminho_imagem, porcentagem=0.05)
    print(f"{len(pixels)} pixels lidos. Gerando música...")

    estilo = configurar_estilo(brilho, saturacao, variedade, cor_media)
    musica = gerar_musica(pixels, estilo)

    duracao_total = 30
    samples_maximos = int(sample_rate * duracao_total)
    musica = musica[:samples_maximos]

    visualizar_em_tempo_real(musica)

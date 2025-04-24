import numpy as np
import sounddevice as sd
import pygame
import math
import sys
from som import instrumento_1, instrumento_2, instrumento_3, instrumento_4
from functions import Pixels

sample_rate = 44100
chunk = 1024  # Tamanho do bloco de áudio que será processado e visualizado


def freq_para_hue(freq):
    freq = np.clip(freq, 20, 20000)
    escala_log = np.log10(freq / 20) / np.log10(20000 / 20)
    hue = (1 - escala_log) * 270  # 0 = vermelho, 270 = violeta
    return hue


def gerar_musica(pixels):
    ondas = []
    for i in range(0, len(pixels) - 2, 3):
        pixel1 = pixels[i]
        pixel2 = pixels[i + 1]
        pixel3 = pixels[i + 2]
        pixel4 = pixels[i - 1]

        onda1 = instrumento_1(*pixel1)
        onda2 = instrumento_2(*pixel2)
        onda3 = instrumento_3(*pixel3)
        onda4 = instrumento_4(*pixel4)

        min_len = min(len(onda1), len(onda2), len(onda3), len(onda4))
        onda1 = onda1[:min_len]
        onda2 = onda2[:min_len]
        onda3 = onda3[:min_len]
        onda4 = onda4[:min_len]

        combinada = onda1 + onda2 + onda3 + onda4
        combinada /= np.max(np.abs(combinada))
        ondas.append(combinada)

    musica = np.concatenate(ondas)
    musica /= np.max(np.abs(musica))
    return musica.astype(np.float32)


def visualizar_circular_em_tempo_real(musica):
    pygame.init()
    largura, altura = 800, 800
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Visualizador Circular de Frequência")
    relogio = pygame.time.Clock()

    cx, cy = largura // 2, altura // 2
    num_barras = 180
    raio_base = 100
    escala_altura = 300
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
        janela = np.hanning(len(bloco))
        fft = np.abs(np.fft.rfft(bloco * janela))[:num_barras]
        if np.max(fft) != 0:
            fft /= np.max(fft)

        tela.fill((0, 0, 0))

        for i in range(num_barras):
            angulo = (i / num_barras) * 2 * math.pi
            frequencia = i * (sample_rate / 2) / num_barras
            hue = freq_para_hue(frequencia)
            cor = pygame.Color(0)
            cor.hsva = (hue, 100, 100, 100)
            altura_barra = fft[i] * escala_altura

            x_final = int(cx + math.cos(angulo) * (raio_base + altura_barra))
            y_final = int(cy + math.sin(angulo) * (raio_base + altura_barra))

            pygame.draw.line(tela, cor, (cx, cy), (x_final, y_final), 2)

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
    pixels = Pixels(caminho_imagem, porcentagem=0.01)
    print(f"{len(pixels)} pixels lidos. Gerando música...")
    musica = gerar_musica(pixels)

    duracao_total = 15
    samples_maximos = int(sample_rate * duracao_total)
    musica = musica[:samples_maximos]

    visualizar_circular_em_tempo_real(musica)

import numpy as np
import sounddevice as sd
import pygame
from som import instrumento_1, instrumento_2, instrumento_3
from functions import Pixels

sample_rate = 44100
chunk = 1024  # Tamanho do bloco de áudio que será processado e visualizado

def gerar_musica(pixels):
    ondas = []
    for i in range(0, len(pixels) - 2, 3):
        pixel1 = pixels[i]
        pixel2 = pixels[i + 1]
        pixel3 = pixels[i + 2]

        onda1 = instrumento_1(*pixel1)
        onda2 = instrumento_2(*pixel2)
        onda3 = instrumento_3(*pixel3)

        min_len = min(len(onda1), len(onda2), len(onda3))
        onda1 = onda1[:min_len]
        onda2 = onda2[:min_len]
        onda3 = onda3[:min_len]

        combinada = onda1 + onda2 + onda3
        combinada /= np.max(np.abs(combinada))
        ondas.append(combinada)

    musica = np.concatenate(ondas)
    musica /= np.max(np.abs(musica))
    return musica.astype(np.float32)

def visualizar_em_tempo_real(musica):
    pygame.init()
    largura, altura = 800, 400
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Visualizador de Espectro 🎧")
    relogio = pygame.time.Clock()

    num_barras = 150
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
            cor = (100, 200, 255)
            pygame.draw.rect(tela, cor, (x, y, largura_barra - 2, altura_barra))

        pygame.display.flip()
        relogio.tick(60)

    stream.stop()
    stream.close()
    pygame.quit()

if __name__ == "__main__":
    print("Carregando pixels da imagem...")
    pixels = Pixels("DavidHilbert.jpeg", porcentagem=0.01)
    print(f"{len(pixels)} pixels lidos. Gerando música...")
    musica = gerar_musica(pixels)
    
    duracao_total = 15
    samples_maximos = int(sample_rate * duracao_total)
    musica = musica[:samples_maximos]

    visualizar_em_tempo_real(musica)

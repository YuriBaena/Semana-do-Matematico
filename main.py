# main.py
import threading
from som import instrumento_1, instrumento_2, instrumento_3
from functions import Pixels
import numpy as np
import sounddevice as sd
import time

sample_rate = 44100

def tocar_musica(pixels, duracao_total):
    def tocar_onda():
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

        # Tocar o som por um tempo específico (assíncrono)
        sd.play(musica, samplerate=sample_rate)
        time.sleep(duracao_total)  # Durar o tempo especificado
        sd.stop()  # Para o som após o tempo
        print("Som terminou!")

    # Criando uma thread para o som tocar em paralelo
    thread = threading.Thread(target=tocar_onda)
    thread.start()
    thread.join()  # Espera a thread terminar para encerrar o programa

if __name__ == "__main__":
    print("Processando pixels...")
    pixels = Pixels('yuri.jpeg', porcentagem=0.01)
    duracao_total = 10  # Duração total da música (em segundos)
    print(f"{len(pixels)} pixels lidos.")
    tocar_musica(pixels, duracao_total)

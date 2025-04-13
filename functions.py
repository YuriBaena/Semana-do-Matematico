from PIL import Image

# Função para achar pontos na curva de hilbert
def Hilbert_Curve(index, length=1, level=1, offset=False):
    # Define os 4 primeiros pontos da curva de Hilbert (ordem base)
    points = [
        [0, 0],  # canto inferior esquerdo
        [0, 1],  # canto superior esquerdo
        [1, 1],  # canto superior direito
        [1, 0]   # canto inferior direito
    ]

    # Obtém os dois últimos bits do índice para determinar a posição inicial
    i = index & 3
    point = points[i]

    # Loop para cada nível da curva de Hilbert (aumenta a resolução da curva)
    for x in range(1, level):
        val = 2**x  # Fator de escala para este nível (tamanho do quadrante atual)
        
        # Desloca o índice 2 bits para a direita para obter os próximos bits relevantes
        index = index >> 2
        i = index & 3  # Obtém os próximos dois bits

        # Modifica o ponto atual com base no valor de i
        if i == 0:
            # Rotação no sentido horário (espelha diagonalmente)
            point[0], point[1] = point[1], point[0]
            
        elif i == 1:
            # Move o ponto para cima
            point[1] += val

        elif i == 2:
            # Move o ponto para cima e para a direita
            point[0] += val
            point[1] += val

        elif i == 3:
            # Reflexão + rotação no sentido anti-horário
            point[0], point[1] = val - 1 - point[1], val - 1 - point[0]
            point[0] += val  # Move para a direita

    # Escala o ponto para a resolução desejada (multiplica pelo tamanho do quadrado)
    point = [
        point[0] * length, 
        point[1] * length
    ]

    # Adiciona deslocamento opcional (para centralizar o ponto no quadrado)
    if offset:
        point = [
            point[0] + length / 2, 
            point[1] + length / 2
        ]

    return point  # Retorna o ponto (x, y) final na curva de Hilbert


# Função para devolver lista de rgb de cada pixel de uma imagem
#  com o padrão da Curva de Hilbert
def Pixels(caminho_imagem='DavidHilbert.jpeg'):

    # Abrir a imagem e redimensionar
    imagem = Image.open(caminho_imagem).resize((512, 512))

    # Parâmetros da curva de Hilbert
    s = 9  # Nível da curva
    n = 2**s  # Divisões por lado
    t = n * n  # Total de pontos

    largura = altura = 512
    tamanho_celula = largura / n

    # Gerar os pontos da curva
    hilbert_points = [Hilbert_Curve(i, tamanho_celula, s, True) for i in range(t)]

    # Obter os valores RGB na ordem da curva de Hilbert
    pixels = imagem.load()
    cores_rgb = []

    for ponto in hilbert_points:
        x, y = int(ponto[0]), int(ponto[1])
        if 0 <= x < imagem.width and 0 <= y < imagem.height:
            rgb = pixels[x, y]
            cores_rgb.append(rgb)

    return cores_rgb;


if __name__ == "__main__":
    print(Pixels()[:10])
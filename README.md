
# 🎵 **Transformando Pixels em Melodias com a Curva de Hilbert**

Este projeto foi desenvolvido como parte da disciplina de **Cálculo III** e tem como objetivo explorar a interseção entre **matemática, arte e programação**. Utilizando a **curva de Hilbert**, um tipo de curva fractal que preenche o espaço bidimensional, transformamos imagens em trilhas sonoras, criando uma maneira inovadora de "ouvir" as imagens.

## 💡 **Sobre o Projeto**

O projeto utiliza a **curva de Hilbert**, que percorre os pontos de uma imagem de forma contínua e sequencial, preservando a proximidade espacial entre os pixels. A sequência gerada pela curva é então associada a diferentes parâmetros sonoros, como frequência e amplitude, para criar uma interpretação sonora da imagem. A ideia é explorar como dados visuais podem ser transformados em dados auditivos, gerando um tipo de "música" a partir das cores e padrões presentes nas imagens.

### O que faz o projeto:

1. **Transforma uma imagem em uma sequência de pixels** utilizando a curva de Hilbert, que percorre os pontos de forma contínua e sem sobreposição.
2. **Converte cada pixel em parâmetros sonoros**, como frequência, amplitude e duração, para gerar ondas sonoras.
3. **Gera uma trilha sonora** que corresponde à imagem, proporcionando uma nova forma de interagir com os dados visuais.

## 🧠 **Conceitos Envolvidos**

- **Curva de Hilbert**: Uma curva fractal que preenche de maneira contínua e sem sobreposição o espaço bidimensional, preservando a localidade dos pontos.
- **Fractais e Auto-semelhança**: A curva de Hilbert é um exemplo clássico de fractal, apresentando propriedades de auto-semelhança, onde pequenas partes do objeto se repetem em uma escala maior.
- **Processamento de Imagens**: Manipulação de imagens para extrair dados visuais (como cores) e convertê-los em informações utilizáveis para a música.
- **Mapeamento de Dados Visuais para Parâmetros Sonoros**: A conversão das características dos pixels (como cor e brilho) para propriedades acústicas como frequência, amplitude e duração das notas musicais.
- **Computação Criativa**: Uso de ferramentas computacionais para explorar novas formas de arte, ligando áreas de conhecimento aparentemente distantes, como matemática, música e tecnologia.

## 🎹 **Funcionamento do Projeto**

1. **Leitura da Imagem**: A imagem é carregada e redimensionada para um tamanho fixo.
2. **Curva de Hilbert**: A curva é gerada para percorrer os pixels da imagem de maneira ordenada, permitindo uma associação sequencial dos pontos.
3. **Geração das Ondas Sonoras**: Para cada pixel percorrido pela curva, suas cores (RGB) são mapeadas para parâmetros sonoros, e uma onda é gerada para cada um dos três instrumentos (violão, piano e flauta), com a cada instrumento usando um pixel diferente.
4. **Execução da Música**: As ondas sonoras são somadas e reproduzidas, gerando a música a partir dos dados visuais.

## 🛠 **Tecnologias Usadas**

- **Python**: Linguagem de programação utilizada para implementar o projeto.
- **Numpy**: Biblioteca para cálculos numéricos e manipulação de arrays.
- **Sounddevice**: Biblioteca para reprodução de áudio no Python.
- **PIL (Python Imaging Library)**: Biblioteca para manipulação de imagens.
- **Git**: Controle de versão utilizado para gerenciar o código e versões do projeto.

## 🚀 **Como Usar**

### Pré-requisitos

1. **Instalar as dependências**:
   ```
   pip install numpy sounddevice Pillow
   ```

2. **Configurar o projeto**:
   - Certifique-se de que a imagem desejada esteja na pasta de fotos do projeto (exemplo: `Fotos/imagen.jpg`).
   - Ajuste o código, se necessário, para apontar para o arquivo de imagem correto.

3. **Rodar o código**:
   Para gerar a música a partir de uma imagem:
   ```bash
   python main.py nome_da_foto
   ```

4. **Ouça a música**:
   A música gerada será tocada no seu sistema de áudio.

## 📚 **Conclusão**

Este projeto é uma fusão criativa de conceitos matemáticos, artísticos e tecnológicos, demonstrando como diferentes áreas do conhecimento podem ser aplicadas para criar novas formas de arte. Ao utilizar a curva de Hilbert, conseguimos transformar a sequência de pixels de uma imagem em uma trilha sonora única e personalizada, proporcionando uma experiência sensorial que combina visão e audição.

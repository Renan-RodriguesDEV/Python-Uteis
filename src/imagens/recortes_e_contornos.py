import os
import cv2
import numpy as np


def detectar_coordenadas_retangulo(imagem):
    """
    Detecta coordenadas do retângulo usando processamento de imagem

    Passos:
    1. Conversão para escala de cinza
    2. Aplicação de limiarização
    3. Encontrar contornos
    4. Filtrar contornos para encontrar o retângulo do gado
    """
    # Converter imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicar limiarização
    _, imagem_bin = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_BINARY)

    # Encontrar contornos
    contornos, _ = cv2.findContours(
        imagem_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filtrar contornos para encontrar o maior retângulo (presumivelmente o gado)
    contorno_gado = max(contornos, key=cv2.contourArea)

    # Obter retângulo delimitador
    x, y, w, h = cv2.boundingRect(contorno_gado)

    # Desenhar retângulo na imagem original para visualização
    imagem_com_retangulo = imagem.copy()
    cv2.rectangle(imagem_com_retangulo, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return x, y, w, h, imagem_com_retangulo


def recortar_imagem(imagem, coordenadas):
    """
    Recorta a imagem baseado nas coordenadas do retângulo
    """
    x, y, w, h = coordenadas
    imagem_recortada = imagem[y : y + h, x : x + w]
    return imagem_recortada


def fit_transform_from_image(image_path):
    # Carregar imagem
    imagem = cv2.imread(image_path)

    # Pega o diretorio e o basename da imagem
    dir_image, filename_image = os.path.split(image_path)

    # Método 1: Detectar coordenadas automaticamente
    x, y, w, h, imagem_marcada = detectar_coordenadas_retangulo(imagem)
    print(f"Coordenadas detectadas: x={x}, y={y}, largura={w}, altura={h}")

    # Método 2: Definir coordenadas manualmente
    coords_manuais = (x, y, w, h)  # Neste exemplo, usando as coords detectadas

    # Método 3: Extrair coordenadas após desenhar manualmente
    def mouse_crop(event, x, y, flags, param):
        # Exemplo de como rastrear coordenadas com mouse
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"Clique em: x={x}, y={y}")

    # Demonstrar visualizações
    cv2.imshow("Imagem Original com Retângulo", imagem_marcada)
    cv2.setMouseCallback("Imagem Original com Retângulo", mouse_crop)

    # Recortar imagem
    imagem_recortada = recortar_imagem(imagem, coords_manuais)

    # Salvar e mostrar imagens
    cv2.imwrite(f"{dir_image}\\recorte_{filename_image}", imagem_recortada)
    cv2.imshow("Imagem Recortada", imagem_recortada)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # deleta a imagem original
    os.remove(image_path)


if __name__ == "__main__":
    fit_transform_from_image(image_path="your\\path\\to\\image.jpeg")

import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models


def calculate_similarity(image1_path, image2_path):
    # Carrega o modelo ResNet-50 pré-treinado, uma rede neural profunda para extração de características
    model = models.resnet50(pretrained=True)
    # Coloca o modelo em "modo de avaliação" (desativa camadas específicas do treinamento)
    model.eval()

    # Função para extrair características de uma imagem
    def get_features(img_path, model):
        # Abre a imagem e a converte para o espaço de cores RGB
        img = Image.open(img_path).convert("RGB")

        # Define uma sequência de transformações a serem aplicadas na imagem
        transform = transforms.Compose(
            [
                transforms.Resize(
                    (224, 224)
                ),  # Redimensiona a imagem para 224x224 pixels
                transforms.ToTensor(),  # Converte a imagem para um tensor
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),  # Normaliza com médias e desvios padrão específicos
            ]
        )

        # Aplica as transformações e adiciona uma dimensão extra para o "batch size"
        img = transform(img).unsqueeze(0)

        # Desativa o cálculo do gradiente para economizar memória e acelerar a inferência
        with torch.no_grad():
            # Extrai as características da imagem usando o modelo
            features = model(img)

        # Retorna o vetor de características da imagem
        return features

    # Extrai as características das duas imagens usando a função auxiliar
    features1 = get_features(image1_path, model)
    features2 = get_features(image2_path, model)

    # Calcula a similaridade de cosseno entre os vetores de características das duas imagens
    cos = torch.nn.functional.cosine_similarity(features1, features2)
    # Imprime a similaridade como uma porcentagem (multiplicando por 100)
    print(f"Similaridade de Cosseno entre as imagens: {cos.item() * 100}")

    # Retorna a similaridade de cosseno como um número entre -1 e 1
    return cos.item()


# TODO: testes para verificar a similaridade entre as imagens
if __name__ == "__main__":
    calculate_similarity(f"image/path1", f"image/path2")

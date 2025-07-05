import pymysql
import io
import logging
import time
from PIL import Image
from ultralytics import YOLO
from datetime import datetime
from colorama import init, Fore, Style
from dotenv import load_dotenv
import os

# Iniciando arquivo .env
load_dotenv()

# Inicializar colorama para cores no console
init()


class ColorFormatter(logging.Formatter):
    """
    Classe responsável por formatar as mensagens de log com cores diferentes
    dependendo do nível da mensagem (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """

    FORMATS = {
        logging.DEBUG: Fore.BLUE + "%(message)s" + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + "%(message)s" + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + "%(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "%(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Style.BRIGHT + Fore.RED + "%(message)s" + Style.RESET_ALL,
    }

    def format(self, record):
        """
        Seleciona o formato colorido adequado de acordo com o nível do log.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Configura o logger para exibir logs coloridos no console
logger = logging.getLogger()

# Remove handlers anteriores (caso já existam)
if logger.hasHandlers():
    logger.handlers.clear()

# Cria um novo handler para exibir as mensagens no console
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter())  # Usa o formato de cores
logger.addHandler(handler)

# Define o nível de log para DEBUG (exibe todas as mensagens de log, inclusive depuração)
logger.setLevel(logging.DEBUG)


# Função para converter blob para uma imagem PIL
def decode_image(blob_data):
    try:
        logger.info("Decodificando imagem do blob.")
        image = Image.open(io.BytesIO(blob_data))
        return Image.open(
            io.BytesIO(blob_data)
        )  # Reabre para operação normal após verificação
    except Exception as e:
        logger.error(f"Erro ao decodificar a imagem: {e}")
        return None


# Função para processar a detecção com YOLOv8
def detect_objects_in_image(image):
    if image is None:
        logger.error("Imagem inválida ou corrompida, pulando detecção.")
        return None, None

    logger.info("Iniciando detecção de objetos na imagem.")
    model = YOLO("yolov8n.pt")
    results = model(image)

    people_count = 0
    car_count = 0
    for result in results:
        for cls in result.boxes.cls:
            if cls == 0:  # Classe 0 = Pessoa
                people_count += 1
            elif cls == 2:  # Classe 2 = Veículo
                car_count += 1

    logger.info(
        f"Detecção concluída: {people_count} pessoas e {car_count} veículos detectados."
    )
    return people_count, car_count


# Função para buscar informações de limite de pessoas e veículos no circuito
def get_circuit_limits(connection, circuito_id):
    logger.info(
        f"Buscando limites de pessoas e veículos para o circuito {circuito_id}."
    )
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT qtd_pessoas, qtd_veiculos, horario_permitido_inicio, horario_permitido_fim
            FROM tbl_nwCircuito
            WHERE id = %s
            """
            cursor.execute(query, (circuito_id,))
            result = cursor.fetchone()
            if result:
                logger.info(
                    f"Limites obtidos: {result[0]} pessoas, {result[1]} veículos."
                )
                return (result[0], result[1], result[2], result[3])
            else:
                logger.warning(f"Nenhum circuito encontrado para o ID {circuito_id}.")
                return None, None, None, None
    except Exception as e:
        logger.error(f"Erro ao buscar limites do circuito: {e}")
        return None, None, None, None


# Função para verificar se o horário atual está dentro do intervalo permitido
def is_within_allowed_time(start_time, end_time):
    now = datetime.now().time()
    logger.debug(
        f"Horário atual: {now}, Horário permitido: {start_time.time()} - {end_time.time()}"
    )
    return start_time.time() <= now <= end_time.time()


# Função para processar e classificar imagens do banco de dados em lotes
def process_images_from_db(connection, batch_size=10):
    logger.info(
        f"Buscando imagens não classificadas no banco de dados (limite: {batch_size})."
    )
    try:
        with connection.cursor() as cursor:
            query = "SELECT id, blob_img, fk_circuito FROM tbl_nwImagem WHERE classificado = 0 LIMIT %s"
            cursor.execute(query, (batch_size,))
            images = cursor.fetchall()

            if not images:
                logger.info("Nenhuma imagem pendente para classificação.")
                return False  # Retorna False se não houver novas imagens

            for image_row in images:
                img_id = image_row[0]
                logger.info(f"Processando imagem ID {img_id}.")

                blob_data = image_row[1]
                circuito_id = image_row[2]
                logger.debug(
                    f"Tamanho do blob para imagem ID {img_id}: {len(blob_data)} bytes."
                )

                # Decodificar a imagem do blob
                image = decode_image(blob_data)

                if image is None:
                    logger.error(f"Falha ao decodificar a imagem ID {img_id}, pulando.")
                    continue

                # Detectar pessoas e veículos
                people_count, car_count = detect_objects_in_image(image)

                if people_count is None or car_count is None:
                    logger.error(f"Falha na detecção para imagem ID {img_id}, pulando.")
                    continue

                # Buscar os limites de pessoas, veículos e horário permitido para o circuito
                circuito_pessoas, circuito_veiculos, horario_inicio, horario_fim = (
                    get_circuit_limits(connection, circuito_id)
                )

                if circuito_pessoas is None or circuito_veiculos is None:
                    logger.error(
                        f"Falha ao buscar limites para o circuito {circuito_id}, pulando."
                    )
                    continue

                # Verificar se a detecção ocorreu dentro do horário permitido
                if not is_within_allowed_time(horario_inicio, horario_fim):
                    # Se for fora do horário permitido, qualquer detecção de pessoas é um alerta
                    if people_count > 0:
                        logger.warning(
                            f"Imagem ID {img_id}: Alerta! Detecção fora do horário permitido."
                        )
                        tipo_classificado = 1  # Alerta
                    else:
                        logger.info(
                            f"Imagem ID {img_id}: Nenhuma pessoa detectada fora do horário permitido."
                        )
                        tipo_classificado = 0  # Suave
                else:
                    # Classificar a imagem com base nas detecções e nos limites do circuito dentro do horário permitido
                    if people_count > circuito_pessoas or car_count > circuito_veiculos:
                        logger.warning(
                            f"Imagem ID {img_id}: Alerta! Quantidade acima do permitido."
                        )
                        tipo_classificado = 1  # Alerta
                    else:
                        logger.info(f"Imagem ID {img_id}: Classificação normal.")
                        tipo_classificado = 0  # Suave

                # Atualizar a imagem no banco de dados
                update_query = """
                UPDATE tbl_nwImagem
                SET classificado = 1, tipo_classificado = %s
                WHERE id = %s
                """
                cursor.execute(update_query, (tipo_classificado, img_id))
                logger.info(f"Imagem ID {img_id} classificada com sucesso.")

            connection.commit()
            logger.info("Batch de imagens processado com sucesso.")
            return True  # Retorna True se houver imagens processadas
    except Exception as e:
        logger.error(f"Erro ao processar as imagens: {e}")
        return False


# Função principal com loop contínuo e segmentação por lotes
def main():
    batch_size = 30
    interval = 60  # Tempo de espera em segundos entre as execuções
    connection = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USUARIO"),
        password=os.getenv("SENHA"),
        database=os.getenv("DATABASE"),
    )

    while True:
        logger.info("Conectando ao banco de dados e procurando imagens...")
        try:
            # Processar imagens em lotes
            has_processed_images = process_images_from_db(
                connection, batch_size=batch_size
            )

            if not has_processed_images:
                logger.info(
                    f"Aguardando {interval} segundos antes de verificar novamente."
                )
                time.sleep(interval)

        finally:
            connection.close()
            logger.info("Conexão com o banco de dados encerrada.")


if __name__ == "__main__":
    main()

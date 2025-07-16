import time

import pika


class CustomerMessaging:
    """
    Uma classe consumidora de mensagens RabbitMQ que gerencia o consumo de filas.

    Esta classe estabelece uma conexão com um servidor RabbitMQ e consome
    mensagens de uma fila especificada usando uma função de callback fornecida.
    """

    def __init__(
        self,
        queue,
        callback,
        host="localhost",
        port=5672,
        username="guest",
        password="guest",
    ):
        """
        Inicializa a instância CustomerMessaging.

        Args:
            queue (str): Nome da fila RabbitMQ para consumir
            callback (callable): Função para tratar mensagens recebidas
            host (str, optional): Hostname do servidor RabbitMQ. Padrão "localhost"
            port (int, optional): Porta do servidor RabbitMQ. Padrão 5672
            username (str, optional): Nome de usuário para autenticação. Padrão "guest"
            password (str, optional): Senha para autenticação. Padrão "guest"
        """
        # Armazena parâmetros de conexão como atributos privados
        self.__host = host  # Hostname do servidor RabbitMQ
        self.__port = port  # Número da porta do servidor RabbitMQ
        self.__queue = queue  # Nome da fila para consumir mensagens
        self.__callback = (
            callback  # Função definida pelo usuário para processar mensagens
        )

        # Cria credenciais de autenticação para conexão RabbitMQ
        self.__credentials = pika.PlainCredentials(username=username, password=password)

        # Estabelece conexão do canal e configura a fila
        self.channel = self.__create_channel()

    def __create_channel(self):
        """
        Cria e configura um canal RabbitMQ para consumo de mensagens.

        Este método:
        1. Estabelece conexão com o servidor RabbitMQ
        2. Cria um canal
        3. Declara a fila (cria se não existir)
        4. Configura o consumo de mensagens

        Returns:
            pika.channel.Channel: Canal configurado pronto para consumo
        """
        # Cria parâmetros de conexão com host, porta e credenciais
        conn_parameters = pika.ConnectionParameters(
            host=self.__host, port=self.__port, credentials=self.__credentials
        )

        # Estabelece conexão bloqueante e cria canal
        channel = pika.BlockingConnection(conn_parameters).channel()

        # Declara fila com durable=True (sobrevive a reinicializações do servidor)
        channel.queue_declare(queue=self.__queue, durable=True)

        # Configura o consumo de mensagens:
        # - queue: qual fila consumir
        # - on_message_callback: função a chamar quando mensagem chegar
        # - auto_ack=True: confirmar automaticamente o recebimento da mensagem
        channel.basic_consume(
            queue=self.__queue, on_message_callback=self.__callback, auto_ack=True
        )

        return channel

    def start(self):
        """
        Inicia o consumo de mensagens da fila.

        Este método inicia o loop de consumo de mensagens. Ele irá bloquear
        e aguardar por mensagens, chamando a função callback para cada
        mensagem recebida. Pressione CTRL+C para parar o consumo.
        """
        # Exibe mensagem de inicialização com timestamp e informações da fila
        print(
            f"{time.strftime('%X')} - [INFO] Aguardando mensagens na fila '{self.__queue}'. Para sair pressione CTRL+C"
        )

        # Inicia o loop de consumo bloqueante
        # Isso executará indefinidamente até ser parado manualmente
        self.channel.start_consuming()

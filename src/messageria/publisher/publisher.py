import json

import pika


# criando a classe PublisherMessaging que será responsável por publicar mensagens
class PublisherMessaging:
    def __init__(
        self,
        host="localhost",  # endereço do servidor RabbitMQ
        port=5672,  # porta de conexão do RabbitMQ
        username="guest",  # usuário para autenticação
        password="guest",  # senha para autenticação
        routing_key="",  # chave de roteamento para direcionamento da mensagem
        exchange="data_exchange",  # exchange onde as mensagens serão publicadas
    ):
        self.__host = host  # armazena o endereço do servidor
        self.__port = port  # armazena a porta de conexão
        self.__username = username  # armazena o usuário
        self.__password = password  # armazena a senha
        # Nome do exchange (ponto de entrada das mensagens no RabbitMQ)
        self.__routing_key = routing_key  # armazena a chave de roteamento
        # Nome do exchange (ponto de entrada das mensagens no RabbitMQ)
        self.__exchange = exchange  # armazena o nome do exchange
        # cria as credenciais de autenticação
        self.__credentials = pika.PlainCredentials(
            username=self.__username, password=self.__password
        )
        # define propriedades da mensagem (delivery_mode=2 para persistência)
        self.__properties = pika.BasicProperties(delivery_mode=2)
        # cria o canal de comunicação
        self.__channel = self.__create_channel()

    def __create_channel(self):
        """Criando uma conexão com o RabbitMQ."""
        # Parâmetros de conexão com o RabbitMQ
        conn_parameters = pika.ConnectionParameters(
            host=self.__host, port=self.__port, credentials=self.__credentials
        )
        # Retorna um canal de comunicação com o RabbitMQ
        return pika.BlockingConnection(conn_parameters).channel()

    def publish(self, body: dict):
        """Publicando uma mensagem no RabbitMQ."""
        self.__channel.basic_publish(
            exchange=self.__exchange,  # exchange de destino
            routing_key=self.__routing_key,  # chave de roteamento
            body=json.dumps(body),  # converte o dicionário para JSON
            properties=self.__properties,  # propriedades da mensagem
        )

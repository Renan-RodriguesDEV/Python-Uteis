from customer.customer import CustomerMessaging
from publisher.publisher import PublisherMessaging


def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")
    # ch.basic_ack(delivery_tag=method.delivery_tag)


pub = PublisherMessaging(
    routing_key="nova_fila", exchange="my_exchange"
)  # Configura o publisher para enviar mensagens para a fila 'nova_fila'
sub = CustomerMessaging(callback, "nova_fila")

if __name__ == "__main__":
    pub.publish({"message": "Hello, RabbitMQ!"})
    # Inicia o consumo de mensagens
    sub.start()

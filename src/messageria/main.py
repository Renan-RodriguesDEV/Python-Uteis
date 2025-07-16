from src.messageria.customer.customer import CustomerMessaging
from src.messageria.publisher.publisher import PublisherMessaging

pub = PublisherMessaging()
sub = CustomerMessaging("data_queue", pub.publish)

# Inicia o consumo de mensagens
sub.start()
# Publica uma mensagem de exemplo
pub.publish({"message": "Hello, RabbitMQ!"})

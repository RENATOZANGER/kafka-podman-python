from confluent_kafka import Producer
import json
import time
import random

conf = {'bootstrap.servers': 'localhost:9092'}

producer = Producer(conf)

# Função de callback
def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Gerar evento simulado
def gerar_evento_transacao():
    customer_id = random.randint(1000, 9999)
    return {
        "transaction_id": f"TX-{random.randint(100000, 999999)}",
        "customer_id": customer_id,
        "amount": round(random.uniform(10.0, 5000.0), 2),
        "currency": "BRL",
        "timestamp": int(time.time()),
        "status": random.choice(["PENDING", "COMPLETED", "FAILED"]),
        "description": "Compra no ecommerce XYZ"
    }, str(customer_id)  # Usamos o customer_id como key

# Definir tópico
topic = 'meu-topico'

for _ in range(10):
    evento, key = gerar_evento_transacao()
    mensagem = json.dumps(evento)
    producer.produce(
        topic=topic,
        key=key.encode('utf-8'),
        value=mensagem.encode('utf-8'),
        headers=[
            ("event-source", "ecommerce".encode('utf-8')),
            ("env", "dev".encode('utf-8'))
        ],
        callback=delivery_report
    )
    producer.poll(0)
    time.sleep(0.5)
    
producer.flush()

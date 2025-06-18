from confluent_kafka import Consumer, KafkaException, KafkaError
import sys

conf = {
    'bootstrap.servers': 'localhost:9092', # Onde o Kafka está acessível (seu host)
    'group.id': 'meu-grupo-consumidor',    # ID do grupo de consumidores
    'auto.offset.reset': 'earliest',       # Começa a ler do início se não houver offset salvo
    'enable.auto.commit': True,            # Comita offsets automaticamente (cada 5 segundos por padrão)
    'session.timeout.ms': 6000,            # Tempo limite para detectar falha do consumidor no grupo
    'max.poll.interval.ms': 10000          # Tempo máximo entre chamadas de poll antes do consumidor ser considerado falho
}

consumer = Consumer(conf)

# 2. Inscrever-se no Tópico
topic = 'meu-topico'

try:
    consumer.subscribe([topic]) # Inscreve o consumidor no tópico 'meu-topico'

    print(f"Consumidor conectado ao tópico '{topic}'. Aguardando mensagens...")

    while True:
        # Tenta buscar 1 mensagem a cada 1 segundo (timeout=1.0)
        msg = consumer.poll(1.0)

        if msg is None:
            # print("Esperando por mensagens...") # Descomente para ver essa mensagem
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Fim da partição (não é um erro, apenas indica que não há mais mensagens novas por enquanto)
                sys.stderr.write(f"%% {msg.topic()} [{msg.partition()}] no final do offset {msg.offset()}\n")
            elif msg.error():
                # Outros erros
                raise KafkaException(msg.error())
        else:
            # Mensagem recebida com sucesso
            # Adicionei uma verificação para msg.key() e msg.value() antes de decodificar
            key_data = msg.key().decode('utf-8') if msg.key() is not None else 'N/A'
            value_data = msg.value().decode('utf-8') if msg.value() is not None else 'N/A (Mensagem nula ou tombstone)'

            print(f"Recebido: Tópico='{msg.topic()}', Partição={msg.partition()}, Offset={msg.offset()}, Chave='{key_data}', Valor='{value_data}'")

except KeyboardInterrupt:
    print("\nConsumidor interrompido pelo usuário.")
finally:
    # 3. Fechar o Consumidor
    print("Fechando consumidor...")
    consumer.close()

# 🐳 Kafka Local com Python | Producer & Consumer
## Sobre o Projeto

Este projeto disponibiliza um ambiente Kafka completo rodando localmente usando **Podman** (ou Docker) e implementações de **Producer** e **Consumer** em Python, simulando um ambiente real.

## 📦 Stack Utilizada

- 🐳 Kafka (Bitnami)
- 🐳 ZooKeeper (Bitnami)
- 🐳 Kafka UI (provectuslabs/kafka-ui)
- 🐍 Python com confluent-kafka

## 🐍 Instalar dependências Python
```bash
pip install confluent-kafka
```

## 🚀 Como subir o ambiente Kafka

### 1️⃣ Pré-requisitos

- [Podman](https://podman.io/) ou Docker instalado
- Python 3.9+
- pip

### 2️⃣ Subir os containers

```bash
podman-compose up -d
```

## Acesse o Kafka UI em:
➡️ http://localhost:8080

## Executar o Producer e Consumer
### 1️⃣ Producer
```bash
python producer.py
```
### 2️⃣ Consumer
```bash
python consumer.py
```


### 2️⃣ Parar os containers

```bash
podman-compose down
```

### 🔗 O Tópico meu-topico foi criado automaticamente no docker-compose em kafka-init
**Tópico **meu-topico** foi configurado com:
- 3 partições
- Tempo de retenção das mensagens com 1 minuto

---

## 🔧 Comandos Úteis - Ambiente Kafka com Podman

### 🔍 Gerenciamento de tópicos no Kafka
- 👉 Acessar o container Kafka
```bash
podman-compose exec kafka bash
```

🔹 Criar um tópico chamado meu-topico2(com 5 partições, fator de replicação 1 e retenção de 1 minuto)
```bash
kafka-topics.sh --create --topic meu-topico2 --bootstrap-server localhost:9092 \
--partitions 5 --replication-factor 1 --config retention.ms=60000
```

🔹 Verificar os tópicos criados
```bash
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 🔥 Comandos sem precisar entrar no container
🔸 Listar tópicos
```bash
podman exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092
```

🔸 Detalhes do tópico **meu-topico**
```bash
podman exec -it kafka kafka-topics.sh --describe --topic meu-topico --bootstrap-server localhost:9092
```

🔸 Alterar número de partições do Tópico **meu-topico** para 5
```bash
podman exec -it kafka kafka-topics.sh --alter --topic meu-topico --bootstrap-server localhost:9092 --partitions 5
```

🔸 Alterar o tempo de retenção do Tópico **meu-topico** para 2 minutos
```bash
podman exec -it kafka kafka-configs.sh --alter --bootstrap-server localhost:9092 \
--entity-type topics --entity-name meu-topico \
--add-config retention.ms=120000
```

### 📜 Logs dos containers
🔸 Acompanhar logs do Kafka
```bash
podman-compose logs -f kafka
```
🔸 Verificar log da criação do tópico no container kafka-init
```bash
podman logs kafka-init
```

### 🧽 Gerenciar imagens Podman
🔸 Remover uma imagem específica
```bash
podman rmi bitnami/kafka
```

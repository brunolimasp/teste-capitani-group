# Teste - Capitani Group



O projeto de teste Capitani Group foi construído com FastAPI devido à sua facilidade e agilidade na criação de APIs, juntamente com sua documentação automática utilizando recursos da OpenAPI como Swagger e Redoc. Para armazenar os dados, foi utilizado Postgres devido à sua estabilidade, solidez e ampla adoção no mercado. Além disso, para melhorar a capacidade de monitoramento e persistência de eventos relacionados aos dados do Postgres, integrei o Kafka. Utilizei o Kafka para persistir dados em tópicos e adicionei o Kafdrop para facilitar a visualização e monitoramento desses tópicos.


## Instruções e Requisitos


- Certifique-se de ter o Docker instalado em seu ambiente. Se ainda não o tiver, você pode baixá-lo e instalá-lo a partir do site oficial: Docker.

- Após instalar o Docker, abra um terminal ou prompt de comando.

- Navegue até o diretório raiz do projeto onde está localizado o arquivo docker-compose.yml.

- Execute o seguinte comando:


```cmd
docker-compose up -d
```

- Aguarde até que o Docker baixe as imagens, construa os contêineres e inicie o serviço.

- Uma vez que o serviço esteja em execução, você poderá acessar a documentação das API´s pelo Swagger ou Redoc através das rotas: http://127.0.0.1:8000/redoc  ou http://127.0.0.1:8000/docs

- As credenciais para acesso ao banco estão no arquivo `.env`

- Para comunicação do kafka com o banco de dados é necessario efetuar um POST request com as configurações necessarias para o debezium se comunicar com o Postgres conforme o exemplo abaixo:

```javascript 
POST http://localhost:8083/connectors

{
  "name": "postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "develop",
    "database.password": "develop",
    "database.dbname": "db_develop",
    "database.server.name": "dbserver1",
    "table.include.list": "public.products",
    "transforms": "route",
    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "dbserver1.public.products",
    "transforms.route.replacement": "produtos-persistidos"
  }
}
```

### Testes e Simulações

Para realizar um teste e visualizar a mensagem no tópico do Kafka, você pode fazer um POST para a seguinte rota: http://localhost:8000/product/register, com o seguinte payload:

```JSON
{
  "id": "12345",
  "name": "Nome do Produto",
  "description": "Descrição do Produto",
  "pricing": {
    "amount": 100.0,
    "currency": "BRL"
  },
  "availability": {
    "quantity": 50,
    "timestamp": "2024-06-12T12:00:00Z"
  },
  "category": "Categoria do Produto"
}
```

Apos efetuar o post e ter o retorno de sucesso com status code ``201`` é possível visualizar o evento no topico ``produtos-persistidos``, para visualizar o evento basta rodar o seguinte no terminal:

```cmd
kafkacat -b localhost:9092 -t produtos-persistidos
```

Você tabem pode visualizar o evento de forma gráfica gerada pelo kafdro, basta acessar a seguinte rota pelo navegador:

```url
http://localhost:19000/
```

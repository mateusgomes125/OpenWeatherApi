# Weather API

Esta aplicação é uma API de serviço construída em Python usando Flask. Ela coleta dados meteorológicos de várias cidades usando a API do OpenWeather e armazena essas informações em um banco de dados MongoDB. A aplicação é configurada para rodar em um contêiner Docker, garantindo fácil portabilidade e consistência de ambiente.

## Funcionalidades

- **POST `/weather`**: Recebe um `user_id`, coleta dados meteorológicos de cidades específicas e armazena no banco de dados.
- **GET `/weather/<user_id>`**: Retorna o progresso da coleta de dados meteorológicos para o `user_id` fornecido.
- **GET `/city/<user_id>`**: Retorna cidades cadastradas associadas ao usuário `user_id` fornecido.

## Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Configuração e Execução

1. **Clone o Repositório**

   Clone este repositório para o seu ambiente local:

   git clone https://github.com/seu-usuario/weather-api.git
   cd weather-api

# Inicialização do serviço
docker-compose up

# Ferramenta de teste de API(Postman e afins) 
  
  ## Para iniciar o processo da API

  método: POST
  rota: http://127.0.0.1:5000/weather

  JSON body
  {
    "user_id": "12345"
  }

  ## Para acompanhar o progresso da operação da rota POST
  método: GET
  rota: http://127.0.0.1:5000/weather/<user_id>


  ## Para verificar as cidades obtidas por usuário
  método: GET
  rota: http://127.0.0.1:5000/city/<user_id>


# Verificação dos registros inseridos no banco

  - Abra outro terminal

  - execute os comandos:

    docker ps

    docker exec -it <container_id> mongosh

    show dbs

    use weather_db

    show collections

    db.cities.find().pretty()

# Encerramento do serviço
docker-compose down


# Execução do teste
 
Para execução do teste, é necessário rodar a API localmente.
Passos necessários:
  Instalação do Python, versão 3.10 - (https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz)

  Instalação do gerenciador de dependências pip execute o comando `pip install pip`
  
  Instalação do mongoDB - (https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.12-signed.msi)

  # Criação do ambiente virtual
  python3 -m venv venv

  # Ativação o ambiente virtual
  ## LINUX
  source venv/bin/activate

  ## WINDOWS
  venv\Scripts\activate

  # Instalação dos pacotes no ambiente virtual
  pip install -r requirements.txt



  # Excução do teste
  atribua 'test' à variável de ambiente FLASK_ENV no arquivo .env na raíz do projeto
  FLASK_ENV=test
  
  pytest -s test/test_app.py







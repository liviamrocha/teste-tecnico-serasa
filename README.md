<div align=center>

<a href="https://ibb.co/dj8197Z"><img src="https://i.ibb.co/n6xZ2Rp/logo-serasa-experian-color-1-png.webp" alt="logo-serasa-experian-color-1-png" border="0"></a>

	
# Serasa Experian - Teste Técnico

</div>


<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Redis-D9281A?style=for-the-badge&logo=redis&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white"/>
</p>

## Objetivo do projeto

Este projeto tem como objetivo desenvolver uma **API HTTP** utilizando o framework **FastAPI**, que fornecerá um endpoint para simulação de crédito. A aplicação utiliza o banco de dados relacional **Postgres** e o **Redis** para cache de dados, além de ser conteinerizada com **Docker**. O objetivo do projeto é criar um sistema eficiente, seguro e de alta performance para atender às necessidades de simulação de crédito.

## Requisitos


- Criar uma API HTTP com o endpoint **/emprestimos**;

- O endpoint deve:
    - Receber o valor e a parcela de uma simulação de crédito;
    - Buscar as ofertas na
API do parceiro;
    - Filtrar apenas uma oferta que tenha o valor e a parcela menor ou igual ao valor e
parcela simulados;

- Em caso de não encontrar oferta, deve retornar o status code 204 (No Content) representando que
não encontrou oferta;

- A oferta deve ser retornada no formato JSON com os atributos:

    <img src="https://i.ibb.co/z64c4Th/campos-api.png" alt="campos-api" border="0">

    Exemplo JSON de oferta da resposta:

    ```
    {
        "identificador": "9dc2882e-ea08-44e0-860e-5e9b0d13f4bf",
        "parceiro": "bradesco",
        "parcelas": 6,
        "valor": 800
    }
    ```
- Para suportar a volumetria seria ótimo guardar as ofertas retornadas para um CPF em cache.

## Entregas extras
:heavy_check_mark: Armazenamento em cache com Redis;

:heavy_check_mark: Autenticação/Login da API (JWT);

:heavy_check_mark: Conteinerização da aplicação com Docker

:heavy_check_mark: Criação de testes unitários;

:heavy_check_mark: Documentação Swagger/OpenAPI


## Executando o projeto

Passo a passo para execução do projeto:

1) Criar um arquivo .env na raiz do projeto para configuração das variáveis de ambiente do banco de dados (para mais detalhes ver arquivo .env-example.txt).

2) Para executar a aplicação utilizando a imagem Docker, execute o seguinte comando:
```
docker-compose up
```

## API Seresa Crédito

### Endpoints

#### POST /login
- Enpoint responsável por lidar com o processo de autenticação de um usuário na API
- Recebe os dados de login do usuário, incluindo o email e a senha.
- Verifica a validade das credenciais fornecidas. Se as credenciais forem válidas:
    - Gera um token de acesso, que será usado para autenticar as requisições subsequentes à API.
    - Gera um token de atualização, que será usado para renovar o token de acesso quando necessário.
    - Retorna o token de acesso, o token de atualização e o tipo do token ("bearer") como resposta.
   
#### POST /refresh-token

- Endpoint responsável por renovar o token de acesso usado para autenticar as requisições na API.
- Recebe como parâmetro o token de atualização, que é fornecido pelo cliente.
- Verifica se o token de atualização é válido e está associado a um usuário válido. Se o token de atualização for válido:
    - Gera um novo token de acesso com base nas informações do usuário associadas ao token de atualização fornecido.
    - Gera um novo token de atualização, que pode ser usado posteriormente para renovar novamente o token de acesso.
    - Retorna o novo token de acesso, o novo token de atualização e o tipo do token ("bearer") como resposta.

#### POST /create-user
- A rota de criação de usuário é necessária para permitir que os usuários se registrem no sistema e tenham uma conta válida. Sem essa rota, não seria possível adicionar novos usuários ao sistema, o que impediria a utilização posterior do processo de autenticação e autorização.
- Recebe como parâmetro o e-mail e a senha do usuário que está sendo criado.
- É importante ressaltar que, no processo de criação de usuário, todas as senhas fornecidas pelos usuários são devidamente hasheadas antes de serem armazenadas no banco de dados.
- Verifica se já existe um usuário com o mesmo e-mail no banco de dados antes de criar um novo registro. 
    - Se o e-mail já estiver sendo usado, a rota retorna um erro com o código 400 (Solicitação inválida) e uma mensagem informando que o usuário já existe.
    - Caso o e-mail não esteja em uso, um novo registro de usuário é criado no banco de dados.

#### GET /emprestimos
- Recebe os parâmetros "valor" e "parcela" que correspondem a uma simulação de crédito, além do parâmetro "cpf" que representa o CPF do solicitante da simulação.
    - Todos os parâmetros são validados através do pydantic
- Armazenamento em cache
    - Antes de iniciar a busca, é realizada uma verificação para saber se a oferta correspondente ao CPF do solicitante, com os mesmos parâmetros de valor e parcela, está armazenada em cache.
    - Se a oferta estiver em cache, ou seja, se for encontrada uma entrada correspondente à chave no Redis, ela é retornada como resposta imediatamente, evitando a necessidade de fazer uma busca adicional nas fontes de dados externas.
- Busca por ofertas na API dos Parceiros
    - Após a verificação de cache, se não for encontrada uma oferta correspondente aos parâmetros repssados, é realizada a consulta das ofertas disponíveis através da API do parceiro.
    - Nesse processo, é realizada uma chamada à API de parceiros, por meio da classe ParceirosAPI. Essa classe encapsula a lógica de comunicação com os sistemas externos que fornecem as ofertas de empréstimo.
- Filtra as ofertas de crédito
    - A filtragem é feita comparando o valor e o número de parcelas da oferta com os valores da simulação. A oferta que possuir o menor valor e menor número de parcelas, dentro dos limites estabelecidos, será a oferta filtrada. 
    - Caso não haja oferta filtrada para os parâmetros repassados, é lançada uma exceção (HTTP 204 No Content) indicando a ausência de ofertas correspondentes.
    - Quando a oferta filtrada é encontrada, ela é armazenada em cache no Redis. Com o intuito de otimizar o desempenho da aplicação, permitindo que futuras requisições com os mesmos parâmetros sejam atendidas de forma mais rápida, sem a necessidade de consultar novamente as fontes de dados externas.

## Arquitetura do projeto

### Consumo da API do Parceiro

A classe ParceirosAPI foi criada para encapsular a lógica de comunicação entre APIs, fornecendo métodos para autenticação e obtenção de ofertas de crédito dos parceiros. 

Para melhorar a resiliência e o desempenho das requisições, foram utilizados conceitos como rate limiting e backoff.

- Rate limit
    - A biblioeca ratelimit foi utilizada para controlar a taxa de solicitações feita à API do parceiro, limitando o número de chamadas que poderiam ser feitas dentro de um determinado período de tempo, evitando a sobrecarga do servidor ou violação das políticas de uso.
    - O limite utilizado foi de 120 chamadas por minuto.
- Backoff
    - A biblioteca backoff foi utilizada para lidar com falhas temporárias de rede ou indisponibilidade de serviços. 
    - A estraégia consistiu em adicionar atrasos cada vez maiores entre as tentativas de uma requisição em caso de falha, permitindo que o serviço se recuperasse antes da próxima tentativa.

Além do rate limiting e backoff, a classe também inclui uma lógica para lidar com a expiração do token de acesso à API dos parceiros, garantindo que as solicitações sejam feitas com um token válido e evitando erros de autenticação.

### Banco de dados
Para o gerenciamento do banco de dados nesta API, foram adotadas as seguintes tecnologias:
- Postgres: Escolhido como o sistema de gerenciamento de banco de dados relacional.
- SQLModel: Atuando como uma camada de abstração, facilitando a manipulação dos dados do banco de dados por meio de modelos Python. 
- Alembic: Permitindo controlar e aplicar migrações, garantindo que o esquema do banco de dados esteja sempre atualizado com as necessidades do projeto.

### Redis
O Redis foi utilizado nesta API como um sistema de cache para armazenar em memória as ofertas de empréstimo correspondentes a simulações de crédito. Isso permitiu que as respostas fossem retornadas de forma mais rápida, evitando consultas repetidas às fontes de dados externas.

### Conteinerização
A aplicação foi conteinerizada utilizando o Docker, que permitiu a orquestração dos serviços "api", "db" e "redis". Essa abordagem possibilitou a definição das dependências, variáveis de ambiente, mapeamento de portas e volumes necessários para cada serviço. Através da conteinerização, a aplicação pôde ser executada de forma isolada, o que facilitou o desenvolvimento, o empacotamento e a implantação em um ambiente consistente e reproduzível. Isso garantiu que a aplicação pudesse ser executada com as mesmas configurações e dependências em diferentes ambientes, proporcionando maior portabilidade e escalabilidade.

### Testes
Os testes automatizados foram desenvolvidos através da utilização do framework **pytest**. Abaixo segue a cobertura total para todas as rotas da aplicação: 

## Links úteis:
<a href="https://docs.python.org/3/" target="_blank"><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" target="_blank" width="80" height="20"></a> <a href="https://fastapi.tiangolo.com/" target="_blank"><img src="https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white" target="_blank" width="80" height="20"></a <a href="https://swagger.io/docs/" target="_blank"><img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white" target="_blank" width="80" height="20"></a>

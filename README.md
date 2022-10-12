<br>
<p align="center" width="100%">
    <img width="50%" src="https://user-images.githubusercontent.com/99370978/195419585-d471b7bb-befa-4eac-91cc-c997f4285bd1.jpeg"

</p>
<br>
<br>
<p>Projeto final do bootcamp em tecnologia LuizaCode, para criar uma aplicação servidora de APIs REST, a qual irá fornecer um conjunto de APIs para um carrinho de compras de livros.</p>


## Índice
<!--ts-->
   * [Objetivo](#objetivo)
   * [Conceitos](#conceitos)
   * [Diagrama do projeto](#diagrama-do-projeto)
   * [Funcionalidades](#funcionalidades)
   * [Métodos](#métodos)
   * [Respostas](#respostas)
   * [Padrão de endpoints](#padrão-de-endpoints)
   * [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
   * [Especificação do produto](#especificação-do-produto)
   * [Documentação da API Rest com o Swagger](#documentação-da-api-rest-com-o-swagger)
   * [Organização e estruturação do código](#organização-e-estruturação-do-código)
   * [Tecnologias utilizadas](#tecnologias-utilizadas)
   * [Bibliotecas do projeto](#bibliotecas-do-projeto)
   * [Configuração do ambiente](#configuração-do-ambiente)
   * [Autorização e autenticação](#autorização-e-autenticação)
   * [Mecanismos de logging](#mecanismos-de-logging)
   * [Deploy da aplicação](#deploy-da-aplicação)
   * [Informações extras sobre o trabalho](#informações-extras-sobre-o-trabalho)
   * [Membros da equipe](#membros-da-equipe)
<!--te-->
<br />


## Objetivo
<p >Contruir um projeto em Python que funcione como um conjunto de APIs REST para um carrinho de compras da categoria livro. O projeto deve utilizar o framework FastAPI e ter seus registros armazenados no banco de dados MongoDB. </p>
<br />


## Conceitos
Algumas definições importantes sobre o projeto: <br />

● **Clientes**: um cliente é a pessoa que está realizando a compra de um ou mais produtos no sistema. <br />
● **Produtos**: produto que o cliente deseja adquirir. No projeto em questão, o sistema realiza a venda de livros. <br />
● **Carrinho de compras**: é a informação central do projeto, em que um cliente agrupa um ou mais produtos para compra. <br />
● **Carrinho aberto**: é o carrinho ativo no momento. Cada cliente pode ter apenas um carrinho de compras aberto na aplicação. <br />
● **Carrinhos fechados**: são os carrinhos de compras os quais a compra/pedido já foi fechado. <br />
● **Negócio de venda**: livros.
<br />
<br />


## Diagrama do projeto
O diagrama abaixo ilustra como funciona o projeto:
<br />

![House (11)](https://user-images.githubusercontent.com/99370978/195459026-a1fd0160-24b8-4a41-8b21-9d59c6a60ee2.png)




<br />
<br />


## Funcionalidades
**Gerenciamento de cliente:**
- [x] Cadastro de cliente
- [x] Pesquisa de cliente
- [x] Inativação de cliente
- [x] Pesquisa de cliente inativado
- [x] Ativação de cliente
- [x] Cadastro de endereço
- [x] Pesquisa de endereço
- [x] Seleciona endereço de entrega
- [x] Remoção de endereço
<br />

**Gerenciamento de produto:**
- [x] Cadastro de produto
- [x] Atualização de dados do produto
- [x] Pesquisa de produto pelo ID
- [x] Pesquisa de produto pelo nome
- [x] Pesquisa de produto pelo ISBN
- [x] Pesquisa todos os produtos
<br />

**Gerenciamento do carrinho de compras:**
- [x] Criação de carrinho aberto
- [x] Inclusão de itens ao carrinho
- [x] Alteração da quantidade de itens no carrinho
- [x] Consulta de carrinho aberto
- [x] Consulta de carrinhos fechados
- [x] Consulta de produtos e suas quantidade em carrinhos fechados
- [x] Consulta de quantos carrinhos fechados o cliente possui
- [x] Encerramento do carrinho (fechar)
- [x] Identificação do endereço utilizado para entrega
- [x] Validação do estoque
- [x] Exclusão de carrinho aberto
<br />
<br />


## Métodos
As requisições para a API seguem os padrões abaixo:<br />

| Método  | Descrição |
| ------- | --------- |
| GET | Busca e retorna informações dos registros  |
| POST | Cria um novo registro |
| PUT | Atualiza/altera os dados de um registro |
| PATCH | Aplica modificações parciais a um recurso |
| DELETE | Deleta um registro |
<br />


## Respostas

| Tipo | Código | Descrição |
| ---- | ------------- | ------------- |
| Sucesso | 200 | Requisição executada com sucesso (OK) |
| Sucesso | 204 | Solicitação bem sucedida e o cliente não precisa sair da página atual (No Content) |
| Erro no cliente | 400 | Erros de validação ou os campos informados não existem (Bad Request) |
| Erro no cliente | 404 | Registro pesquisado não encontrado (Not Found) |
| Erro no cliente | 409 | A solicitação não pôde ser concluída devido a um conflito com o estado atual do recurso de destino (Conflict) |
<br />
<br />


## Padrão de endpoints
**URL BASE:** http://localhost:8000

**Administrador:**
- Para buscar por todos os clientes, use GET: ```/admin/user/enabled``` 
- Para desativar um cliente pelo e-mail, use PATCH: ```/admin/user/deactivate/{email}``` 

**Login:**
- Para autenticar um usuário, use POST: ```/auth/login``` 

**Cliente:**
- Para cadastrar um cliente, use POST: ```/user``` 
- Para pesquisar um cliente pelo e-mail, use GET: ```/user/{email}``` 

**Endereço:**
- Para adicionar um novo endereço a um usuário, use POST: ```/address```
- Para buscar todos os endereços vinculados a um e-mail, use GET: ```/address/{email}```
- Para selecionar o endereço de entrega, use PATCH: ```/address/delivery/{id}```
- Para deletar o endereço de um usário pelo id do endereço, use DELETE: ```/address/{id_address}```

**Produto:**
- Para cadastrar um produto, use POST: ```/product```
- Para pesquisar um produto pelo ID do MongoDB, use GET: ```/product/{id}```
- Para pesquisar um produto pelo nome/título, use GET: ```/product/title/{title}```
- Para pesquisar todos os produtos, use GET: ```/product```
- Para atualizar os dados do produto pelo ISBN, use PATCH: ```/product/{isbn}```
     
**Carrinho:**  
- Para criar um carrinho baseado no e-mail, use POST: ```/cart/{email}/create```
- Para adicionar produto ao carrinho, use POST: ```/cart/{email}/additem```
- Para alterar a quantidade de um produto do carrinho, use POST: ```/cart/{email}/additem```
- Para remover um produto do carrinho, use PATCH: ```/cart/{email}/removeitem/{isbn}```
- Para buscar carrinho aberto do usuário, use GET: ```/cart/{email}```
- Para deletar um carrinho aberto, use DELETE: ```/cart/{email}/drop```
- Para fechar um carrinho aberto, use DELETE: ```/cart/{email}```
    
**Estoque:**
- Para atualizar a quantidade de itens em estoque pelo ISBN, use PATCH: ```/inventory/{isbn}```
    
**Pedido:**
- Para listar os carrinhos fechados do usuário, use GET: ```/order/{email}```
<br />


## Estrutura do Banco de Dados


![Estruturabancodedados](https://user-images.githubusercontent.com/99370978/195434462-6373319d-27a1-4888-9935-73572d29c7e8.jpeg)


<br />
<br />


## Especificação do produto
As especificações de livros adotadas foram: <br />
 <br />
● Título  <br />
● Autor  <br />
● Editora  <br />
● Ano de publicação  <br />
● Edição  <br />
● Gênero  <br />
● Descrição  <br />
● Linguagem  <br />
● Quantidade de páginas  <br />
● ISBN: 
```sh
O código ISBN é um padrão numérico que funciona como um identificador para livros, artigos, apostilas e outros. 
É composto de 13 números que indicam o título, o autor, o país, a editora e a edição de uma obra. 
Acesse esse site para mais informações: https://www.cblservicos.org.br/isbn/o-que-e-isbn/ 
```
<br />


## Documentação da API Rest com o Swagger
A documentação no Swagger pode ser acessada pelo endereço: http://127.0.0.1.8000/docs
<br />
<br />


## Organização e estruturação do código
O código do projeto foi organizado e estruturado conforme algumas boas práticas da programação:
- Indentação;
- Comentários e Documentação;
- Módulos: organização de pastas por categorias e funcionalidades;
- Convenção de nomes de classes, métodos e variáveis: nomes adequados e padronizados;
- Tratamento de erros (try/except).

Quanto à organização de pastas, seguem alguns prints de demonstração.
- O código do projeto teve a seguinte estruturação: <br />

![estruturapastas](https://user-images.githubusercontent.com/99370978/195454495-8bd58a73-cf5a-4efe-b4e8-849ee3065f4b.png)


<br />
<br />

- A pasta "app" foi subvidida nas seguintes pastas e arquivos: <br />

![pastaapp](https://user-images.githubusercontent.com/99370978/195454872-b831acf2-fa70-403f-9a86-630a83132840.png)

<br />

- Subpastas
- "config": 

![config](https://user-images.githubusercontent.com/99370978/195456140-b469ba68-b71c-43bf-aef0-3fc8cedfe168.png)
<br>

- "controllers": 

![controllers](https://user-images.githubusercontent.com/99370978/195456416-6de75417-daf0-4ede-b9e8-21f0e48d723d.png)

<br />

- "routers":

![routers](https://user-images.githubusercontent.com/99370978/195456982-4c8ea0ab-6f0d-4a93-a91c-83962602ec87.png)


- "schemas": 

![schemas](https://user-images.githubusercontent.com/99370978/195456632-4d180cc3-5c99-4a28-ac5e-d61e6accb24d.png)


- "server": 
 
![server](https://user-images.githubusercontent.com/99370978/195456673-dd7c0b71-01d4-4b26-91f6-7fd14e8922f2.png)
<br />
<br />


## Tecnologias utilizadas

| Tecnologia | Descrição |
| ---------- | --------- |
| [Python](https://www.python.org/downloads/) | Linguagem de programação |
| [Git](https://git-scm.com/) | Sistema de controle de versões do código |
| [GitHub](https://github.com/)| Plataforma para gerenciamento do código, que utiliza o Git como sistema de controle |
| [VSCode](https://code.visualstudio.com/) | Editor de código-fonte |
| [MongoDB](https://www.mongodb.com/) |	Banco de dados |
| [Insomnia](https://insomnia.rest/download) | Framework Open Source para desenvolvimento/teste de API Clients |
| [Heroku](https://www.heroku.com/) | Plataforma nuvem que permite o deploy de aplicações |
| [Docker](https://docs.docker.com/) | Plataforma de software que permite a criação, o teste e a implantação de aplicações rapidamente |
<br />
<br />


## Bibliotecas do projeto
As seguintes bibliotecas do Python estão no projeto:<br />

<p align="left">
• <a href="#fastapi">fastapi</a> 
 <br>
• <a href="#uvicorn">uvicorn</a> 
 <br>
• <a href="#pydantic">pydantic</a> 
 <br>
• <a href="#motor">motor</a> 
 <br>
• <a href="#email-validator">email-validator</a>
 <br>
• <a href="#python-decouple">python-decouple</a>  
 <br>
• <a href="#starlette">starlette</a>  
 <br>
• <a href="#datetime">datetime</a> 
 <br>
• <a href="#python-multipart">python-multipart</a> 
<br>
• <a href="#pyjwt">pyjwt</a> 
<br>
• <a href="#passlib">passlib</a> 
<br>	
</p>
<br />


## Configuração do ambiente
• Criação do ambiente virtual:
```
Windows
python -m venv venv
venv\Scripts\activate
```

```
Linux
virtualenv venv --python=3.10
source venv/bin/activate
```
<br>
		
• Instalação dos requisitos:
```
Windows/Linux
pip install -r requirements.txt
```
<br>
			
• Executar
```
Windows/Linux
uvicorn main:app --reload
```

## Autorização e autenticação
Autorização e autenticação são processos diferentes que ajudam a proteger as informações de uma conta. Enquanto a autorização confirma a identidade de um usuário antes de permitir o seu acesso ao sistema, a autenticação diz respeito as permissões que um usuário tem para acessar determinados recursos e informações.
Instaladas duas bibliotecas do Python para adicionar segurança a aplicação:
<br>
• Passlib: utilizada para gerar o hash de senhas.
<br>
• Pyjwt: gera os JSON Web Tokens, ou JWTs.
<br>
<br />
<br />


## Mecanismos de logging
Mensagens de log são utilizadas para rastrear os eventos que ocorrem quando um software é executado, um evento é representado por uma mensagem descritiva que pode opcionalmente conter o dado de uma variável. Para implementar mecanismos de logging é necessário importar a biblioteca logging, nativa do Python e, adicionar o método basicConfig() para executar a configuração básica, como exemplificado abaixo:

```
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
```

Como a aplicação foi estruturada em módulos, as mensagens de log foram adicionadas atribuindo a variável logger o resultado de ```logging.getLogger(__name__).```
Sendo a construção recomendada para organizar os registradores por módulo, e ```(__name__)``` o nome do módulo.


## Deploy da aplicação
O deploy da aplicação foi feito no Heroku: https://carts-books.herokuapp.com/ , e o projeto contém também os arquivos DockerFile e docker-compose.
<br />
<br />


## Informações extras sobre o trabalho
Das atividades extras solicitadas não foi implementada a criação de testes unitários.
<br />
<br />


## Membros da equipe
- [Amanda Santos Mantovani](https://github.com/amdsantos)
- [Carmen Carolina Mattos de Pontes](https://github.com/carmencmattos)
- [Debora  Martinez](https://github.com/deboraamartinez)
- [Isadora Santana Garcia](https://github.com/isadorasg)
- [Leiliane da Silva Oliveira](https://github.com/Leiliane-Oliveira)
- [Leticia Cavalcanti Andrade de Alcantara](https://github.com/leticiacaa)

<br />
<br />

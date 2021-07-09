
---

# Habilidades mesenvolvidas

- Utilizar o terminal interativo do Python.
- Escrever sospróprios módulos e importá-los em outros códigos.
- Aplicar técnicas de raspagem de dados;
- Extrair dados de conteúdo HTML;
- Armazenar os dados obtidos em um banco de dados;

## Objetivo

 Projeto que tem como principal objetivo fazer consultas em notícias sobre tecnologia, criar um banco de dados, obter dados para popular este banco, e preparar consultas a serem feitas nestas notícias.

As notícias pforam obtidas através da raspagem das [últimas notícias do _TecMundo_](https://www.tecmundo.com.br/novidades).

---
## Antes de começar a desenvolver:

1. Clone o repositório

- Entre na pasta do repositório que você acabou de clonar:

2. Crie o ambiente virtual para o projeto

- `python3 -m venv .venv && source .venv/bin/activate`

3. Instale as dependências

- `python3 -m pip install -r dev-requirements.txt`


---
## Linter

Para garantir a qualidade do código, foi utilizado neste projeto o linter `Flake8`.
Assim o código estará alinhado com as boas práticas de desenvolvimento, sendo mais legível
e de fácil manutenção! Para rodá-lo localmente no projeto, execute o comandos abaixo:

```bash
python3 -m flake8
```

⚠️ Pull Requests com problemas de linter não serão avaliados.

---

# Como desenvolver

## Testes

Para executar os testes certifique-se de que os seguintes passos foram realizados;

1. **criar o ambiente virtual**

```bash
$ python3 -m venv .venv
```

2. **ativar o ambiente virtual**

```bash
$ source .venv/bin/activate
```

3. **instalar as dependências no ambiente virtual**

```bash
$ python3 -m pip install -r dev-requirements.txt
```

📚 Se quiser saber mais sobre a instalação de dependências com `pip`, veja esse [artigo](https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1).

Com o seu ambiente virtual ativo, as dependências serão instaladas neste ambiente.
Quando precisar desativar o ambiente virtual, execute o comando "deactivate". Lembre-se de ativar novamente quando voltar a trabalhar no projeto.

O arquivo `dev-requirements.txt` contém todas as dependências que serão utilizadas no projeto, ele está agindo como se fosse um `package.json` de um projeto `Node.js`.

Com esta preparação feita, podemos executar os testes:

**Executar os testes**

```bash
$ python3 -m pytest
```

Este comando irá executar todos os testes do projeto. Caso o teste falhe e você queira ter um print melhor do erro basta executar o seguinte comando:

```bash
python3 -m pytest -s -vv
```

Caso precise executar apenas um arquivo de testes basta executar o comando:

```bash
python3 -m pytest tests/nomedoarquivo.py
```

Para verificar se você está seguindo o guia de estilo do Python corretamente, execute o comando:

**Verificar o estilo**

```bash
$ python3 -m flake8
```

---

## Raspagem de notícias

As notícias a serem raspadas estarão disponíveis na aba de últimas notícias do _TecMundo_: https://www.tecmundo.com.br/novidades.
Essas notícias form salvas no banco de dados utilizando as funções python que já vêm prontas no módulo `database.py`

## MongoDB

Este projeto, utilizou um banco de dados chamado `tech_news`, e as notícias serão armazenadas em uma coleção chamada `news`. Já existem algumas funções prontas no arquivo `tech_news/database.py` que tauxiliaram no desenvolvimento.

Para instalar e rodar o servidor MongoDB, siga as instruções no tutorial oficial:
Ubuntu: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
MacOS:  https://docs.mongodb.com/guides/server/install/

Lembre-se de que o mongoDB utilizará por padrão a porta 27017. Se já houver outro serviço utilizando esta porta, considere desativá-lo.

---

# Requisitos 

### 1 - função `fetch`
local: `tech_news/scraper.py`

Antes de fazer scrape, precisamos de uma página! Esta função é responsável por fazer a requisição HTTP ao site Tecmundo e obter o conteúdo HTML.
- A função recebe uma URL
- A função faz uma requisição HTTP `get` para esta URL utilizando a função `requests.get`
- A função retorna  o conteúdo HTML da resposta.
- A função respeita um Rate Limit de 1 requisição por segundo; .


✍️ Teste manual: abra um terminal Python importando esta função através do comando `python3 -i tech_news/scraper.py` e invoque a função utilizando diferentes parâmetros. Exemplo: `fetch("https://app.betrybe.com/")`.

**🤖
### 2 - a função `scrape_noticia`
local: `tech_news/scraper.py`

Agora que temos a página HTML, é hora de fazer o scrape! Como a biblioteca Parsel, pobtem os dados que queremos de cada página.

- A função recebe como parâmetro o conteúdo HTML da página de uma notícia da Tecmundo
- A função  no conteúdo recebido, busca as informações das notícias para preencher um dicionário com os seguintes atributos:
  - `url` - link para acesso da notícia. Ex: "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/155000-musk-tesla-carros-totalmente-autonomos.htm"
  - `title` - título da notícia. Ex: "Musk: Tesla está muito perto de carros totalmente autônomos"
  - `timestamp` - data e hora da notícia. Ex: "2020-07-09T11:00:00"
  - `writer` - nome da pessoa autora da notícia. Ex: "Nilton Kleina". Se a informação não for encontrada, salve este atributo como `None`
  - `shares_count` - número de compartilhamento da notícia. Ex: `61`. Se a informação não for encontrada, salve este atributo como `0` (zero)
  - `comments_count` - número de comentários que a notícia recebeu. Ex: `26`
  - `summary` - o primeiro parágrafo da notícia. Ex:"O CEO da Tesla, Elon Musk, garantiu que a montadora está muito perto de atingir o chamado nível 5 de autonomia de sistemas de piloto automático de carros. A informação foi confirmada em uma mensagem enviada pelo executivo aos participantes da Conferência Anual de Inteligência Artificial (WAIC, na sigla em inglês). O evento aconteceu em Xangai, na China, onde a montadora comemora resultados positivos de mercado."
  - `sources` - lista contendo fontes da notícia. Ex: ["Venture Beat", "Source 2"]
  - `categories` - lista de categorias que classificam a notícia. Ex: ["Mobilidade Urbana/Smart Cities", "Veículos autônomos", "Tesla", "Elon Musk"]


### 3 - a função `scrape_novidades`
local: `tech_news/scraper.py`

Com o scrape da página de notícias, busca os links para várias páginas de notícias. Estes links estão  na página Novidades (https://www.tecmundo.com.br/novidades). Esta função faz o scrape da página Novidades para obter as URLs das páginas de notícias.

- recebe uma string com o conteúdo HTML da página Novidades (https://www.tecmundo.com.br/novidades)
- faz o scrape do conteúdo recebido para obter uma lista contendo as URLs das notícias listadas.
- retornar esta lista.
- Caso não encontre nenhuma URL de notícia, retorna uma lista vazia.


### 4 - a função `scrape_next_page_link`
local: `tech_news/scraper.py`

Busca mais notícias, faz a paginação, e o link da próxima página. Esta função sé responsável por fazer o scrape deste link.

-  receber como parâmetro uma `string` contendo o conteúdo HTML da página de novidades (https://www.tecmundo.com.br/novidades)
- fazer o scrape deste HTML para obter a URL da próxima página.
- retornar a URL obtida.
- Caso não encontre o link da próxima página, a função retorna`None`

### 5 - Crie a função `get_tech_news` para obter as notícias!
local: `tech_news/scraper.py`
Aplica todas as funções feitas, as ferramentas prontas, fazem o scraper mais robusto com a paginação.

-receber como parâmetro um número inteiro `n` e buscar as últimas `n` notícias do site.
- Utiliza as funções `fetch`, `scrape_noticia` `scrape_novidades` e `scrape_next_page_link` para buscar as notícias e processar seu conteúdo.
- As notícias buscadas são inseridas no MongoDB; Para acessar o banco de dados, importa e utiliza as funções  prontas em `tech_news/database.py`
- insere as notícias no banco, retorna estas mesmas notícias.

📌 De aqui em diante, usaremos o MongoDB. Para instalar e rodar o servidor MongoDB, siga as instruções no tutorial oficial:
Ubuntu: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
MacOS:  https://docs.mongodb.com/guides/server/install/
Com o servidor rodando, o nosso módulo conseguirá acessá-lo sem problemas. Importe o módulo `tech_news/database.py` e chame as funções contidas nele.


### 6 - Crie a função `search_by_title`
local: `tech_news/analyzer/search_engine.py`

popular nosso banco de dados com notícias, esta função faz  buscas por título.

- recebe uma string com um título de notícia
-  busca as notícias do banco de dados por título
- retorna uma lista de tuplas com as notícias encontradas nesta busca. 
Exemplo: 
```python
[
  ("Título1_aqui", "url1_aqui"),
  ("Título2_aqui", "url2_aqui"),
  ("Título3_aqui", "url3_aqui"),
]
```
- A busca é  _case insensitive_
- nenhuma notícia seja encontrada, retorna uma lista vazia.


### 7 - a função `search_by_date`
local: `tech_news/analyzer/search_engine.py`

Esta função busca as notícias do banco de dados por data.

- recebe como parâmetro uma data no formato "aaaa-mm-dd"
- busca as notícias do banco de dados por data.
- retorna no mesmo formato do requisito anterior.
- data seja inválida, ou esteja em outro formato, uma exceção `ValueError` é lançada com a mensagem `Data inválida`.
-nenhuma notícia seja encontrada, retorna uma lista vazia.

✍️ Teste manual: abra um terminal Python importando esta função através do comando `python3 -i tech_news/analyzer/search_engine.py` e invoque a função utilizando diferentes parâmetros. Exemplo: `search_by_date("2020-11-11")`.

### 8 - Crie a função `search_by_source`,
local: `tech_news/analyzer/search_engine.py`

Esta função busca as notícias por fonte.

- recebe como parâmetro o nome da fonte completo.
- busca as notícias do banco de dados por fonte.
- retorno no mesmo formato do requisito anterior.
- nenhuma notícia  encontrada, retorna uma lista vazia.
- A busca é _case insensitive_

✍️ Teste manual: abra um terminal Python importando esta função através do comando `python3 -i tech_news/analyzer/search_engine.py` e invoque a função utilizando diferentes parâmetros. Exemplo: `search_by_source("Venture Beat")`.


### 9 - Crie a função `search_by_category`
local: `tech_news/analyzer/search_engine.py`

Esta função ibuscca as notícias por categoria.

- recebe como parâmetro o nome da categoria completo.
- busca as notícias do banco de dados por categoria.
- retorna no mesmo formato do requisito anterior.
- nenhuma notícia  encontrada, eetorna uma lista vazia.
- A busca é  _case insensitive_

✍️ Teste manual: abra um terminal Python importando esta função através do comando `python3 -i tech_news/analyzer/search_engine.py` e invoque a função utilizando diferentes parâmetros. Exemplo: `search_by_category("Tesla")`.

### 10 - Crie a função `top_5_news`
local: `tech_news/analyzer/ratings.py`

Esta função lista as cinco notícias mais populares; no critério de popularidade será a soma dos compartilhamentos e comentários.

-  busca as notícias do banco de dados e calcula a sua "popularidade" somando seu número de compartilhamentos e comentários.
-  ordena as notícias por ordem de popularidade.
- O empate, e o desempate dsão por ordem alfabética de título.
- O retorno no mesmo formato do requisito anterior, porém limitado a 5 notícias.
- Caso haja menos de cinco notícias, no banco de dados,  retorna todas as notícias existentes;
- Caso não haja notícias disponíveis, dretorna uma lista vazia.

✍️ Teste manual: abra um terminal Python importando esta função através do comando `python3 -i tech_news/analyzer/ratings.py` e invoque a função utilizando diferentes parâmetros. Exemplo: `top_5_news()`.


### 11 - Crie a função `top_5_categories`
local: `tech_news/analyzer/ratings.py`

Esta função lista as cinco categorias com maior ocorrência no banco de dados. 

- ordenadas por ordem alfabética.
- As top 5 categorias da análise retornadas em uma lista no formato `["category1", "category2"]`;
- Caso haja menos de cinco categorias, no banco de dados, retorna todas as categorias existentes;
- Caso não haja categorias disponíveis,  retorna uma lista vazia.

✍️ Teste manual: abra um terminal Python importando esta função através do comando `python3 -i tech_news/analyzer/ratings.py` e invoque a função utilizando diferentes parâmetros. Exemplo: `top_5_categories()`.
---

### 12 - a função `analyzer_menu`
local: `tech_news/menu.py`

Esta função é o menu do programa. Através dele poderemos operar as funcionalidades criadas. Um menu de opções, em que cada opção pede as informações necessárias para disparar uma ação.
```

- Caso a opção `0` seja selecionada, seve-se exibir a mensagem "Digite quantas notícias serão buscadas:"

- Caso a opção `1` seja selecionada, deve-se exibir a mensagem "Digite o título:";

- Caso a opção `2` seja selecionada, deve-se exibir a mensagem "Digite a data no formato aaaa-mm-dd:";

- Caso a opção `3` seja selecionada, deve-se exibir a mensagem "Digite a fonte:";

- Caso a opção `4` seja selecionada, deve-se exibir a mensagem "Digite a categoria:";

- Caso a opção não exista, exiba a mensagem de erro "Opção inválida" na `stderr`.

📌 A função `input` utilizada para receber a entrada de dados da pessoa usuária.

✍️ Teste manual: dentro de um ambiente virtual onde seu projeto foi configurado, digite o comando `tech-news-analyzer`, o menu deve ser exibido. Isto acontece pois durante a configuração inicial do projeto já configuramos para que a função seja corretamente chamada quando este comando seja invocado.


## Requisitos não implementados:
### 13 - Implemente as funcionalidades do menu
local: `tech_news/menu.py`

- Quando selecionada uma opção do menu, e inseridas as informações necessárias, a ação adequada deve ser realizada.

- Caso a opção `0` seja selecionada, a importação deve ser feita utilizando a função `get_tech_news`;

- Caso a opção `1` seja selecionada, a importação deve ser feita utilizando a função `search_by_title` e seu resultado deve ser impresso em tela;

- Caso a opção `2` seja selecionada, a exportação deve ser feita utilizando a função `search_by_date` e seu resultado deve ser impresso em tela;

- Caso a opção `3` seja selecionada, a importação deve ser feita utilizando a função `search_by_source` e seu resultado deve ser impresso em tela;

- Caso a opção `4` seja selecionada, a exportação deve ser feita utilizando a função `search_by_category` e seu resultado deve ser impresso em tela;

- Caso a opção `5` seja selecionada, a raspagem deve ser feita utilizando a função `top_5_news` e seu resultado deve ser impresso em tela;

- Caso a opção `6` seja selecionada, a raspagem deve ser feita utilizando a função `top_5_categories` e seu resultado deve ser impresso em tela;

- Caso a opção `7` seja selecionada, deve-se encerrar a execução do script e deve-se exibir a mensagem "Encerrando script";

- Caso alguma exceção seja lançada, a mesma deve ser capturada e sua mensagem deve ser exibida na saída padrão de erros (`stderr`).

✍️ Teste manual: dentro de um ambiente virtual onde seu projeto foi configurado, digite o comando `tech-news-analyzer`, assim você conseguirá interagir com o menu.



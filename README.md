# Analisando a cobertura da Mídia nas eleições de 2018

Uma das tarefas que costuma consumir o tempo de pesquisadores em mídia é a fase de coleta de dados. Depois de escolher um tópico e um recorte temporal, nem sempre é fácil extrair uma boa quantidade de reportagens de diferentes veículos. Essa coleção de _scripts_, com o apoio de uma interface web, pode ajudar a acelerar sensivelmente o processo.

O código foi criado por @BurgosNY e @bernardovianna, utilizando partes do software do [Impacto.jor](https://www.impacto.jor.br). Para dúvidas e sugestões, abra um issue.

Apesar de não exigir conhecimento em programação, é interessante que se saiba o básico de [Python](https://www.python.org/downloads/) para modificar o código. Usamos Python 3.5+.


## Obtendo os tokens de acesso

Crie um arquivo chamado .env e cole lá uma variável com o seu FACEBOOK_TOKEN e outra para o seu MEDIACLOUD_TOKEN. Para lê-lo, usamos o [django-environ](https://github.com/joke2k/django-environ) pela compatibilidade com Windows/Mac/Linux.


### Facebook
Usamos a API do Facebook para ter acesso aos dados de compartilhamento dos posts.

Para conseguir um token de acesso à API, crie um “app do Facebook” [neste site](https://developers.facebook.com/apps/), usando sua conta normal da rede social.

Após criá-lo (qualquer nome serve), vá no menu à esquerda, clique em Configurações > Básico, e copie tanto o seu “ID do Aplicativo” quanto a “Chave Secreta do Aplicativo”. O seu token será composto pelas duas coisas, com um **|** no meio. Algo assim:
2808639462424532|75f186bc5ad5347863443d375028e231


### Media Cloud
Para este script, usamos a API do [Media Cloud](https://mediacloud.org) para ler o feed e obter as URLs dos veículos selecionados. O banco de dados deles monitora centenas de sites no Brasil, boa parte com arquivo de dois anos ou mais. A chave é gratuita. Leia aqui os [limites para as requisições](https://mediacloud.org/support/query-guide) via API.

EXPLICAR COMO SELECIONAR OS MEDIA_IDS, falar dos selecionados


### Rodar o "criar .csv"

EXPLICAR o que ele faz, e por que pode demorar (limite de 200 req por hora do Facebook) -- o rodar python create_csv

### Rodando o programa

EXPLICAR BREVEMENTE COMO FUNCIONA A INTERFACE 


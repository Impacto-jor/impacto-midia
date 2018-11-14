# Analisando a cobertura da mídia nas eleições de 2018

## Obtendo os tokens de acesso

Crie um arquivo .env (usamos o [django-environ](https://github.com/joke2k/django-environ) pela compatibilidade com Windows/Mac/Linux) e adicione uma variável para o seu FACEBOOK_TOKEN e outra para o seu MEDIACLOUD_TOKEN.

```
FACEBOOK_TOKEN=XXXXXXXXXXXXXX
MEDIACLOUD_API=XXXXXXXXXXXXXX
```

### Facebook
Usamos a API do Facebook para ter acesso aos dados de compartilhamento dos posts.

Para conseguir um token de acesso à API, crie um “app do Facebook” [neste site](https://developers.facebook.com/apps/), usando sua conta normal da rede social.

Após criá-lo (qualquer nome serve), vá no menu à esquerda, clique em Configurações > Básico, e copie tanto o seu “ID do Aplicativo” quanto a “Chave Secreta do Aplicativo”. O seu token será composto pelas duas coisas, com um **|** no meio. Algo assim:
2808639462424532|75f186bc5ad5347863443d375028e231

### Media Cloud
Para este script, usamos a API do [Media Cloud](https://mediacloud.org) para ler o feed e obter as URLs dos veículos selecionados. O banco de dados deles monitora centenas de sites no Brasil, boa parte com arquivo de dois anos ou mais. A chave é gratuita. Leia aqui os [limites para as requisições](https://mediacloud.org/support/query-guide) via API. 

## Instalando dependências

Execute o comando para instalar as bibliotecas necessárias.

```
pip install -r requirements.txt
```

## Fazendo sua pesquisa inicial

Com seus tokens de acesso já adicionados ao arquivo .env, basta executar o arquivo create_csv.py para realizar sua pesquisa na base do Media Cloud e acrescentar os dados de reações e compartilhamentos do Facebook. 

```
python create_csv.py
```

O script vai pedir que você informe a data inicial e a data limite da pesquisa. Observe que a data limite não é incluída. Por exemplo, se você determinar o dia 27 de algum mês como data limite, o script retornará notícias publicadas até 23h59 do dia 26.

Escolhido o recorte temporal, o script vai pedir que você informe palavras-chave que serão buscadas nas notícias. Digite os termos separando-os com vírgulas. O programa não diferencia entre maiúsculas e minúsculas. Ex.: Haddad, bolsonaro, eleições.

A API do Facebook tem um limite de 200 requisições por hora. Por isso, o script faz uma pausa de uma hora após atingir esse limite. Se sua pesquisa for retornar um grande número de resultados, a coleta de informações do Facebook poderá demorar algumas horas.

O resultado final da pesquisa será salvo em um arquivo chamado "clipping.csv". O script também vai criar um arquivo chamado "clipping_tagged.csv", que será usado pelo web app que fará a visualização e a classificação das notícias.

## Visualizando e organizando sua pesquisa

O arquivo flask_dashboard.py é um web app que utiliza o framework [Flask](http://flask.pocoo.org/) para visualizar os resultados de sua pesquisa e organizá-los. 

```
export FLASK_APP=flask_dashboard.py && flask run
```

*Obs.: Se você estiver no Windows, substitua "export" por "set".*

Na tela inicial, você poderá ordenar os resultados da sua pesquisa por data ou por número de interações no Facebook e poderá filtrá-los de acordo com o veículo de publicação. A partir daí, é possível classificar cada notícia como positiva, negativa ou neutra ou criar suas próprias categorias de classificação. Na tabela, clique no respectivo botão para atribuir uma classificação a uma notícia.

As matérias que você classificar são reunidas em uma segunda tabela, onde você poderá revisar e organizar sua seleção e exportar o resultado final para uma arquivo .csv.
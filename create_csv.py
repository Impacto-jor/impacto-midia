from mediacloud_scripts import MediaCloud
from facebook_scripts import FacebookRequest
import time
import settings
import datetime as dt
import pandas as pd
import csv
from util import clean_story_url


def main(midia_filename='midia.csv', subject_list=['bolsonaro', 'haddad']):
    df = pd.read_csv(midia_filename)
    ids = df['mediacloud_id'].tolist()
    print('Criando csv com reportagens sobre tópicos específicos')
    ano_inicio = int(input('Escreva o ano de início das consulta. Ex.: 2018\n> '))
    mes_inicio = int(input('Escreva o mês de início das consulta. Ex.: 10\n> '))
    dia_inicio = int(input('Escreva o dia de início das consulta. Ex.: 23\n> '))
    ano_fim = int(input('Escreva o ano da data-limite das consulta. Ex.: 2018\n> '))
    mes_fim = int(input('Escreva o mês da data-limite das consulta. Ex.: 11\n> '))
    dia_fim = int(input('Escreva o dia da data-limite das consulta. Ex.: 3\n> '))
    raw_subject = input('Quais os termos de busca? Escreva apenas palavras únicas, separadas por vírgulas, sem aspas. Ex.: Haddad, Bolsonaro\n> ')
    subject_list = [x.strip().lower() for x in raw_subject.split(',') if x]
    start = dt.datetime(ano_inicio, mes_inicio, dia_inicio)
    end = dt.datetime(ano_fim, mes_fim, dia_fim)

    print('Buscando reportagens no MediaCloud. Isso talvez demore um pouquinho...')
    mc = MediaCloud(settings.MEDIACLOUD_API)
    stories = mc.get_story_list(ids, subject_list, start, end)
    print(stories[0].keys())

    print(f'Acrescentando informações do Facebook para {len(stories)}')
    fb = FacebookRequest(settings.FACEBOOK_TOKEN)
    for count, story in enumerate(stories, 1):
        story_url = clean_story_url(story['url'])
        info = fb.url_stats(story_url)
        for key in info.keys():
            story[key] = info[key]
        if count % 199 == 0:
            print('Limite da API do Facebook atingido. Script voltará a rodar em uma hora.')
            print(dt.datetime.now())
            time.sleep(3601)

    print('Exportando busca para csv.')
    df = pd.DataFrame(stories)
    df.set_index('stories_id', inplace=True)
    df['media_id'] = df['media_id'].astype(str)
    df['publish_date'] = pd.to_datetime(df.publish_date)
    df['publish_date'] = df['publish_date'].dt.strftime('%d/%m/%Y')
    df['tag'] = ''
    df.to_csv('clippingFOLHA.csv')
    with open('clipping_taggedFOLHA.csv', 'w', newline='') as csvfile:
        fieldnames = ['stories_id'] + list(df)
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
    print('Pronto!')

if __name__ == '__main__':
    main()
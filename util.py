import csv
import pandas as pd


def del_csv_row(csvfile, rowindex, indexcolumn):
    df = pd.read_csv(csvfile, index_col=indexcolumn)
    df.drop(rowindex, inplace=True)
    df.to_csv(csvfile)


def add_tagged_to_csv(newcsv, linedict):
    with open(newcsv, 'a', newline='') as csvfile:
        fieldnames = list(linedict.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(linedict)


def clean_story_url(story_url):
    #Limpa redirecionamento das URLs da Folha.
    #Pode ser amplido para corrigir problemas semelhantes em outros conjuntos de URLs.
    if story_url.startswith('https://redir'):
        clean_url = story_url.split('*')[-1]
        return clean_url
    else:
        return story_url


media_dict = {'38945':'Estadão',
              #'272170':'Zero Hora',
              '40252':'O Globo',
              '60427':'G1',
              '101882':'Exame',
              '59723':'Veja',
              '41736':'Folha de S. Paulo',
              '65509':'UOL',
              #'83356':'R7',
              '83498':'Istoé',
              #'102035':'Época',
              '83417':'Gazeta do Povo',
              '83399':'Valor',
              #'102526':'Jornal do Commercio',
              '83420':'O Povo'}
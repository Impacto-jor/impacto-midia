from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory
import settings
from util import *
import datetime

# Initialize app:
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

input_file = 'clipping_test.csv'
output_file = 'clipping_test_tagged.csv'
tags_list = ['Positivo', 'Negativo', 'Neutro']

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return redirect(url_for('dashboard', offset=0, limit=25, 
                            sortby='publish_date', order='desc',
                            media_filter='todos'))

@app.route('/dashboard/<int:offset>/<int:limit>/<sortby>/<order>/<media_filter>', methods=['GET', 'POST'])
def dashboard(offset, limit, sortby, order, media_filter):
    data_source = open(input_file, encoding="utf8", newline='')
    df = pd.read_csv(input_file)
    df = df.fillna('')
    df['media_id'] = df['media_id'].astype(str)
    if order == 'desc':
        df = df.sort_values(by=[f'{sortby}'], ascending=False)
    elif order == 'asc':
        df = df.sort_values(by=[f'{sortby}'], ascending=True)
    if media_filter == 'todos':
        pass
    else:
        df = df.loc[df['media_id'] == media_filter]
    data = df.to_dict('records')
    total_records = len(data)
    first_row = offset
    last_row = limit + offset
    next_url = '/dashboard/' + str(offset + limit) + '/' + str(limit) + f'/{sortby}/{order}/{media_filter}'
    prev_url = '/dashboard/' + str(offset - limit) + '/' + str(limit) + f'/{sortby}/{order}/{media_filter}'
    if request.method == 'POST':
        global tags_list
        custom_tags = request.form.get('tags_list')
        clear_list = request.form.get('clear_list')
        if custom_tags:
          tags_list = custom_tags.split(',')
        if clear_list:
          tags_list = ['Positivo', 'Negativo', 'Neutro']
          #redirect(url_for('dashboard', offset=offset, limit=limit, sortby=sortby, order=order, media_filter=media_filter, tags_list=tags_list))
        response = request.form.getlist('tags')
        if response:
            stories_id = response[0].split(',')[0]
            tag = response[0].split(',')[1]
            line = df.loc[df['stories_id'] == int(stories_id)]
            line['tag'] = tag
            linedict = line.to_dict('records')[0]
            add_tagged_to_csv(output_file, linedict)
            flash(f'A matéria foi adicionada à tabela de impacto.')
            del_csv_row(input_file, linedict['stories_id'], 'stories_id')
        return redirect(url_for('dashboard', offset=offset, limit=limit, sortby=sortby, order=order, media_filter=media_filter, tags_list=tags_list))
    return render_template('dashboard.html', 
                           data=data, 
                           media_dict=media_dict,
                           tags_list=tags_list, 
                           offset=offset,
                           limit=limit,
                           first_row=first_row,
                           last_row=last_row,
                           next_url=next_url,
                           prev_url=prev_url,
                           sortby=sortby,
                           order=order,
                           media_filter=media_filter,
                           total_records=total_records)

@app.route('/impact_table/<int:offset>/<int:limit>/<sortby>/<order>/<media_filter>/<impact>', methods=['GET', 'POST'])
def impact_table(offset, limit, sortby, order, media_filter, impact):
    data_source = open(output_file, encoding="utf8", newline='')
    df = pd.read_csv(output_file)
    df = df.fillna('')    
    df['media_id'] = df['media_id'].astype(str)
    if order == 'desc':
        df = df.sort_values(by=[f'{sortby}'], ascending=False)
    elif order == 'asc':
        df = df.sort_values(by=[f'{sortby}'], ascending=True)
    if media_filter == 'todos':
        pass
    else:
        df = df.loc[df['media_id'] == media_filter]
    if impact == 'todos':
        pass
    else:
        df = df.loc[df['tag'] == impact.capitalize()]        
    data = df.to_dict('records')
    total_records = len(data)
    first_row = offset
    last_row = limit + offset
    next_url = '/impact_table/' + str(offset + limit) + '/' + str(limit) + f'/{sortby}/{order}/{media_filter}/{impact}'
    prev_url = '/impact_table/' + str(offset - limit) + '/' + str(limit) + f'/{sortby}/{order}/{media_filter}/{impact}'
    if request.method == 'POST':
        stories_id = request.values.get('send_back')
        export_csv = request.values.get('export_csv')
        if stories_id:
            df = df.drop('tag', 1)
            line = df.loc[df['stories_id'] == int(stories_id)]
            linedict = line.to_dict('records')[0]
            add_tagged_to_csv(input_file, linedict)
            del_csv_row(output_file, linedict['stories_id'], 'stories_id')
            return redirect(url_for('impact_table', offset=offset, limit=limit, sortby=sortby, order=order, media_filter=media_filter, impact=impact))
        if export_csv:
            df['media_id'] = df['media_id'].map(media_dict)
            df.to_csv('OUTPUT.csv', encoding='utf-8', index=False)
            return send_from_directory('./', 'OUTPUT.csv', as_attachment=True)
    tags_list = set([tag for tag in df.tag])
    return render_template('impact_table.html', 
                           data=data, 
                           media_dict=media_dict, 
                           tags_list=tags_list,
                           offset=offset,
                           limit=limit,
                           first_row=first_row,
                           last_row=last_row,
                           next_url=next_url,
                           prev_url=prev_url,
                           sortby=sortby,
                           order=order,
                           media_filter=media_filter,
                           impact=impact,
                           total_records=total_records)

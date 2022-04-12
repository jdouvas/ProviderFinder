#-----------------------------------------------------------------------
# app.py
# Author: Julia Douvas
# Description:
#-----------------------------------------------------------------------

from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session
from db_basic import search
import logging
#-----------------------------------------------------------------------

app = Flask(__name__)

#-----------------------------------------------------------------------


# def real_home_page():

#     html = render_template('homepage.html')
#     response = make_response(html)
#     return response

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/homepage', methods=['GET'])
def home_page():

    # html = render_template('search.html')
    html = render_template('homepage.html')
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search_results():

    student_health = False

    if request.args.get('name') is not None:
        name = request.args.get('name')
    else:
        name = ''
    if request.args.get('titles') is not None:
        titles = request.args.get('titles')
    else:
        titles = ''
    if request.args.get('insurance') is not None:
        insurance = request.args.get('insurance')
        if (insurance == 'Princeton Student Health Plan'):
            student_health = True
    else:
        insurance = ''
    if request.args.get('telehealth') is not None:
        telehealth = request.args.get('telehealth')
    else:
        telehealth = ''
    if request.args.get('payby') is not None:
        payby = request.args.get('payby')
    else:
        payby = ''
    if request.args.get('specialties') is not None:
        specialties = request.args.get('specialties')
    else:
        specialties = ''
    if request.args.get('allied') is not None:
        allied = request.args.get('allied')
    else:
        allied = ''
    if request.args.get('therapies') is not None:
        therapies = request.args.get('therapies')
    else:
        therapies = ''
    if request.args.get('degrees') is not None:
        degrees = request.args.get('degrees')
    else:
        degrees = ''
    if request.args.get('walkable') is not None:
        walkable = request.args.get('walkable')
    else:
        walkable = ''

    search_dict = {'name': name,
                   'insurance': insurance, 'payby': payby,
                   'specialties': specialties, 'allied': allied,
                   'therapies': therapies, 'titles': titles,
                   'telehealth': telehealth, 'degrees': degrees,
                   'walkable': walkable} 

    # pass dict into db_basic.py
    search_results = search(search_dict, student_health)
    if 'data' in search_results:
        # search_results will be a list of lists
        search_results = search_results.get('data')
    
    # create html table
    html = '''
    <table class="table table-striped">
        <tr>
        <th align="left">Name</th>
        <th align="left">Phone Number</th>
        </tr>'''
    count = 0
    for line in search_results:
        count += 1
        html += ('<tr><td><a target="_blank" href='+ str(line[1]) + '>' + str(line[0]) + '</a></td>')
        html += '<td>' + str(line[2]) + '</td></tr>'
    html += '</table>'

    print(count)
    response = make_response(html)
    return response


#-----------------------------------------------------------------------

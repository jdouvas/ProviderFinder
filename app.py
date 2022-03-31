#-----------------------------------------------------------------------
# app.py
# Author: Julia Douvas
#-----------------------------------------------------------------------

from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session
from db_basic import search
#-----------------------------------------------------------------------

app = Flask(__name__)

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/homepage', methods=['GET'])
def home_page():

    error_msg = request.args.get('error_msg')
    if error_msg is None:
        error_msg = ''

    html = render_template('home_page.html', error_msg=error_msg)
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search_results():

    provider = request.args.get('provider_name')
    # if (provider is None) or (provider.strip() == ''):
    #     error_msg = 'Please type a valid provider name.'
    #     return redirect(url_for('home_page', error_msg=error_msg))

    providers = search(provider) # needs to call database
    if providers is None:
        providers = []

    html = render_template('search_results.html', prov_list=providers)
    response = make_response(html)
    return response


#-----------------------------------------------------------------------

@app.route('/costforprovider', methods=['GET'])
def cost_estimation():
    
    html = render_template('cost_ques.html')
    response = make_response(html)
    return response

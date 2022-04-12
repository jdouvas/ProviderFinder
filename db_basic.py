#-----------------------------------------------------------------------
# db_basic.py
# Author: Julia Douvas
# Description: functions for querying the PostgreSQL Database
#-----------------------------------------------------------------------

import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

# main search function
def search(search_dict, student_health):
    conn = psycopg2.connect(
        host=os.environ.get("COS398_HOST"),
        database=os.environ.get("COS398_DATABASE"),
        user=os.environ.get('COS398_USER'),
        password=os.environ.get('COS398_PASSWORD'))
    
    cur = conn.cursor()
    params = {}

    aliases = ["Princeton Student Health Plan", "Princeton University EPN",
                "Princeton University Health Plan","Princeton University Student Insurance (Aetna)", 
                "Princeton U and PTS Healthplan",'Princeton University Student H',
                'Princeton U student insurance','Princeton University Mental Health EPN',
                'Princeton U. Student Health','PU Student Health Plan',
                'Princeton University Aetna Student Health Plan','Princeton Univ. Student Health',
                'Princeton Student Health Plan','Princeton University Student Health Plan',
                'Princeton Aetna Student Health','Princeton Healthcare EAP',
                'Student Health Plan','Princeton University SHP',
                'Aetna Student Health (Princeton)','Aetna for Princeton University Health Plan',
                'Aetna for Princeton University Student Insurance','Aetna Student Health (Princeton University)',
                'Aetna SHP (Princeton)','Aetna Student Health Plan',
                'Aetna Student Health-Princeton','Aetna Student Health',
                'Aetna Princeton University Student Health Plan','Aetna Student Health - Princeton Univ',
                'I am an EPN provider for PU','SHP (Princeton University)',
                'Students with Aetna','Princeton University Student Health as of 9/1/17']

    # initialize aliases for the Princeton Health Plan
    alias1 = "Princeton University EPN"
    alias1 = '%'+alias1+'%'
    params['alias1'] = alias1
    alias2 = "Princeton University Health Plan"
    alias2 = '%'+alias2+'%'
    params['alias2'] = alias2
    alias3 = "Princeton University Student Insurance (Aetna)"
    alias3 = '%'+alias3+'%'
    params['alias3'] = alias3
    alias4 = "Princeton U and PTS Healthplan"
    alias4 = '%'+alias4+'%'
    params['alias4'] = alias4
    alias5 = 'Princeton University Student H'
    alias5 = '%'+alias5+'%'
    params['alias5'] = alias5
    alias6 = 'Princeton U student insurance'
    alias6 = '%'+alias6+'%'
    params['alias6'] = alias6
    alias7 = 'Princeton University Mental Health EPN'
    alias7 = '%'+alias7+'%'
    params['alias7'] = alias7
    alias8 = 'Princeton U. Student Health'
    alias8 = '%'+alias8+'%'
    params['alias8'] = alias8
    alias9 = 'PU Student Health Plan'
    alias9 = '%'+alias9+'%'
    params['alias9'] = alias9
    alias10 = 'Princeton University Aetna Student Health Plan'
    alias10 = '%'+alias10+'%'
    params['alias10'] = alias10
    alias11 = 'Princeton Univ. Student Health'
    alias11 = '%'+alias11+'%'
    params['alias11'] = alias11
    alias12 = 'Princeton Student Health Plan'
    alias12 = '%'+alias12+'%'
    params['alias12'] = alias12
    alias13 = 'Princeton University Student Health Plan'
    alias13 = '%'+alias13+'%'
    params['alias13'] = alias13
    alias14 = 'Princeton Aetna Student Health'
    alias14 = '%'+alias14+'%'
    params['alias14'] = alias14
    alias15 = 'Student Health Plan'
    alias15 = '%'+alias15+'%'
    params['alias15'] = alias15
    alias16 = 'Princeton University SHP'
    alias16 = '%'+alias16+'%'
    params['alias16'] = alias16
    alias17 = 'Aetna Student Health (Princeton)'
    alias17 = '%'+alias17+'%'
    params['alias17'] = alias17
    alias18 = 'Aetna for Princeton University Health Plan'
    alias18 = '%'+alias18+'%'
    params['alias18'] = alias18
    alias19 = 'Aetna for Princeton University Student Insurance'
    alias19 = '%'+alias19+'%'
    params['alias19'] = alias19
    alias20 = 'Aetna Student Health (Princeton University)'
    alias20 = '%'+alias20+'%'
    params['alias20'] = alias20
    alias21 = 'Aetna SHP (Princeton)'
    alias21 = '%'+alias21+'%'
    params['alias21'] = alias21
    alias22 = 'Aetna Student Health Plan'
    alias22 = '%'+alias22+'%'
    params['alias22'] = alias22
    alias23 = 'Aetna Student Health-Princeton'
    alias23 = '%'+alias23+'%'
    params['alias23'] = alias23
    alias24 = 'Aetna Student Health'
    alias24 = '%'+alias24+'%'
    params['alias24'] = alias24
    alias25 = 'Aetna Princeton University Student Health Plan'
    alias25 = '%'+alias25+'%'
    params['alias25'] = alias25
    alias26 = 'Aetna Student Health - Princeton Univ'
    alias26 = '%'+alias26+'%'
    params['alias26'] = alias26
    alias27 = 'I am an EPN provider for PU'
    alias27 = '%'+alias27+'%'
    params['alias27'] = alias27
    alias28 = 'SHP (Princeton University)'
    alias28 = '%'+alias28+'%'
    params['alias28'] = alias28
    alias29 = 'Students with Aetna'
    alias29 = '%'+alias29+'%'
    params['alias29'] = alias29
    alias30 = 'Princeton University Student Health as of 9/1/17'
    alias30 = '%'+alias30+'%'
    params['alias30'] = alias30



    name = str(search_dict['name'])
    name = '%'+name+'%'
    params['name'] = name

    telehealth = str(search_dict['telehealth'])
    telehealth = '%'+telehealth+'%'
    params['telehealth'] = telehealth

    walkable = str(search_dict['walkable'])
    walkable = '%'+walkable+'%'
    params['walkable'] = walkable

    insurance = str(search_dict['insurance'])
    insurance = '%'+insurance+'%'
    params['insurance'] = insurance

    payby = str(search_dict['payby'])
    payby = '%'+payby+'%'
    params['payby'] = payby

    specialties = str(search_dict['specialties'])
    specialties = '%'+specialties+'%'
    params['specialties'] = specialties

    allied = str(search_dict['allied'])
    allied = '%'+allied+'%'
    params['allied'] = allied

    therapies = str(search_dict['therapies'])
    therapies = '%'+therapies+'%'
    params['therapies'] = therapies

    titles = str(search_dict['titles'])
    titles = '%'+titles+'%'
    params['titles'] = titles

    degrees = str(search_dict['degrees'])
    degrees = '%'+degrees+'%'
    params['degrees'] = degrees

    sqlstring = 'SELECT name, url, phone_number FROM providers'
    b_name = False
    b_telehealth = False
    b_walkable = False
    b_insurances = False
    b_payby = False
    b_specialties = False
    b_allied = False
    b_therapies = False
    b_titles = False
    b_degrees = False

    if ((name != '%%') or (telehealth != '%%') or (insurance != '%%') or (payby != '%%') or (specialties != '%%') or (allied != '%%') or (therapies != '%%') or (titles != '%%') or (degrees != '%%') or (walkable != '%%')):
        sqlstring += ' WHERE'

    
    if name != '%%':
        b_name = True
        sqlstring += ' LOWER(providers.name) LIKE LOWER(%(name)s)'
    if telehealth != '%%':
        b_telehealth = True
        if b_name is True:
            sqlstring += ' AND'
        sqlstring += ' LOWER(providers.telehealth_option) LIKE LOWER(%(telehealth)s)'
    if payby != '%%':
        b_payby = True
        if b_name is True or b_telehealth is True:
            sqlstring += ' AND'
        sqlstring += ' array_to_string(providers.pay_by, \',\') LIKE %(payby)s'
    if specialties != '%%':
        b_specialties = True
        if b_name is True or b_telehealth is True or b_payby is True:
            sqlstring += ' AND'
        sqlstring += ' array_to_string(providers.specialties_issues, \',\') LIKE %(specialties)s'
    if allied != '%%':
        b_allied = True
        if b_name is True or b_telehealth is True or b_payby is True or b_specialties is True:
            sqlstring += ' AND'
        sqlstring += ' array_to_string(providers.sexuality, \',\') LIKE %(allied)s'
    if therapies != '%%':
        b_therapies = True
        if b_name is True or b_telehealth is True or b_payby is True or b_specialties is True or b_allied is True:
            sqlstring += ' AND'
        sqlstring += ' array_to_string(providers.therapies_offered, \',\') LIKE %(therapies)s'
    if titles != '%%':
        b_titles = True
        if b_name is True or b_telehealth is True or b_payby is True or b_specialties is True or b_allied is True or b_therapies is True:
            sqlstring += ' AND'
        sqlstring += ' array_to_string(providers.titles, \',\') LIKE %(titles)s'
    if degrees != '%%':
        b_degrees = True
        if b_name is True or b_telehealth is True or b_payby is True or b_specialties is True or b_allied is True or b_therapies is True or b_titles is True:
            sqlstring += ' AND'
        sqlstring += ' array_to_string(providers.titles, \',\') LIKE %(degrees)s'
    if insurance != '%%':
        b_insurances = True
        if b_name is True or b_telehealth is True or b_payby is True or b_specialties is True or b_allied is True or b_therapies is True or b_titles is True or b_degrees is True:
            sqlstring += ' AND'
        if (student_health):
            sqlstring += ' (array_to_string(providers.insurances, \',\') LIKE %(insurance)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias1)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias2)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias3)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias4)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias5)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias6)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias7)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias8)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias9)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias10)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias11)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias12)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias13)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias14)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias15)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias16)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias17)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias18)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias19)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias20)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias21)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias22)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias23)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias24)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias25)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias26)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias27)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias28)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias29)s OR \
                            array_to_string(providers.insurances, \',\') LIKE %(alias30)s)'
        else:
            sqlstring += ' (array_to_string(providers.insurances, \',\') LIKE %(insurance)s)'
    if walkable != '%%':
        b_walkable = True
        if b_name is True or b_telehealth is True or b_payby is True or b_specialties is True or b_allied is True or b_therapies is True or b_titles is True or b_insurances is True:
            sqlstring += ' AND'
        sqlstring += ' LOWER(providers.walkable) LIKE LOWER(%(walkable)s)'
    

    sqlstring += ' ORDER BY providers.name;'
    cur.execute(sqlstring, params)
    results = cur.fetchall()
    conn.commit()
    return results


#-----------------------------------------------------------------------
# db_basic.py
# functions for querying the PostgreSQL Database
#-----------------------------------------------------------------------

import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

# main search function
def search(prov_name):
    conn = psycopg2.connect(
        host=os.environ.get("COS398_HOST"),
        database=os.environ.get("COS398_DATABASE"),
        user=os.environ.get('COS398_USER'),
        password=os.environ.get('COS398_PASSWORD'))
    
    cur = conn.cursor()
    prov = '%'+prov_name+'%'
    # cur.execute('SELECT * FROM profs;')
    cur.execute('SELECT name, url FROM providers WHERE LOWER(providers.name) LIKE LOWER(%(provider_name)s);', {'provider_name': prov})
    providers = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return providers

# get prof info for prof page
# def prof_info(prof_name):
#     conn = psycopg2.connect()
    
#     cur = conn.cursor()
#     prof = '%'+prof_name+'%'
#     output = cur.execute('SELECT name, title FROM profs WHERE LOWER(profs.name) LIKE LOWER(%(profname)s);', {'profname': prof})
#     profs = cur.fetchall()

#     conn.commit()
#     cur.close()
#     conn.close()
#     return profs
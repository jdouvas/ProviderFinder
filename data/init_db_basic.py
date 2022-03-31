#-----------------------------------------------------------------------
# init_db_basic.py
# NOT WORKING!!!!! (just did it manually on pgAdmin4)
#-----------------------------------------------------------------------

import os
import json
import psycopg2
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
        conn = psycopg2.connect(
                host=os.environ.get("COS398_HOST"),
                database=os.environ.get("COS398_DATABASE"),
                user=os.environ.get('COS398_USER'),
                password=os.environ.get('COS398_PASSWORD'))

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a command: create our database tables
        cur.execute('DROP TABLE IF EXISTS providers;')
        cur.execute('CREATE TABLE providers (name varchar PRIMARY KEY,'
                                            'id integer UNIQUE,'
                                            'url varchar);'
                                            )
        cur.execute('COPY providers(name, id, url) FROM \'ids.csv\' DELIMITER \',\' CSV HEADER;')

        # with open('ids.json') as f:
        #     providers = json.load(f)
        
        # for prov in providers:
        #         cur.execute("""
        #                 INSERT INTO providers (name, id, url)
        #                 VALUES (%(name)s, %(id)s, %(url)s)
        #                 """,
        #                 prov)

        conn.commit()

        cur.execute("SELECT * FROM providers")
        print(cur.fetchone())

        cur.close()
        conn.close()
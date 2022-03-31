#!/usr/bin/env/ python

#-------------------------------------------------
# query.py
# Authors: Julia Douvas
#-------------------------------------------------

from sys import argv, stderr
from contextlib import closing
from sqlite3 import connect

#-------------------------------------------------

DATABASE_URL = 'file:providers.sql?mode=rw'

def select(args):
    try:
        with connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:

                cursor.execute('BEGIN')
                # create SQL statement
                # sqlstring = "SELECT ... WHERE"

                # get data from SQL database
                # sqlstring += " ORDER BY "
                output = cursor.execute(sqlstring, tuple(params))
                # get data from tuples
                data = []
                for row in output:
                    data.append(row)

                cursor.execute('COMMIT')
                return {'data': data}
    
    except Exception as ex:
        print(argv[0] + ': ' + str(ex), file=stderr)
        return {'error': 'A server error occurred. Please contact the system administrator.'}

def details(provider_name):
    try:
        # # connect to database
        # with connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
        #     with closing(connection.cursor()) as cursor:
        #         cursor.execute('BEGIN')
        #         # create SQL statement
        #         # sqlstring = "SELECT ... WHERE "
        #         # output
        #         output = cursor.execute(sqlstring, (provider_name, ))
        #         # check if empty result set
        #         check = cursor.fetchone()
        #         if check is None:
        #             print(argv[0] + ": no provider " + provider_name + " exists")
        #             return {'error': ": no provider " + provider_name + " exists"}
        #         cursor.execute(sqlstring, (provider_name, ))
        #         return_data = {}
        #         depts = []
        #         for row in output:
        #             return_data['areas'] = str(row[0])


    # Catch exceptions
    except Exception as ex:
        print(argv[0] + ': ' + str(ex), file=stderr)
        return {'error': 'A server error occurred. Please contact the system administrator.'}
from database.database import Database

import tkFileDialog as fd
import pandas as pd
import csv

gdp_csv = fd.askopenfilename(title='Choose historical GDP csv file')
gdp_db_file = fd.asksaveasfilename(title='Choose a db name for GDP database')


def csv_to_db(): 
    df = pd.read_csv(gdp_csv, header=1, index_col=0).fillna(-1)

    gdp_db = Database(gdp_db_file)
    gdp_tb = gdp_db.create_table('gdp', 'country TEXT, gdp REAL, year INT')

    gdp_db.cursor.execute('BEGIN')

    for column, country in enumerate(df): 
        print '{} out of {} countries'.format(column + 1, len(df.columns))
        for row, gdp in enumerate(df[country]): 
            print country, gdp, df.index[row]

            gdp_db.insert('INSERT INTO {tb} VALUES(?, ?, ?)'.format(tb=gdp_tb), [country, float(gdp), int(df.index[row])])            

    gdp_db.connection.commit()
    gdp_db.connection.close()

csv_to_db()
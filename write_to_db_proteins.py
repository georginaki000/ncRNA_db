import pandas as pd
import sqlalchemy

DB_USER = "diamantop"
DB_PASSWORD = "12345678"
DB_HOSTNAME = "pez.insybio.com"
DB_PORT = "3306"
DB_NAME = "diamantop_ncrnas"
DB_TABLE = "proteins"

# read data into pandas dataframe
df = pd.read_csv("proteins_final.csv", sep=';', header=0)
df['status'] = 'reviewed'
# delete empty columns
df.dropna('columns', 'all', inplace=True)
df.drop('Sequence', 'columns', inplace=True)

print(df.columns)

df.to_csv("proteins_to_db.csv", sep='\t', na_rep='NULL', index=False)
# exit()
# input()

# # connet to mySQL db
# engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}')


# df.to_sql(DB_TABLE, engine, if_exists='append', index=False, chunksize=50)


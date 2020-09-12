import psycopg2 as pg2
from getpass import getpass

if __name__ == "__main__":

    conn = psycopg2.connect(dbname='fraud_data',
                            user='postgres',
                            password = getpass(),
                            host='52.15.236.214')
    c = conn.cursor()

    conn.commit()
    conn.close()

# # open connection and create database
# database='realty-db'
# try:
#     with pg2.connect(user='postgres', password=getpass.getpass(), host='localhost', port='5435') as conn:
#         with conn.cursor() as curs:
#             conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#             curs.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
# finally:
#     conn.close()

# # switch to from sqlalchemy import create_engine
# engine = sqlalchemy.create_engine('postgresql://postgres:password@localhost:5435/realty-db', echo=True)
# #connection = engine.raw_connection()
# population.to_sql('population', engine)
# conn.close()

# # another way
# c.execute(

#     # Connecting to the database
# conn = connect(param_dic)
# # Inserting each row
# for i in dataframe.index:
#     query = """
#     INSERT into emissions(column1, column2, column3) values('%s',%s,%s);
#     """ % (dataframe['column1'], dataframe['column2'], dataframe['column3'])
#     single_insert(conn, query)
# # Close the connection
# conn.close()

# # Create a DataFrame
# dataFrame   = pds.DataFrame(studentScores,

#               index=(1211,1212,1213), # Student ids as index

#               columns=("Physics", "Chemistry", "Biology", "Mathematics", "Language")

#               );
# alchemyEngine           = create_engine('postgresql+psycopg2://test:test@127.0.0.1/test', pool_recycle=3600);
# postgreSQLConnection    = alchemyEngine.connect();
# postgreSQLTable         = "StudentScores";

# try:
#     frame           = dataFrame.to_sql(postgreSQLTable, postgreSQLConnection, if_exists='fail');
# except ValueError as vx:
#     print(vx)
# except Exception as ex:  
#     print(ex)
# else:
#     print("PostgreSQL Table %s has been created successfully."%postgreSQLTable);
# finally:
#     postgreSQLConnection.close();

# # now we can connect to the database specifically
# sqlGetTableList = '''\d                    '''
# sqlCreateTable = "create table "+name_Table+" (id bigint, title varchar(128), summary varchar(256), story text);"

# try:
#     with pg2.connect(database="realty-db", user="postgres", password='password', host="localhost", port="5435") as conn:
#         with conn.cursor() as curs:
#             # df.to_sql('my_table', con, if_exists='append')
#             curs.execute(sqlCreateTable)
#             tables = curs.fetchall()
# finally:
#     conn.close()

    # or with sqlalchemy
try:
    with create_engine('postgresql://scott:tiger@localhost:5432/mydatabase') as engine:
        df.to_sql('table_name', engine, if_exists='replace',index=False)
finally:
    conn.close()

# conn = engine.raw_connection()
# cur = conn.cursor()
# output = io.StringIO()
# df.to_csv(output, sep='\t', header=False, index=False)
# output.seek(0)
# contents = output.getvalue()
# cur.copy_from(output, 'table_name', null="") # null values become ''
# conn.commit()


###### PULLING DATA

table_df = pd.read_sql_table(
    table_name,
    con=engine
)

sql_df = pd.read_sql(
    "SELECT * FROM nyc_jobs",
    con=engine,
    parse_dates=[
        'created_at',
        'updated_at'
    ]
)
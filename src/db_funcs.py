import psycopg2
from getpass import getpass

if __name__ == "__main__":

    conn = psycopg2.connect(dbname='fraud_data',
                            user='postgres',
                            password = getpass(),
                            host='52.15.236.214')
    c = conn.cursor()

    conn.commit()
    conn.close()
import sqlalchemy
from sqlalchemy import text
import db_setup
from sqlalchemy import create_engine





def execute_query(query:str,conn):

    resp=conn.execute(text(query))
    rows=resp.fetchall()
    print(rows)






if __name__=="__main__":

    try:
        result=db_setup.set_connection()
        

        query="select * from companydata;"
        with result.connect() as conn:
            execute_query(query,conn)
    except Exception as e:
        print(f"something went wrong {str(e)}")


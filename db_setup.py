import sqlalchemy
from sqlalchemy import create_engine
user="root"
password="user123"
host="127.0.0.1"
port=3306
db="structurerag"

def set_connection():
    return create_engine(url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, db))


if __name__=="__main__":

    try:
        result=set_connection()
        print("done")
    except Exception as e:
        print(f"something went wrong {str(e)}")


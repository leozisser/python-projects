from sqlalchemy import create_engine
from sqlalchemy import text
def query():
    sqlquery = text("insert into `masa_table` (`name`,`age`,`sex`) values ('leo', 30, 1);")
    engine = create_engine("mysql+pymysql://root:root@192.168.1.51/masa_db")
    result = engine.execute(sqlquery)
    return [row for row in result]
    # for row in result:
    #    print(
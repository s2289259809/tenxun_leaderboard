import pymysql
class SqlHelper(object):
    def __init__(self):
        self.connect()

    def connect(self):
        self.db = pymysql.connect(host='139.155.75.65', user='root', password='rootvgmysql', database='zeng',charset='utf8')
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self,sql,args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return  result

    def get_one(self,sql,args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self,sql,args):
        self.cursor.execute(sql,args)
        self.db.commit()

    def create(self,sql,args):
        self.cursor.execute(sql, args)
        self.db.commit()
        return self.cursor.lastrowid

    def multiple_modify(self,sql,args):
        self.cursor.executemany(sql,args)
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()
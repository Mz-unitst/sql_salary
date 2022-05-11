import pymysql


class User:
    def __init__(self):
        try:
            self.db = pymysql.connect(
                host='',
                user='',
                password='',
                database='salary',connect_timeout=30)
            # cursor是一个对象，执行的命令时execute, 返回的结果存于fetchone
            self.cursor = self.db.cursor()
            # self.show_processlist()
            # self.cursor.execute('show processlist')
            # ipp=self.cursor.fetchone()
            # print('success,ip:port=', ipp[2])
        except BaseException:
            print("connect fail")

    def show_processlist(self):
        try:
            self.cursor.execute('show processlist;')
            res=self.cursor.fetchall()
            for i in res:
                print(i)
        except BaseException:
            print('show processlist执行失败')
            self.db.rollback()

    def get_dep(self):
        try:
            self.cursor.execute('select dname from department;')
            self.db.commit()
            res = self.cursor.fetchall()
            return res

        except BaseException:
            print('执行失败')
            self.db.rollback()

    def select_bsalary(self, dname='navi'):
        try:
            self.cursor.execute(
                "SELECT sno,sname,dno,dname,bsalary FROM salary.staff_info  where dname='%s' limit 10;" % (dname))
            self.db.commit()
            # res = self.cursor.fetchone()
            maxx = self.cursor.rowcount
            res = self.cursor.fetchall()
            return res
        except BaseException:
            print('执行失败')
            self.db.rollback()

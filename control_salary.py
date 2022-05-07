from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from salary import Ui_salary_window
from connectdb import User


class salary_table(QMainWindow, Ui_salary_window):
    def __init__(self, parent=None):
        super(salary_table, self).__init__(parent)
        self.affected_rows_index = []
        self.currow = 0
        self.setupUi(self)
        self.modell = QStandardItemModel(20, 8)
        # self.user = User()
        self.modell.setHorizontalHeaderLabels(
            ['员工号', '姓名', '部门', '基本薪水', '总奖金', '总罚款', '总工资', '时间'])
        self.salarytable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.salarytable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.salarytable.setModel(self.modell)
        self.init_salary_table()

    def init_salary_table(self):
        try:
            self.user = User()
            # ['员工号', '姓名', '部门', '时间','薪水']
            self.clear_sum()
            self.update_sumfine()
            self.update_sumbonous()
            self.update_sumsalary()

            self.user.cursor.execute(
                'select sno,sname,dname,bsalary,sumbonous,sumfine,sumsalary,date from salary order by sno,date limit 20')
            self.user.db.commit()
            res = self.user.cursor.fetchall()
            # print('salary:',res)
            cur_row_index = 0
            for cur in res:
                for i in range(8):
                    item = QStandardItem(str(cur[i]))
                    self.modell.setItem(cur_row_index, i, item)
                cur_row_index = cur_row_index + 1
        except BaseException:
            self.user.db.rollback()
            print("表赋值失败")

        self.user.cursor.close()
        self.user.db.close()

    def update_sumbonous(self):
        try:
            self.user.cursor.execute('select sno,bonous,date,dno,dname,sname from bonous') #获取fine表信息
            res=self.user.cursor.fetchall()
            for i in res:

                # print('bonous',i)
                sno = int(i[0])
                bonous = float(i[1])
                tmp = str(i[2])
                y = int(tmp.split('-')[0])
                m = int(tmp.split('-')[1])
                if (m == 12):
                    m = 1
                    y = y + 1
                else:
                    m = m + 1
                date = str(y) + '-' + str(m) + '-01' # date是salary中对应的date
                # print(i[3])
                dno=int(i[3])
                dname=i[4]
                sname=i[5]

                # print(date)
                sql_get_bsalary='select  bsalary from staff_info where sno=%d;'%(sno)
                self.user.cursor.execute(sql_get_bsalary)
                bsalary=self.user.cursor.fetchone()[0]
                # print(bsalary)
                sql_if_null='select * from salary where sno=%d and date=str_to_date("%s","%%Y-%%m-%%d");'%(sno,date)
                # print('if null: ',self.user.cursor.mogrify(sql_if_null))
                self.user.cursor.execute(sql_if_null)
                res_if_null=self.user.cursor.fetchall()
                # print('res_if_null',res_if_null)
                # print(len(res_if_null))

                sql_insert_bonous='insert ignore into salary (sno, sname, dno, dname, date, bsalary, sumbonous, sumfine, sumsalary) VALUES (%d,"%s",%d,"%s",str_to_date("%s","%%Y-%%m-%%d"),%f,0,0,0);'
                # sql_insert_fine='insert ignore into salary set sno=%d,date=str_to_date("%s","%%Y-%%m-%%d"),bsalary=0,dno=%d,dname="%s",sname="%s";'%(sno,date,dno,dname,sname)
                sql_update_bonous='update ignore salary set sumbonous=salary.sumbonous+%f where sno=%d and  date=str_to_date("%s","%%Y-%%m-%%d");'%(bonous,sno,date)
                # print(sql_insert_fine%(sno,sname,dno,dname, date,9 ))
                # print(self.user.cursor.mogrify(sql_insert_fine%(sno,sname,dno,dname, date,bsalary )))
                # t=self.user.cursor.mogrify(sql_update_fine)

                if len(res_if_null) == 0:
                    # print('insert salary: ')
                    # print(sql_insert_fine % (sno, sname, dno, dname, date, bsalary))
                    self.user.cursor.execute(
                        sql_insert_bonous % (sno, sname, dno, dname, date, bsalary))  # 当时间冲突 有重复时会卡死。 update直接卡死，每个函数都没问题啊。
                    # res_insert=self.user.cursor.fetchall()
                    # print('res_insert',res_insert)
                    self.user.db.commit()
                # print('update fine:', t)
                # print('update: ',self.user.cursor.mogrify(sql_update_fine))
                self.user.cursor.execute(sql_update_bonous)
                # res_update=self.user.cursor.fetchall()
                # print('res_update',res_update)
                # print('-'*80)
                self.user.db.commit()
            print('success update sumbonous')
        except:
            print('update sumbonous failed')
            self.user.db.rollback()

    def update_sumfine(self):
        try:
            self.user.cursor.execute('select sno,fine,date,dno,dname,sname from fine') #获取fine表信息
            res=self.user.cursor.fetchall()
            for i in res:

                # print('fine:',i)
                sno = int(i[0])
                fine = float(i[1])
                tmp = str(i[2])
                y = int(tmp.split('-')[0])
                m = int(tmp.split('-')[1])
                if (m == 12):
                    m = 1
                    y = y + 1
                else:
                    m = m + 1
                date = str(y) + '-' + str(m) + '-01' # date是salary中对应的date
                # print(i[3])
                dno=int(i[3])
                dname=i[4]
                sname=i[5]

                # print(date)
                sql_get_bsalary='select  bsalary from staff_info where sno=%d;'%(sno)
                self.user.cursor.execute(sql_get_bsalary)
                bsalary=self.user.cursor.fetchone()[0]
                # print(bsalary)
                sql_if_null='select * from salary where sno=%d and date=str_to_date("%s","%%Y-%%m-%%d");'%(sno,date)
                # print('if null: ',self.user.cursor.mogrify(sql_if_null))
                self.user.cursor.execute(sql_if_null)
                res_if_null=self.user.cursor.fetchall()
                # print('res_if_null',res_if_null)
                # print(len(res_if_null))

                sql_insert_fine='insert ignore into salary (sno, sname, dno, dname, date, bsalary, sumbonous, sumfine, sumsalary) VALUES (%d,"%s",%d,"%s",str_to_date("%s","%%Y-%%m-%%d"),%f,0,0,0);'
                # sql_insert_fine='insert ignore into salary set sno=%d,date=str_to_date("%s","%%Y-%%m-%%d"),bsalary=0,dno=%d,dname="%s",sname="%s";'%(sno,date,dno,dname,sname)
                sql_update_fine='update ignore salary set sumfine=sumfine+%f where sno=%d and  date=str_to_date("%s","%%Y-%%m-%%d");'%(fine,sno,date)
                # print(sql_insert_fine%(sno,sname,dno,dname, date,9 ))
                # print(self.user.cursor.mogrify(sql_insert_fine%(sno,sname,dno,dname, date,bsalary )))
                # t=self.user.cursor.mogrify(sql_update_fine)

                if len(res_if_null) == 0:
                    # print('insert salary: ')
                    # print(sql_insert_fine % (sno, sname, dno, dname, date, bsalary))
                    self.user.cursor.execute(
                        sql_insert_fine % (sno, sname, dno, dname, date, bsalary))  # 当时间冲突 有重复时会卡死。 update直接卡死，每个函数都没问题啊。
                    # res_insert=self.user.cursor.fetchall()
                    # print('res_insert',res_insert)
                    self.user.db.commit()
                # print('update fine:', t)
                # print('update: ',self.user.cursor.mogrify(sql_update_fine))
                self.user.cursor.execute(sql_update_fine)
                # res_update=self.user.cursor.fetchall()
                # print('res_update',res_update)
                # print('-'*80)
                self.user.db.commit()
            print('success update sumfine')

        except:
            print('update fine failed')
            self.user.db.rollback()


    def clear_sum(self):
        # 清空sumbonous,sumfine
        try:
            sql='update ignore salary set sumfine=0,sumbonous=0;'
            self.user.cursor.execute(sql)
            self.user.db.commit()
        except:
            print('清空sumfine,sumbonous失败')
            self.user.db.rollback()

    def update_sumsalary(self):
        try:
            sql_update_sumsalry = 'update salary set sumsalary=bsalary+sumbonous+sumfine;'
            self.user.cursor.execute(sql_update_sumsalry)
            self.user.db.commit()
        except:
            print('update sumsalary failed')
            self.user.db.rollback()

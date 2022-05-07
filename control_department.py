from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate
from department import Ui_department_window
from connectdb import User


class department_table(QMainWindow, Ui_department_window):
    def __init__(self, parent=None):
        super(department_table, self).__init__(parent)
        self.affected_rows_index = []
        self.currow = 0
        self.setupUi(self)

        self.modell = QStandardItemModel(10, 4)
        self.modell.setHorizontalHeaderLabels(
            ['部门', '人数', '平均薪水（元）','日期'])
        self.departmenttable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.departmenttable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.departmenttable.setModel(self.modell)
        # self.update_nop()
        # self.init_department_table()
        # self.user.show_processlist()
        # self.update_ave_salary()
        # self.update_nop()
        self.curdate=self.dateEdit.text().replace('/','-')
        # print('curdate',self.curdate,type(self.curdate))
        # print(self.dateEdit.date())
        self.init_department_table()

    def init_department_table(self):
        try:

            tmp=self.dateEdit.text()
            a=tmp.split('/')
            b = a[0] + '-' + a[1] + '-01'
            self.dateEdit.setDate(QDate(int(a[0]),int(a[1]),int(1)))
            print('init dep_table ing...')
            self.departmenttable.setModel(QStandardItemModel(20,4))

            # self.update_nop()
            # self.update_ave_salary()

            self.user = User()
            # ['员工号', '姓名', '部门', '金额', '罚款原因', '时间']
            self.curdate = self.dateEdit.text().replace('/', '-')
            # print(self.user.cursor.mogrify('select  dname, nop, avesalary,date from department where date=str_to_date("%s","%%Y-%%m-%%d")'%(self.curdate)) )
            self.user.cursor.execute(
                'select  dname, nop, avesalary,date from department where date=str_to_date("%s","%%Y-%%m-%%d");'%(self.curdate) )
            self.user.cursor.close()
            self.user.db.commit()
            # print('init指令：',self.user.cursor.mogrify('select  dname, nop, avesalary,date from department where date=str_to_date("%s","%%Y-%%m-%%d");'%(self.curdate)))
            res = self.user.cursor.fetchall()
            # print('res:',res,len(res))
            if len(res)==0: #空
                self.modell = QStandardItemModel(10, 4)
            cur_row_index = 0
            for cur in res:
                for i in range(4):
                    # print(cur[i], type(cur[i]))

                    # print('第',i,cur)
                    item = QStandardItem(str(cur[i]))
                    self.modell.setItem(cur_row_index, i, item)
                cur_row_index = cur_row_index + 1
            self.departmenttable.setModel(self.modell)
        except BaseException:
            self.user.db.rollback()
            print("表赋值失败")
        self.user.db.close()

    def update_nop(self):
        try:
            self.user = User()
            self.user.cursor=self.user.db.cursor()
            print('update_nop ing')
            self.curdate = self.dateEdit.text().replace('/', '-')
            sql_get_nop = 'select department.*,( select count(*) from staff_info where department.dno=staff_info.dno) 人数 from department ;'
            print(self.user.cursor.mogrify(sql_get_nop))
            self.user.cursor.execute(sql_get_nop)
            self.user.cursor.close()
            self.user.db.commit()
            res = self.user.cursor.fetchall()
            for i in res:
                # self.user.cursor = self.user.db.cursor()
                # (1, 'Navi', 2, Decimal('1000'), 3)
                # (2, '技术部', 3000, Decimal('18773'), datetime.date(2022, 5, 1), 3000) 更改后
                print(i)
                dno = i[0]
                date = str(i[4])
                nop = i[5]
                # print(date)
                # sql_test='select * from department where dno=%d and date=str_to_date("%s","%%Y-%%m-%%d");'%(dno,date)
                # self.user.cursor.execute(sql_test)
                # self.user.db.commit()
                # self.user.cursor.close()
                # ress=self.user.cursor.fetchall()
                # if len(ress)==0:
                #     print('dno date 无信息')
                #     return
                # print('ress',ress)
                self.user.cursor1 = self.user.db.cursor()
                sql = 'update ignore department set nop=%d where dno=%d and date=str_to_date("%s","%%Y-%%m-%%d");'
                print(self.user.cursor1.mogrify(sql % (nop, dno,date)))
                self.user.cursor1.execute(sql % (nop, dno,date)) #执行失败。。
                self.user.cursor1.close()
                self.user.db.commit()
                # print(s)
                print('人数',i[4])
            self.user.db.commit()
            print('success update nop')
            # self.init_department_table()

        except BaseException:
            print('更新人数失败')
            self.user.db.rollback()
        self.user.db.close()

    def update_ave_salary(self):
        try:
            self.user=User()
            self.curdate=self.dateEdit.text().replace('/','-')
            # 更新工资
            sql_update_sumsalry = 'update salary set sumsalary=bsalary+sumbonous-sumfine;'
            self.user.cursor.execute(sql_update_sumsalry)
            print('update sumsalsry success')
            dno_list = []  # 存放部门号,字典
            department_sumsalary = 0
            sql_get_dno = 'select dno from department;'
            self.user.cursor.execute(sql_get_dno)
            res = self.user.cursor.fetchall()
            # print('部门号',res)
            for i in res:
                # print(i[0])
                if i[0] not in dno_list:
                    dno_list.append(i[0])

            print(dno_list)
            for i in dno_list:
                sum_department_salary = 0  # 0.0就报错，无语

                ave_salary = 0.0
                # print('部门号',i)
                # self.curdate='2011-2-2'
                sql_get_sumsalary = 'select sumsalary from salary where dno=%d and date=str_to_date("%s","%%Y-%%m-%%d");'  % (
                    i,self.curdate)
                sql_get_nop = 'select nop from department where dno=%d and date=str_to_date("%s","%%Y-%%m-%%d");' % (i,self.curdate)
                # print('get_sumsalary:',self.user.cursor.mogrify(sql_get_sumsalary))
                self.user.cursor.execute(sql_get_nop)
                res_nop = self.user.cursor.fetchall()
                # print(len(res_nop),res_nop[0][0])
                # print('0',len(res_nop))
                if len(res_nop)==0:
                    # print(res_nop)
                    print('无该月份工资记录')
                    return 0
                # print('1')
                nop = res_nop[0][0] # 该部门人数
                print(i,'部门人数',nop)
                if nop>0: #此部门有人
                    self.user.cursor.execute(sql_get_sumsalary)
                    res_sumsalary = self.user.cursor.fetchall()
                    # print('sumsalary',res_sumsalary)
                    if len(res_sumsalary) > 0: #有salary信息
                        for j in res_sumsalary:
                            # print(j,type(j[0])) #j是元组
                            sum_department_salary = sum_department_salary + j[0]
                            # print('?')
                        # print('sum_department_salary',sum_department_salary)
                        ave_salary = round(sum_department_salary / nop, 2)
                else:
                    # print('该部门没人')
                    ave_salary = 0
                # print('平均工资', ave_salary)
                sql_insert_avesalary='insert ignore into department set avesalary=%f where dno=%d and date=str_to_date("%s","%%Y-%%m-%%d");' % (
                    ave_salary,i,self.curdate)
                self.user.cursor.execute(sql_insert_avesalary)
                sql_update_avesalary = 'update ignore  department set avesalary=%f where dno=%d and date=str_to_date("%s","%%Y-%%m-%%d");' % (
                    ave_salary,i,self.curdate)
                self.user.cursor.execute(sql_update_avesalary)

                # print('------------------')
                print('success update ave salary')

            self.user.db.commit()
            self.user.db.close()
            # self.init_department_table()

        except BaseException:
            # print('更新平均工资失败')
            self.user.db.rollback()

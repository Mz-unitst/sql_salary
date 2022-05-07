import time
import datetime
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from fine import Ui_fine_window
from connectdb import User


class fine_table(QMainWindow, Ui_fine_window):
    def __init__(self, parent=None):
        super(fine_table, self).__init__(parent)
        self.affected_rows_index = []  # 存下标本身
        self.currow = 0
        self.setupUi(self)
        self.user = User()
        self.cur_sno=0
        self.cur_date=''
        self.row_num = 20
        try:
            self.user.cursor.execute(
                'select fineno from fine')
            self.row_num = self.user.cursor.rowcount
        except BaseException:
            print('fine表格样式初始化失败')

        self.modell = QStandardItemModel(int(self.row_num), 7)
        self.modell.setHorizontalHeaderLabels(
            ['罚款号', '员工号', '姓名', '部门', '金额', '罚款原因', '时间'])
        self.finetable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.finetable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.finetable.setModel(self.modell)
        self.init_fine_table()
        # self.test_null()
        # self.test_add_date()
        # self.trigger_after_insert_fine()

    def add_item(self):
        self.modell.appendRow(QStandardItem('-1'))

    def del_item(self):
        # 删除行会改变行号，确保已经提交修改后再删除行
        cur_row_item = self.finetable.selectionModel().currentIndex()
        cur_index = cur_row_item.row()
        try:
            fine_no = self.modell.item(cur_index, 0).text()
            print(self.user.cursor.mogrify(
                "delete from fine where fineno= %d ;" % (int(fine_no))))
            self.user.cursor.execute(
                "delete from fine where fineno= %d ;" % (int(fine_no)))
            self.user.db.commit()
            print('删除fine成功')
        except BaseException:
            self.user.db.rollback()
            print('删除fine失败')
        self.modell.removeRow(cur_index)
        print("当前选中行:", cur_index)

    def change_item(self):
        # TODO 还需实现数据库修改
        # self.test_null()
        # return 0
        if len(self.affected_rows_index) == 0:
            print('没有修改需要被提交')
            return 0
        else:
            print('受影响行:',self.affected_rows_index)

        try:
            for i in range(len(self.affected_rows_index)):
                cur_row = self.affected_rows_index[i]
                print('提交第', cur_row + 1, '行数据')
                # 根据fine_no是否为空判断是添加还是修改

                sql_check = """select dname from staff_info where sno='%s' and sname='%s'""" % (
                    int(self.modell.item(cur_row, 1).text()), self.modell.item(cur_row, 2).text())
                self.user.cursor.execute(sql_check)
                check_res = self.user.cursor.fetchall()
                # print(check_res[0][0])
                if (len(check_res)) == 0:
                    print('员工信息不匹配')
                    return 0

                if self.modell.item(cur_row, 0).text() == '-1':  # 添加
                    print('添加数据')
                    # 要填满一行，不能留空格
                    # TODO 部门名做个触发器,从staff_info中找
                    sql_add = """insert into fine (sno, sname,  dname, fine, cause, date) values (%d,'%s','%s',%f,'%s',str_to_date( '%s','%%Y-%%m-%%d'));""" % (
                        int(self.modell.item(cur_row, 1).text()),
                        self.modell.item(cur_row, 2).text(),
                        self.modell.item(cur_row, 3).text(),
                        float(self.modell.item(cur_row, 4).text()),
                        self.modell.item(cur_row, 5).text(),
                        self.modell.item(cur_row, 6).text())
                    print(self.user.cursor.mogrify(sql_add))
                    self.user.cursor.execute(sql_add)
                    # print(self.user.cursor.mogrify(sql_add))
                    #再修改 salary
                    #insert 后 若 salary中没有对应的日期，即没有初始化。则应insert
                    # self.trigger_after_insert_fine(cur_row=cur_row)
                    self.user.db.commit()
                else:  # 修改
                    print('修改数据')
                    fine_no = self.modell.item(cur_row, 0).text()
                    # print('fine_no',fine_no,type(fine_no))
                    sql = "update fine set sno='%s',sname='%s',dname='%s',fine='%s',cause='%s',date=" + \
                        "str_to_date( '%s','%%Y-%%m-%%d')" + "where fineno='%s';"
                    sql_change = sql % (int(self.modell.item(cur_row, 1).text()),
                                        self.modell.item(cur_row, 2).text(),
                                        self.modell.item(cur_row, 3).text(),
                                        float(self.modell.item(cur_row, 4).text()),
                                        self.modell.item(cur_row, 5).text(),
                                        self.modell.item(cur_row, 6).text(),
                                        self.modell.item(cur_row, 0).text())
                    self.user.cursor.execute(sql_change)
                    self.user.db.commit()

                print('第', cur_row + 1, '行的修改已被提交')
            self.affected_rows_index = []  # 重置受影响行
        except BaseException:
            self.user.db.rollback()
            print('fine表修改提交失败')
        self.init_fine_table()

    def add_affected_rows(self):  # 添加一行也会触发这个..
        cur_row_item = self.finetable.selectionModel().currentIndex()
        cur_index = cur_row_item.row()
        if cur_index not in self.affected_rows_index:
            self.affected_rows_index.append(cur_index)
            # print(self.affected_rows_index)

    def init_fine_table(self):
        try:
            print('start init fine table')
            # ['员工号', '姓名', '部门', '金额', '罚款原因', '时间']
            self.user.cursor.execute(
                'select fineno,sno,sname,dname,fine,cause,date from fine;')
            self.user.db.commit()
            res = self.user.cursor.fetchall()
            cur_row_index = 0
            for cur in res:
                for i in range(7):
                    # print(cur[i], type(cur[i]))
                    item = QStandardItem(str(cur[i]))
                    self.modell.setItem(cur_row_index, i, item)
                cur_row_index = cur_row_index + 1
            print('success init fine table')
        except BaseException:
            self.user.db.rollback()
            print("表赋值失败")

    def test_print_row(self):
        u = self.finetable.selectionModel().selectedRows()
        print("selectedrows:", u)
        cur_row_index = self.finetable.selectionModel().currentIndex()
        print("当前选中行:", cur_row_index.row())

    def test_add_date(self):
        create_time = datetime.datetime.now().strftime("%Y-%m-%d")
        print(create_time)
        # sno不可空！
        self.user.db.commit()
        t = self.user.cursor.execute(
            """insert into fine (fineno,sno,date) value (%d,%d,str_to_date( '%s','%%Y-%%m-%%d'))""" %
            (3223, 223, '2011-01-11'))
        self.user.db.commit()
        print(t)
        # self.user.db.commit()

    def test_null(self):
        self.cur_sno=1
        self.cur_date='2022-10-11'
        year=int(self.cur_date.split('-')[0])
        month=int(self.cur_date.split('-')[1])
        if month == 12:
            year=year+1
            month=1
        else:
            month=month+1
        salary_date=str(year)+'-'+str(month)+'-01'
        print(salary_date)
        #TODO 为啥这里可以直接字符串表示时间？？
        sql="""SELECT date FROM salary where sno='%s' and date ='%s';"""%(self.cur_sno,salary_date)
        s=self.user.cursor.mogrify(sql)
        self.user.cursor.execute(sql)
        res=self.user.cursor.fetchall()
        if len(res)==0:
            #说明没初始化，应insert
            pass
        else:
            #直接update
            pass

    def trigger_after_insert_fine(self,cur_row=1):
        # 放弃 无法做出trigger 删除 old new
        # 插入fine后更新salary的sumfine项，值增加 cur row 为第几行
        #默认 salary中有对应？
        try:
            print('trigger after insert fine')
            sno=int(self.modell.item(cur_row, 1).text())
            old_date=self.modell.item(cur_row, 6).text()
            print(sno,old_date)
            tmp=old_date.split('-')
            y=int(tmp[0])
            m=int(tmp[1])
            m=m+1
            if(m==13):
                m=1
                y=y+1
            new_date=str(y)+'-'+str(m)+'-01'
            print(new_date)
            #todo bug:staff_info中bsalary应该有个表，加上时间才对。。无所谓了
            sql_select_salary="select * from salary where sno=%d and date =str_to_date( '%s','%%Y-%%m-%%d');"%(sno,new_date)
            t1=self.user.cursor.mogrify(sql_select_salary)
            print('t1',t1)
            self.user.cursor.execute(sql_select_salary)
            res_salary=self.user.cursor.fetchall()
            print(res_salary)
            sql_get_bsalary="select bsalary from staff_info where sno=%d;"%(sno)
            t2 = self.user.cursor.mogrify(sql_get_bsalary)
            print(t2)
            self.user.cursor.execute(sql_get_bsalary)
            res_get_bsalary=self.user.cursor.fetchall()
            bsalary=float(res_get_bsalary[0][0])
            fine=float(self.modell.item(cur_row, 4).text())
            print(res_get_bsalary,bsalary)
            if(len(res_salary)<1):
                #没找到记录 增应添加
                sql_insert_salary="insert into salary set sno=%d,sname='%s',date=str_to_date( '%s','%%Y-%%m-%%d'),bsalary=%f,sumbonous=0,sumfine=%d"%(sno,'2',new_date,bsalary,)
                t3=self.user.cursor.mogrify(sql_insert_salary)
                print(t3)
            else:
                sql_update_salary="update ignore salary set sumfine=sumfine+%f where sno=%d and date=str_to_date( '%s','%%Y-%%m-%%d');"%(fine,sno,new_date)
                t3 = self.user.cursor.mogrify(sql_update_salary)
                print(t3)
                self.user.cursor.execute(sql_update_salary)
                print('success update salary')
            #若有salary
        except:
            print('第%d行 trigger after insert fine failed'%(cur_row))
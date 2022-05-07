from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from base_salary import Ui_base_salary_window
from connectdb import User


class base_salary_window(QMainWindow, Ui_base_salary_window):
    def __init__(self, parent=None):
        super(base_salary_window, self).__init__(parent)
        # 需要setupUI才行。。。
        self.setupUi(self)
        self.user = User()
        self.query_dep()
        # self.query_dep(self, user)
        # self.dep_list.addItem('2')

    def query_dep(self):
        sss = """
        item(2).text()
        currentindex().data()
        """
        self.user.cursor.execute("select dname from department")
        res = self.user.cursor.fetchall()
        for i in res:
            # print(i[0])
            self.dep_list.addItem(i[0])
        # return res

    def query_staff(self):
        dname = self.dep_list.currentIndex().data()
        print(dname)
        self.user.cursor.execute(
            "select sno,sname,position  from staff_info where dname='%s' limit  10;" %
            (dname))
        sname = self.user.cursor.fetchall()
        self.staff_list.clear()
        for i in sname:
            self.staff_list.addItem(str(i[0]) +'-'+str(i[1]+'-'+str(i[2])))

    def query_base_salary(self):
        cur=self.staff_list.currentIndex().data()
        sno=cur.split('-')[0] # 用-做分隔符也行？？直接cur也行？？？WTF
        # print(sno)
        self.user.cursor.execute('select bsalary from staff_info where sno="%s"'%(sno))
        res=str(self.user.cursor.fetchone()[0])
        self.base_salary.setText(res)

    def change_base_salary(self):
        sno=self.staff_list.currentIndex().data().split('-')[0]
        try:
            new_salary=str(self.new_base_salary.text())
            self.user.cursor.execute('update staff_info set bsalary=%s where sno=%s' %(new_salary,sno))
            self.user.db.commit()
            self.base_salary.setText(new_salary)
            print('修改成功')
        except:
            self.user.db.rollback()
            print("修改失败，已回滚")
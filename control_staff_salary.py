from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from staffsalary import Ui_staff_salary_window
from connectdb import User
import conf

class staff_salary_table(QMainWindow, Ui_staff_salary_window):
    def __init__(self, parent=None):
        super(staff_salary_table, self).__init__(parent)
        self.affected_rows_index = []
        self.currow = 0
        self.setupUi(self)
        self.user = User()
        self.modell = QStandardItemModel(20, 8)
        self.modell.setHorizontalHeaderLabels(
            ['员工号', '姓名', '部门', '基本薪水', '总奖金', '总罚款', '总工资', '时间'])
        self.staffsalarytable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.staffsalarytable.setSelectionBehavior(
            QAbstractItemView.SelectRows)
        self.sno = 12
        self.staffsalarytable.setModel(self.modell)
        # self.test_func()
        # self.init_staff_salary()

    def init_staff_salary(self):  # 刷新页面
        # print(conf.sno)
        sql_update_sumsalry = 'update salary set sumsalary=bsalary+sumbonous-sumfine;'
        self.user.cursor.execute(sql_update_sumsalry)
        self.user.db.commit()
        sql = """
            select sno,sname,dname,bsalary,sumbonous,sumfine,sumsalary,date from salary where sno=%d;
        """%(conf.sno)
        self.user.cursor.execute(sql)
        res = self.user.cursor.fetchall()
        cur_row = 0
        for i in res:
            for j in range(8):
                self.modell.setItem(cur_row, j, QStandardItem(str(i[j])))

        self.show()

    def test_func(self):
        res_status = self.user.cursor.execute(
            'select pow(2,3);')  # res_status=1 执行成功
        res = self.user.cursor.fetchone()  # fetchone 获取结果
        print(res)

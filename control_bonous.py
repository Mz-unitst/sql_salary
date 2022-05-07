from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from bonous import Ui_bonous_window
from connectdb import User


class bonous_table(QMainWindow, Ui_bonous_window):
    def __init__(self, parent=None):
        super(bonous_table, self).__init__(parent)
        self.affected_rows_index = []
        self.currow = 0
        self.setupUi(self)
        self.user = User()
        self.cur_sno = 0
        self.cur_date = ''
        self.row_num = 20
        try:
            self.user.cursor.execute(
                'select bonousno from bonous')
            self.row_num = self.user.cursor.rowcount
        except BaseException:
            print('bonous表格样式初始化失败')

        self.modell = QStandardItemModel(int(self.row_num), 7)
        self.modell.setHorizontalHeaderLabels(
            ['奖励号', '员工号', '姓名', '部门', '金额', '奖励原因', '时间'])
        self.bonoustable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.bonoustable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bonoustable.setModel(self.modell)
        self.init_bonous_table()

    def add_item(self):
        self.modell.appendRow(QStandardItem('-1'))

    def del_item(self):
        cur_row_item = self.bonoustable.selectionModel().currentIndex()
        cur_index = cur_row_item.row()
        # TODO 还需实现数据库删除，已实现表格删除
        try:
            bonous_no = self.modell.item(cur_index, 0).text()
            self.user.cursor.execute(
                "delete from bonous where bonousno= '%s' " % (bonous_no))
            self.user.db.commit()
            print('删除bonous成功')
        except BaseException:
            self.user.db.rollback()
            print('删除bonous失败')
        self.modell.removeRow(cur_index)
        print("当前选中行:", cur_index)

    def change_item(self):
        if len(self.affected_rows_index) == 0:
            print('没有修改需要被提交')
            return 0
        else:
            print('受影响行:', self.affected_rows_index)

        try:
            #一次有误全体取消 ，懒得改
            for i in range(len(self.affected_rows_index)):
                cur_row = self.affected_rows_index[i]
                print('提交第', cur_row + 1, '行数据')

                sql_check = """select dname from staff_info where sno='%s' and sname='%s'""" % (
                int(self.modell.item(cur_row, 1).text()), self.modell.item(cur_row, 2).text())
                self.user.cursor.execute(sql_check)
                check_res = self.user.cursor.fetchall()
                # print(check_res[0][0])
                if(len(check_res))==0:
                    print('员工信息不匹配')
                    return 0


                # 根据fine_no是否为空判断是添加还是修改
                if self.modell.item(cur_row, 0).text() == '-1':  # 添加
                    print('添加数据')
                    # 要填满一行，不能留空格
                    # TODO 部门名做个触发器,从staff_info中找


                    sql_add = """insert into bonous (sno, sname,  dname, bonous, cause, date) values (%d,'%s','%s',%f,'%s',str_to_date( '%s','%%Y-%%m-%%d'))""" % (
                        int(self.modell.item(cur_row, 1).text()),
                        self.modell.item(cur_row, 2).text(),
                        self.modell.item(cur_row, 3).text(),
                        float(self.modell.item(cur_row, 4).text()),
                        self.modell.item(cur_row, 5).text(),
                        self.modell.item(cur_row, 6).text())
                    self.user.cursor.execute(sql_add)
                    # print(self.user.cursor.mogrify(sql_add))
                    self.user.db.commit()
                else:  # 修改
                    print('修改数据')
                    bonous_no = self.modell.item(cur_row, 0).text()
                    # print('fine_no',fine_no,type(fine_no))
                    sql = "update bonous set sno='%s',sname='%s',dname='%s',bonous='%s',cause='%s',date=" + \
                          "str_to_date( '%s','%%Y-%%m-%%d')" + \
                        "where bonousno='%s';"
                    sql_change = sql % (int(self.modell.item(cur_row, 1).text()),
                                        self.modell.item(cur_row, 2).text(),
                                        str(check_res[0][0]),
                                        float(self.modell.item(
                                            cur_row, 4).text()),
                                        self.modell.item(cur_row, 5).text(),
                                        self.modell.item(cur_row, 6).text(),
                                        self.modell.item(cur_row, 0).text())
                    self.user.cursor.execute(sql_change)
                    self.user.db.commit()
                print('第', cur_row + 1, '行的修改已被提交')
            self.affected_rows_index = []  # 重置受影响行
        except BaseException:
            self.user.db.rollback()
            print('bonous表修改提交失败')
        self.init_bonous_table()

    def add_affected_rows(self):
        cur_row_item = self.bonoustable.selectionModel().currentIndex()
        cur_index = cur_row_item.row()
        # TODO 小BUG，双击后即使不修改也会添加emmmmm,在addbutton加个判空好了
        if cur_index not in self.affected_rows_index:
            self.affected_rows_index.append(cur_index)
            for i in range(1,6):
                if  (self.bonoustable.selectionModel().currentIndex().data())=='':
                    self.modell.setItem(cur_index,i,QStandardItem(''))

        else:
            print('行已被修改过，无需添加')
        # print(self.affected_rows_index)

    def init_bonous_table(self):
        try:

            # ['员工号', '姓名', '部门', '金额', '罚款原因', '时间']
            self.user.cursor.execute(
                'select bonousno,sno,sname,dname,bonous,cause,date from bonous')
            self.user.db.commit()
            res = self.user.cursor.fetchall()
            # print(res)
            cur_row_index = 0
            for cur in res:
                for i in range(7):
                    # print(cur[i], type(cur[i]))
                    item = QStandardItem(str(cur[i]))
                    self.modell.setItem(cur_row_index, i, item)
                cur_row_index = cur_row_index + 1

        except BaseException:
            self.user.db.rollback()
            print("表赋值失败")

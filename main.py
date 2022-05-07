import pymysql
import sys
from fine import Ui_fine_window
from login import Ui_login_window
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import connectdb
from control_fine import fine_table
from control_bonous import bonous_table
from control_salary import salary_table
from control_department import department_table
from control_staff_salary import staff_salary_table
from control_base_salary import base_salary_window
from connectdb import User
from control_login import login_window
from control_admin_menu import admin_menu
from control_staff_menu import staff_menu
from control_update_password import update_password_window
import conf
user = User()
account = ''
password = ''
is_admin = False
# TODO BUG
aaasdsd = """
1.行号会变的，比如修改后删除了一行，那么行号就改变了，应该被修改的行找不到了
考虑用员工号做索引，添加员工号到列表中。
2.部门号与部门名称一一对应
"""


if __name__ == '__main__':
    apps = QApplication(sys.argv)
    mainw = QMainWindow()

    wlogin = login_window()
    wlogin.setupUi(mainw)

    wlogin.radioButton.clicked.connect(lambda :wlogin.change_account_label())

    fine_table = fine_table()
    fine_table.addbutton.clicked.connect(lambda: fine_table.add_item())
    fine_table.delbutthon.clicked.connect(lambda: fine_table.del_item())
    fine_table.changebutton.clicked.connect(lambda: fine_table.change_item())
    # 有model单元格被修改时添加affected_row[]
    fine_table.modell.itemChanged.connect(
        lambda: fine_table.add_affected_rows())

    bonous_table = bonous_table()
    bonous_table.addbutton.clicked.connect(lambda: bonous_table.add_item())
    bonous_table.delbutthon.clicked.connect(lambda: bonous_table.del_item())
    bonous_table.changebutton.clicked.connect(
        lambda: bonous_table.change_item())
    # 有model单元格被修改时添加affected_row[] ，将表格eidt属性设置为anykeypressed
    bonous_table.modell.itemChanged.connect(
        lambda: bonous_table.add_affected_rows())

    salary_table = salary_table()
    staff_salary_table = staff_salary_table()


    department_table = department_table()
    department_table.dateEdit.dateChanged.connect(lambda :department_table.init_department_table())


    basesalary_window = base_salary_window()
    basesalary_window.change_button.clicked.connect(
        lambda: print('butthon clicked'))
    basesalary_window.dep_list.itemClicked.connect(
        lambda: basesalary_window.query_staff())
    basesalary_window.staff_list.itemClicked.connect(
        lambda: basesalary_window.query_base_salary())
    basesalary_window.change_button.clicked.connect(
        lambda: basesalary_window.change_base_salary())

    admin_menu=admin_menu()
    admin_menu.base_button.clicked.connect(lambda :basesalary_window.show())
    admin_menu.salary_button.clicked.connect(lambda :salary_table.show())
    admin_menu.department_button.clicked.connect(lambda :department_table.show())
    admin_menu.fine_button.clicked.connect(lambda :fine_table.show())
    admin_menu.bonous_button.clicked.connect(lambda: bonous_table.show())

    staff_menu=staff_menu()
    update_password_window = update_password_window()

    staff_menu.salary_button.clicked.connect(lambda :staff_salary_table.init_staff_salary())
    staff_menu.update_button.clicked.connect(lambda: update_password_window.show())
    update_password_window.submit_button.clicked.connect(lambda :update_password_window.update_password())

    def login():
        wlogin.check_admin(
            wlogin.account.text(),
            wlogin.password.text())
        if conf.suc_login == 1:
            if wlogin.radioButton.isChecked() == True:
                print('success login admin')
                admin_menu.show()
            else:
                staff_menu.show()
                print('员工功能，修改密码+查询流水')
        conf.suc_login=0

    wlogin.login_button.clicked.connect(
        lambda: login())

    # staff_menu.show()
    # admin_menu.show()
    # basesalary_window.show()
    # staff_salary_table.show()
    # department_table.show()
    # salary_table.show()
    # bonous_table.show()
    # fine_table.show()
    mainw.show()
    # update_password_window.show()
    apps.exec()

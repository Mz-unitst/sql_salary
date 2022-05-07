from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from base_salary import Ui_base_salary_window
from connectdb import User
from login import Ui_login_window
import conf

class login_window(QMainWindow, Ui_login_window):
    def __init__(self, parent=None):
        super(login_window, self).__init__(parent)
        self.setupUi(self)

        self.username = ''
        self.password = ''
        self.suc_login=0
        # self.update_password()

    def check_admin(self, a, b):
        is_admin = self.radioButton.isChecked()
        print(is_admin)
        if is_admin==True:
            self.username=a
        else:
            self.username = int(a)
        self.password = str(b)
        print(self.username, self.password)
        if is_admin == True:
            print('admin login')
            self.login_admin()

        else:
            print('staff login')
            self.login_staff()


    def login_admin(self):
        try:
            self.user = User()
            self.user.cursor.execute(
                "select * from admin where username='%s' and password=md5('%s')" %
                (self.username, self.password))
            self.user.db.commit()
            res = self.user.cursor.fetchone()
            print(res)
            if res is not None:
                print('登录成功')
                conf.suc_login = 1
            else:
                print('账密错误')
                self.suc_login=0
                conf.suc_login = 0
        except BaseException:
            self.user.db.rollback()
            print('登录失败')
            self.user.db.close()

    def login_staff(self):
        try:
            print('start login staff')
            # a=self.user.cursor.mogrify(
            #     "select * from staff_info where sno=%d and password=md5('%s')" % (self.username, self.password))
            # print(a)
            #类型错误 无语
            self.user.cursor.execute(
                "select * from staff_info where sno=%d and password=md5('%s')" % (self.username, self.password))
            self.user.db.commit()
            res = self.user.cursor.fetchone()

            if res is not None:
                print(res[1],'登录成功')
                conf.suc_login = 1
                conf.sno=int(self.username)
                conf.password=self.password
        except BaseException:
            self.user.db.rollback()
            print('登录失败')
            self.suc_login=0
            conf.suc_login = 0

    def update_password(self):
        print('start update')
        for i in range(1000, 2010):
            try:
                self.user.cursor.execute(
                    "UPDATE staff_info SET password = 'e10adc3949ba59abbe56e057f20f883e' WHERE sno ='%s';"%(i))
                self.user.db.commit()
                # print(self.user.cursor.rowcount)
            except BaseException:
                self.user.db.rollback()
                print('密码更新失败')
        print('success')

    def change_account_label(self):
        if self.radioButton.isChecked()==True:
            self.label_account.setText('管理员账号名')
        else:
            self.label_account.setText('员工号')



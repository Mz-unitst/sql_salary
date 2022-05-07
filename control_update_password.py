from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from base_salary import Ui_base_salary_window
from connectdb import User
from update_password import Ui_update_password
import conf

class update_password_window(QMainWindow, Ui_update_password):
    def __init__(self, parent=None):
        super(update_password_window, self).__init__(parent)
        self.setupUi(self)
        self.user=User()

    def update_password(self):
        # old=self.old_password.text()
        # new1=self.new_password.text()
        # new2=self.re_new_password.text()
        # sno=int(conf.sno)
        # pw=conf.password
        # # print(old,new1,new2,sno,pw)
        if self.new_password.text()==self.re_new_password.text() and self.old_password.text()==conf.password and len(self.new_password.text())>1:
            try:
                print('try to udpate password')
                # print(type(conf.sno))
                # print(self.user.cursor.mogrify('select * from salary.staff_info where sno=%d;'%(sno)))
                self.user.cursor.execute('select * from salary.staff_info where sno=%d;'%(conf.sno))
                ress = self.user.cursor.fetchall()
                # print('ress', ress[0])
                # print(self.user.cursor.mogrify('update staff_info set password=md5("%s") where sno=%d;')%(self.new_password.text(),sno))
                self.user.cursor.execute('update ignore staff_info set password=md5("%s") where sno=%d;'%(self.new_password.text(),conf.sno))
                # res=self.user.cursor.fetchall()
                # print('res',res)
                self.user.db.commit()
            except:
                print('密码修改失败')
                self.user.db.rollback()
        else:
            print('本地检验失败')

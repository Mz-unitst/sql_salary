# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'staff_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_staff_menu(object):
    def setupUi(self, staff_menu):
        staff_menu.setObjectName("staff_menu")
        staff_menu.resize(305, 233)
        self.salary_button = QtWidgets.QPushButton(staff_menu)
        self.salary_button.setGeometry(QtCore.QRect(50, 40, 191, 51))
        self.salary_button.setObjectName("salary_button")
        self.update_button = QtWidgets.QPushButton(staff_menu)
        self.update_button.setGeometry(QtCore.QRect(50, 120, 191, 51))
        self.update_button.setObjectName("update_button")

        self.retranslateUi(staff_menu)
        QtCore.QMetaObject.connectSlotsByName(staff_menu)

    def retranslateUi(self, staff_menu):
        _translate = QtCore.QCoreApplication.translate
        staff_menu.setWindowTitle(_translate("staff_menu", "员工菜单界面"))
        self.salary_button.setText(_translate("staff_menu", "查看工资流水"))
        self.update_button.setText(_translate("staff_menu", "修改密码"))
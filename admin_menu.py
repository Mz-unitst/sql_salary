# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_admin_menu(object):
    def setupUi(self, admin_menu):
        admin_menu.setObjectName("admin_menu")
        admin_menu.resize(378, 300)
        self.base_button = QtWidgets.QPushButton(admin_menu)
        self.base_button.setGeometry(QtCore.QRect(90, 50, 191, 51))
        self.base_button.setObjectName("base_button")
        self.salary_button = QtWidgets.QPushButton(admin_menu)
        self.salary_button.setGeometry(QtCore.QRect(90, 120, 191, 51))
        self.salary_button.setObjectName("salary_button")
        self.department_button = QtWidgets.QPushButton(admin_menu)
        self.department_button.setGeometry(QtCore.QRect(90, 200, 191, 51))
        self.department_button.setObjectName("department_button")

        self.retranslateUi(admin_menu)
        QtCore.QMetaObject.connectSlotsByName(admin_menu)

    def retranslateUi(self, admin_menu):
        _translate = QtCore.QCoreApplication.translate
        admin_menu.setWindowTitle(_translate("admin_menu", "管理员功能菜单"))
        self.base_button.setText(_translate("admin_menu", "修改基本工资"))
        self.salary_button.setText(_translate("admin_menu", "查询工资流水"))
        self.department_button.setText(_translate("admin_menu", "查询部门平均工资"))

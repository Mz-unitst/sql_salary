# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'salary.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_salary_window(object):
    def setupUi(self, salary_window):
        salary_window.setObjectName("salary_window")
        salary_window.resize(907, 517)
        self.salarytable = QtWidgets.QTableView(salary_window)
        self.salarytable.setGeometry(QtCore.QRect(0, 0, 911, 521))
        self.salarytable.setMouseTracking(False)
        self.salarytable.setObjectName("salarytable")

        self.retranslateUi(salary_window)
        QtCore.QMetaObject.connectSlotsByName(salary_window)

    def retranslateUi(self, salary_window):
        _translate = QtCore.QCoreApplication.translate
        salary_window.setWindowTitle(_translate("salary_window", "全体员工工资流水"))

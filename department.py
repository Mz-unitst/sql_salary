# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'department.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_department_window(object):
    def setupUi(self, department_window):
        department_window.setObjectName("department_window")
        department_window.resize(781, 436)
        self.departmenttable = QtWidgets.QTableView(department_window)
        self.departmenttable.setGeometry(QtCore.QRect(40, 50, 617, 331))
        self.departmenttable.setMouseTracking(False)
        self.departmenttable.setObjectName("departmenttable")
        self.dateEdit = QtWidgets.QDateEdit(department_window)
        self.dateEdit.setGeometry(QtCore.QRect(90, 10, 121, 31))
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 5, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.label = QtWidgets.QLabel(department_window)
        self.label.setGeometry(QtCore.QRect(43, 12, 71, 31))
        self.label.setObjectName("label")

        self.retranslateUi(department_window)
        QtCore.QMetaObject.connectSlotsByName(department_window)

    def retranslateUi(self, department_window):
        _translate = QtCore.QCoreApplication.translate
        department_window.setWindowTitle(_translate("department_window", "部门平均工资"))
        self.label.setText(_translate("department_window", "时间："))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fine.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_fine_window(object):
    def setupUi(self, fine_window):
        fine_window.setObjectName("fine_window")
        fine_window.resize(784, 421)
        self.finetable = QtWidgets.QTableView(fine_window)
        self.finetable.setGeometry(QtCore.QRect(40, 30, 617, 331))
        self.finetable.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed)
        self.finetable.setObjectName("finetable")
        self.addbutton = QtWidgets.QPushButton(fine_window)
        self.addbutton.setGeometry(QtCore.QRect(690, 100, 75, 23))
        self.addbutton.setObjectName("addbutton")
        self.delbutthon = QtWidgets.QPushButton(fine_window)
        self.delbutthon.setGeometry(QtCore.QRect(690, 150, 75, 23))
        self.delbutthon.setObjectName("delbutthon")
        self.changebutton = QtWidgets.QPushButton(fine_window)
        self.changebutton.setGeometry(QtCore.QRect(690, 210, 75, 23))
        self.changebutton.setObjectName("changebutton")

        self.retranslateUi(fine_window)
        QtCore.QMetaObject.connectSlotsByName(fine_window)

    def retranslateUi(self, fine_window):
        _translate = QtCore.QCoreApplication.translate
        fine_window.setWindowTitle(_translate("fine_window", "修改罚金"))
        self.addbutton.setText(_translate("fine_window", "增加一行"))
        self.delbutthon.setText(_translate("fine_window", "删除该行"))
        self.changebutton.setText(_translate("fine_window", "提交修改"))

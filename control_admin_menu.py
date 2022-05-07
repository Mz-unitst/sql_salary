from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from admin_menu import Ui_admin_menu

class admin_menu(QMainWindow, Ui_admin_menu):
    def __init__(self, parent=None):
        super(admin_menu, self).__init__(parent)
        self.setupUi(self)



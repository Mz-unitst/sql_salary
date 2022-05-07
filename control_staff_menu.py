from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from staff_menu import Ui_staff_menu
from connectdb import User

class staff_menu(QMainWindow, Ui_staff_menu):
    def __init__(self, parent=None):
        super(staff_menu, self).__init__(parent)
        self.setupUi(self)



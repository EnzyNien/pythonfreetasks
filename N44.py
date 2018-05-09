from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys


class MainClass():

    def calc(self):
        try:
            amount = round(
                int(self.mainWindow.lineedit_count.text()) * self.price, 2)
            amount = f'сумма = {amount} руб.'
        except BaseException:
            amount = 'error input data'
        self.mainWindow.label_amount.setText(amount)

    def set_price(self, val):
        val = round(float(val), 2)
        self.price = val
        self.mainWindow.label_per_one.setText(f'1 шт. = {val} руб.')

    def on_button_group_clicked(self, button):
        price = self.price_dict.get(button.text(), 0)
        self.set_price(price)

    class mainWindowClass(QtWidgets.QMainWindow):

        def __init__(self, parent=None, fatherlyClass=None):
            QtWidgets.QMainWindow.__init__(self, parent)
            self.centralwidget = QtWidgets.QWidget()
            self.centralwidget.setObjectName("centralwidget")

            self.radio_button_9x12 = QtWidgets.QRadioButton('9 x 12')
            self.radio_button_9x12.setChecked(True)

            self.radio_button_10x15 = QtWidgets.QRadioButton('10 x 15')
            self.radio_button_18x24 = QtWidgets.QRadioButton('18 x 24')

            self.label_group_name = QtWidgets.QLabel()
            self.label_group_name.setObjectName("label_group_name")
            self.label_group_name.setText("Формат")

            self.label_count = QtWidgets.QLabel()
            self.label_count.setObjectName("label_count")
            self.label_count.setText("Количество:")

            self.lineedit_count = QtWidgets.QLineEdit()
            self.lineedit_count.setObjectName("lineedit_count")

            self.label_amount = QtWidgets.QLabel()
            self.label_amount.setObjectName("label_amount")
            self.label_amount.setText("сумма = 0.0 руб.")

            self.label_per_one = QtWidgets.QLabel()
            self.label_per_one.setObjectName("label_per_one")
            self.label_per_one.setText("1 шт. = 0.0 руб.")

            self.button_group = QtWidgets.QButtonGroup()
            self.button_group.addButton(self.radio_button_9x12)
            self.button_group.addButton(self.radio_button_10x15)
            self.button_group.addButton(self.radio_button_18x24)
            self.button_group.buttonClicked.connect(
                fatherlyClass.on_button_group_clicked)

            self.mainWindow_button_calc = QtWidgets.QPushButton('OK')
            self.mainWindow_button_calc.setObjectName("button_find")

            vbox_radio = QtWidgets.QVBoxLayout()
            vbox_radio.addWidget(self.label_group_name)
            vbox_radio.addWidget(self.radio_button_9x12)
            vbox_radio.addWidget(self.radio_button_10x15)
            vbox_radio.addWidget(self.radio_button_18x24)
            vbox_radio.addWidget(self.label_per_one)
            vbox_radio.addSpacing(1)

            hbox_count = QtWidgets.QHBoxLayout()
            hbox_count.addWidget(self.label_count)
            hbox_count.addWidget(self.lineedit_count)

            vbox = QtWidgets.QVBoxLayout()
            vbox.addLayout(vbox_radio)
            vbox.addLayout(hbox_count)
            vbox.addWidget(self.mainWindow_button_calc)
            vbox.addWidget(self.label_amount)

            self.centralwidget.setLayout(vbox)
            self.setCentralWidget(self.centralwidget)

            self.mainWindow_button_calc.clicked.connect(fatherlyClass.calc)

    def __init__(self):
        self.price = 0.0
        self.price_dict = {'9 x 12': 10, '10 x 15': 12, '18 x 24': 15}

        self.mainWindow = self.mainWindowClass(fatherlyClass=self)
        price = self.price_dict.get('9 x 12', 0)
        self.set_price(price)
        self.mainWindow.setWindowTitle('Печать фотографий')
        self.mainWindow.setWindowFlags(QtCore.Qt.Window)
        self.mainWindow.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = MainClass()
    sys.exit(app.exec_())

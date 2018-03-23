from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, Qt
import sqlite3 as lite
import sys
'''
CREATE TABLE "words" ( `word` TEXT UNIQUE, `low_word` TEXT, `definition` TEXT, `index` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE )
'''

class MainClass():

	def showQuestion(self,text = ''):
		self.dialogYes = False
		dialog = QtWidgets.QDialog()
		dialog_mainWindow_label_word = QtWidgets.QLabel(text)
		dialog_button_yes = QtWidgets.QPushButton("Да")
		dialog_button_no = QtWidgets.QPushButton("Нет")

		hbox = QtWidgets.QHBoxLayout()
		hbox.addWidget(dialog_button_yes)
		hbox.addWidget(dialog_button_no)

		vbox = QtWidgets.QVBoxLayout()
		vbox.addWidget(dialog_mainWindow_label_word)
		vbox.addLayout(hbox)
		dialog.setLayout(vbox)

		dialog.setWindowTitle("Вопрос")
		dialog.setWindowModality(QtCore.Qt.ApplicationModal)
		dialog_button_yes.clicked.connect(dialog.accept)
		dialog_button_no.clicked.connect(dialog.reject)
		return dialog


	def selectLike(self,text):
		if not text:
			return None
		query = QtSql.QSqlQuery()
		query.exec("select * from words where low_word like '%{}%' ORDER BY word ASC".format(text))
		return query

	def selectBy(self,text):
		if not text:
			return None
		query = QtSql.QSqlQuery()
		query.exec("select * from words where low_word == '{}' ORDER BY word ASC".format(text))
		return query

	def selectByList(self,text):
		if not text:
			return None
		query = QtSql.QSqlQuery()
		query.exec('select * from words where _rowid_ in ({})'.format(text))
		return query
	

	def insertBy(self,word,definition):
		if not word or not definition:
			return None
		query = QtSql.QSqlQuery()
		query.exec("insert into words (word,low_word,definition) values ('{}', '{}', '{}')".format(word,word.lower(),definition))
		return query

	def updateBy(self,idx,definition):
		if not idx or not definition:
			return None
		query = QtSql.QSqlQuery()
		query.exec("update words set definition = '{}' where _rowid_ = {}".format(definition,idx))
		return query

	def deleteBy(self,idx):
		if not idx:
			return None
		query = QtSql.QSqlQuery()
		query.exec("delete from words where _rowid_ = {}".format(idx))
		return query

	def fillTable(self,listrow):
		self.mainWindow.tableWidget.setRowCount(len(listrow))
		for idx, row in enumerate(listrow):
			self.mainWindow.tableWidget.setItem(idx, 0, QtWidgets.QTableWidgetItem(row[0]))
			self.mainWindow.tableWidget.setItem(idx, 1, QtWidgets.QTableWidgetItem(row[1]))
			self.mainWindow.tableWidget.setItem(idx, 2, QtWidgets.QTableWidgetItem(row[2]))

	def updateTable(self):
		resultlist = []
		rows = self.mainWindow.tableWidget.rowCount()
		idlist = [str(self.mainWindow.tableWidget.item(row,2).text()) for row in range(rows)]
		idlist = ','.join(idlist)
		query = self.selectByList(idlist)
		if query is None:
			return
		if query.isActive():
			self.mainWindow.tableWidget.clear()
			self.mainWindow.mainWindow_textedit_definition.clear()
			query.first()
			count = 0
			while query.isValid():
				resultlist.append([query.value('word'),query.value('definition'),str(query.value('index'))])
				count += 1
				query.next()
			self.fillTable(resultlist)

	def open_add_word_window(self):
		self.editWindow.editWindow_lineEdit.clear()
		self.editWindow.textEdit.clear()
		self.editWindow.show()

	def find_word(self):
		resultlist = []
		query = self.selectLike(self.mainWindow.mainWindow_lineEdit.text().strip().lower())
		if query is None:
			return
		if query.isActive():
			self.mainWindow.tableWidget.clear()
			self.mainWindow.mainWindow_textedit_definition.clear()
			query.first()
			count = 0
			while query.isValid():
				resultlist.append([query.value('word'),query.value('definition'),str(query.value('index'))])
				count += 1
				query.next()
			self.fillTable(resultlist)
		
	def tab_item_one_click_event(self, item):
		data_ = self.mainWindow.tableWidget.item(item.row(),1).text()
		self.mainWindow.mainWindow_textedit_definition.setText(data_)

	def edit_word(self):
		definition = self.mainWindow.mainWindow_textedit_definition.toPlainText()
		if not definition:
			return
		dialog = self.showQuestion('Изменить текст?')
		if dialog.exec() == 0:
			return	
		row_ = self.mainWindow.tableWidget.selectionModel().currentIndex().row()
		idx_ = self.mainWindow.tableWidget.item(row_,2).text()
		definition = self.mainWindow.mainWindow_textedit_definition.toPlainText()
		query = self.updateBy(int(idx_),definition)
		if query is None:
			return
		if query.isActive():
			self.updateTable()

	def del_word(self):
		dialog = self.showQuestion('Удалить слово?')
		if dialog.exec() == 0:
			return	
		row_ = self.mainWindow.tableWidget.selectionModel().currentIndex().row()
		idx_ = self.mainWindow.tableWidget. item(row_,2).text()
		query = self.deleteBy(int(idx_))
		if query is None:
			return
		if query.isActive():
			self.mainWindow.mainWindow_textedit_definition.clear()
			self.updateTable()

	def add_word(self):
		dialog = self.showQuestion('Добавить слово?')
		if dialog.exec() == 0:
			return	
		word = self.editWindow.editWindow_lineEdit.text()
		definition = self.editWindow.textEdit.toPlainText()
		query = self.insertBy(word,definition)
		if query is None:
			return
		if query.isActive():
			self.editWindow.editWindow_lineEdit.clear()
			self.editWindow.textEdit.clear()

	def close_modal(self):
		self.editWindow.close()

	class editWindowClass(QtWidgets.QWidget):

		def __init__(self, parent=None, fatherlyClass = None):
			QtWidgets.QWidget.__init__(self,parent)
			self.editWindow_button_add = QtWidgets.QPushButton('Добавить')
			self.editWindow_button_close = QtWidgets.QPushButton('Закрыть')
			self.editWindow_lineEdit = QtWidgets.QLineEdit()
			self.textEdit = QtWidgets.QTextEdit()
			vbox = QtWidgets.QVBoxLayout()
			vbox.addWidget(self.editWindow_lineEdit)
			vbox.addWidget(self.editWindow_button_add)
			vbox.addWidget(self.editWindow_button_close)
			vbox.addStretch()
			
			hbox = QtWidgets.QHBoxLayout()
			hbox.addLayout(vbox)
			hbox.addWidget(self.textEdit)
			self.setLayout(hbox)

			self.editWindow_label_definition = QtWidgets.QLabel()
			self.editWindow_label_word = QtWidgets.QLabel()
			self.statusbar = QtWidgets.QStatusBar()
			self.setWindowModality(QtCore.Qt.WindowModal)

			self.editWindow_button_add.clicked.connect(fatherlyClass.add_word)
			self.editWindow_button_close.clicked.connect(fatherlyClass.close_modal)

	class mainWindowClass(QtWidgets.QMainWindow):

		def __init__(self, parent=None, fatherlyClass = None):
			QtWidgets.QMainWindow.__init__(self,parent)
			self.centralwidget = QtWidgets.QWidget()
			self.centralwidget.setObjectName("centralwidget")

			self.fontSegoePrint20 = QtGui.QFont()
			self.fontSegoePrint20.setFamily("Segoe Print")
			self.fontSegoePrint20.setPointSize(20)

			self.fontSegoePrint13 = QtGui.QFont()
			self.fontSegoePrint13.setFamily("Segoe Print")
			self.fontSegoePrint13.setPointSize(13)


			self.mainWindow_lineEdit = QtWidgets.QLineEdit()
			self.mainWindow_lineEdit.setObjectName("lineEdit")
			self.mainWindow_lineEdit.setMaximumWidth(300)

			self.mainWindow_button_find = QtWidgets.QPushButton('Поиск')
			self.mainWindow_button_find.setObjectName("button_find")
			self.mainWindow_button_find.setMaximumWidth(300)

			self.tableWidget = QtWidgets.QTableWidget()
			self.tableWidget.setColumnCount(3)
			self.tableWidget.hideColumn(1)
			self.tableWidget.hideColumn(2)
			self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
			self.tableWidget.verticalHeader().setVisible(False)
			self.tableWidget.setObjectName("listWidget")
			self.tableWidget.setMaximumWidth(300)

			self.mainWindow_label_word = QtWidgets.QLabel()
			self.mainWindow_label_word.setFont(self.fontSegoePrint13)
			self.mainWindow_label_word.setObjectName("label_word")
			self.mainWindow_label_word.setText("Слова")
			self.mainWindow_label_word.setMaximumWidth(300)

			self.mainWindow_label_definition = QtWidgets.QLabel()
			self.mainWindow_label_definition.setFont(self.fontSegoePrint20)
			self.mainWindow_label_definition.setObjectName("label_definition")
			self.mainWindow_label_definition.setText("Определение")

			self.mainWindow_button_edit = QtWidgets.QPushButton("Редактировать")
			self.mainWindow_button_edit.setObjectName("button_edit")

			self.mainWindow_button_del = QtWidgets.QPushButton("Удалить")
			self.mainWindow_button_del.setObjectName("button_del")

			self.mainWindow_textedit_definition = QtWidgets.QTextEdit()
			self.mainWindow_textedit_definition.AutoFormattingFlag(0)
			self.mainWindow_textedit_definition.height=250
			self.mainWindow_textedit_definition.setObjectName("textedit_definition")
	
			vboxLeft = QtWidgets.QVBoxLayout()
			vboxLeft.addWidget(self.mainWindow_lineEdit)
			vboxLeft.addWidget(self.mainWindow_button_find)
			vboxLeft.addWidget(self.mainWindow_label_word)
			vboxLeft.addWidget(self.tableWidget)
			#vboxLeft.addStretch(1)
		
			hboxButton = QtWidgets.QHBoxLayout()
			hboxButton.addWidget(self.mainWindow_button_edit)
			hboxButton.addWidget(self.mainWindow_button_del)
			hboxButton.addStretch(1)		

			vboxRight = QtWidgets.QVBoxLayout()
			vboxRight.addWidget(self.mainWindow_label_definition)
			vboxRight.addWidget(self.mainWindow_textedit_definition)
			vboxRight.addLayout(hboxButton)
			
			hbox = QtWidgets.QHBoxLayout()
			hbox.addLayout(vboxLeft)
			hbox.addLayout(vboxRight)
			self.centralwidget.setLayout(hbox)
			self.setCentralWidget(self.centralwidget)

			self.mainWindow_menubar = QtWidgets.QMenuBar()
			self.mainWindow_menubar.setObjectName("menubar")

			self.setMenuBar(self.mainWindow_menubar)

			self.mainWindow_menu = QtWidgets.QMenu(self.mainWindow_menubar)
			self.mainWindow_menu.setObjectName("menu")

			self.mainWindow_menuaction_add = QtWidgets.QAction('Добавить')
			self.mainWindow_menuaction_add.setObjectName("menuaction_add")

			self.mainWindow_menuaction_exit = QtWidgets.QAction('Выход')
			self.mainWindow_menuaction_exit.setObjectName("menuaction_exit")

			self.mainWindow_menu.addAction(self.mainWindow_menuaction_add)
			self.mainWindow_menu.addAction(self.mainWindow_menuaction_exit)

			self.mainWindow_menubar.addAction(self.mainWindow_menu.menuAction())

			self.mainWindow_menu.setTitle("Файл")
			self.mainWindow_menuaction_add.setText("Добавить")
			self.mainWindow_menuaction_exit.setText("Выход")


			self.statusbar = QtWidgets.QStatusBar()
			self.statusbar.setObjectName("statusbar")
			self.setStatusBar(self.statusbar )

			self.tableWidget.itemClicked.connect(fatherlyClass.tab_item_one_click_event)
			self.mainWindow_menuaction_add.triggered.connect(fatherlyClass.open_add_word_window)
			self.mainWindow_button_find.clicked.connect(fatherlyClass.find_word)
			self.mainWindow_button_edit.clicked.connect(fatherlyClass.edit_word)
			self.mainWindow_button_del.clicked.connect(fatherlyClass.del_word)
			self.mainWindow_menuaction_exit.triggered.connect(QtWidgets.qApp.quit)

	def __init__(self):
		
		self.dialogYes = False

		self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
		self.db.setDatabaseName('dict.db')
		self.db.open()
		self.mainWindow = self.mainWindowClass(fatherlyClass = self)
		self.mainWindow.resize(599, 364)
		self.mainWindow.setWindowTitle('Словарь')
		self.mainWindow.setWindowFlags(QtCore.Qt.Window)

		self.editWindow = self.editWindowClass(self.mainWindow, fatherlyClass = self)
		self.editWindow.resize(466, 288)
		self.editWindow.setWindowTitle('Добавление элемента в базу данных')
		self.editWindow.setWindowFlags(QtCore.Qt.Window)

		self.mainWindow.show()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	gui = MainClass()
	sys.exit(app.exec_())

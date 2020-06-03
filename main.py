from tools import *
from PyQt5 import QtCore, QtGui, QtWidgets

URL = 'https://windows.php.net/downloads/releases/archives/'


links = extractLinks(URL)
releases = clearData(links)
print(releases)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 602)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(7)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.phpVersionsTreeView = QtWidgets.QTreeView(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.phpVersionsTreeView.setFont(font)
        self.phpVersionsTreeView.setObjectName("phpVersionsTreeView")
        self.verticalLayout_4.addWidget(self.phpVersionsTreeView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.loadBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.loadBtn.setFont(font)
        self.loadBtn.setObjectName("loadBtn")
        self.horizontalLayout_2.addWidget(self.loadBtn)
        self.installBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.installBtn.setFont(font)
        self.installBtn.setObjectName("installBtn")
        self.horizontalLayout_2.addWidget(self.installBtn)
        self.withTScheckBox = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.withTScheckBox.setFont(font)
        self.withTScheckBox.setObjectName("withTScheckBox")
        self.horizontalLayout_2.addWidget(self.withTScheckBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(7)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.installedVesionList = QtWidgets.QListView(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.installedVesionList.setFont(font)
        self.installedVesionList.setObjectName("installedVesionList")
        self.verticalLayout_5.addWidget(self.installedVesionList)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.removeBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.removeBtn.setFont(font)
        self.removeBtn.setObjectName("removeBtn")
        self.horizontalLayout_3.addWidget(self.removeBtn)
        self.useBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.useBtn.setFont(font)
        self.useBtn.setObjectName("useBtn")
        self.horizontalLayout_3.addWidget(self.useBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(7)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        self.formLayout_2.setSpacing(7)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.phpVersionTextbox = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phpVersionTextbox.sizePolicy().hasHeightForWidth())
        self.phpVersionTextbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.phpVersionTextbox.setFont(font)
        self.phpVersionTextbox.setText("")
        self.phpVersionTextbox.setReadOnly(True)
        self.phpVersionTextbox.setPlaceholderText("")
        self.phpVersionTextbox.setObjectName("phpVersionTextbox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.phpVersionTextbox)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.phpPathTextbox = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.phpPathTextbox.setFont(font)
        self.phpPathTextbox.setText("")
        self.phpPathTextbox.setReadOnly(True)
        self.phpPathTextbox.setPlaceholderText("")
        self.phpPathTextbox.setObjectName("phpPathTextbox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.phpPathTextbox)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.phpIniPathTextbox = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.phpIniPathTextbox.setFont(font)
        self.phpIniPathTextbox.setText("")
        self.phpIniPathTextbox.setReadOnly(True)
        self.phpIniPathTextbox.setPlaceholderText("")
        self.phpIniPathTextbox.setObjectName("phpIniPathTextbox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.phpIniPathTextbox)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.logPathTextbox = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.logPathTextbox.setFont(font)
        self.logPathTextbox.setText("")
        self.logPathTextbox.setReadOnly(True)
        self.logPathTextbox.setPlaceholderText("")
        self.logPathTextbox.setObjectName("logPathTextbox")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.logPathTextbox)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.composerStatusTextbox = QtWidgets.QLineEdit(self.centralwidget)
        self.composerStatusTextbox.setReadOnly(True)
        self.composerStatusTextbox.setObjectName("composerStatusTextbox")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.composerStatusTextbox)
        self.verticalLayout_6.addLayout(self.formLayout_2)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(7)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.viewLogBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.viewLogBtn.setFont(font)
        self.viewLogBtn.setObjectName("viewLogBtn")
        self.verticalLayout_7.addWidget(self.viewLogBtn)
        self.phpInfoBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.phpInfoBtn.setFont(font)
        self.phpInfoBtn.setObjectName("phpInfoBtn")
        self.verticalLayout_7.addWidget(self.phpInfoBtn)
        self.manageExtBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.manageExtBtn.setFont(font)
        self.manageExtBtn.setObjectName("manageExtBtn")
        self.verticalLayout_7.addWidget(self.manageExtBtn)
        self.configBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.configBtn.setFont(font)
        self.configBtn.setObjectName("configBtn")
        self.verticalLayout_7.addWidget(self.configBtn)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_7.addWidget(self.checkBox)
        self.verticalLayout_6.addLayout(self.verticalLayout_7)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PHP windows installer"))
        self.label.setText(_translate("MainWindow", "Available PHP versions:"))
        self.loadBtn.setText(_translate("MainWindow", "Load"))
        self.installBtn.setText(_translate("MainWindow", "Install"))
        self.withTScheckBox.setText(_translate("MainWindow", "With thread safe"))
        self.label_2.setText(_translate("MainWindow", "Installed PHP versions:"))
        self.removeBtn.setText(_translate("MainWindow", "Delete"))
        self.useBtn.setText(_translate("MainWindow", "Use"))
        self.label_4.setText(_translate("MainWindow", "PHP Setup::"))
        self.label_3.setText(_translate("MainWindow", "Version"))
        self.label_5.setText(_translate("MainWindow", "Path"))
        self.label_6.setText(_translate("MainWindow", "Configuration file"))
        self.label_7.setText(_translate("MainWindow", "Error log"))
        self.label_8.setText(_translate("MainWindow", "Composer Status"))
        self.viewLogBtn.setText(_translate("MainWindow", "Open log file"))
        self.phpInfoBtn.setText(_translate("MainWindow", "phpinfo()"))
        self.manageExtBtn.setText(_translate("MainWindow", "Manage extensions"))
        self.configBtn.setText(_translate("MainWindow", "Open php.ini file"))
        self.checkBox.setText(_translate("MainWindow", "Update composer setting"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


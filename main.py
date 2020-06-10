from tools import *
from PyQt5 import QtWidgets, uic, QtGui
import sys
from PyQt5.Qt import QStandardItemModel, QStandardItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'design.ui'))

URL = 'https://windows.php.net/downloads/releases/archives/'

class StandardItem(QStandardItem):
    def __init__(self, txt="", font_size=10, set_bold=False, color=QtGui.QColor(0,0,0)):
        super().__init__()

        fnt = QtGui.QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)

class MainWindow(QtWidgets.QMainWindow, FORM_CLASS):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.loadBtn.clicked.connect(self.load)
        self.installBtn.clicked.connect(self.install)
        self.removeBtn.clicked.connect(self.remove)
        self.useBtn.clicked.connect(self.use)

        for i in installedPHP:
            self.installedVesionList.addItem(i)


        currentSetup = currentConfig()

        self.phpVersionTextbox.setText(currentSetup['version'])
        self.phpPathTextbox.setText(currentSetup['ini_path'][:-7])
        self.phpIniPathTextbox.setText(currentSetup['ini_path'])


    def load(self):
        links = extractLinks(URL)
        releases = clearData(links, self.latestPatchcheckBox.isChecked())

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        for name, group in releases.items():
            version = StandardItem("PHP " + name)
            version.setSelectable(False)
            rootNode.appendRow(version)

            for n, v in group:
                r = StandardItem(n)
                version.appendRow(r)

        self.phpVersionsTreeView.setModel(treeModel)
        # self.phpVersionsTreeView.expandAll()
        self.phpVersionsTreeView.setHeaderHidden(True)
        self.statusbar.showMessage('100%', 2000)

    def install(self):
        if self.phpVersionsTreeView.selectedIndexes():
            name = self.phpVersionsTreeView.selectedIndexes()[0].data()
            if any(name in s for s in installedPHP):
                self.statusbar.showMessage('This package is already installed', 2000)
                return
            download('{}{}.zip'.format(URL, name), name)
            self.statusbar.showMessage('Done!', 2000)
            self.installedVesionList.addItem(name) 
        else:
            self.statusbar.showMessage('Please select a package first', 2000)
    
    def remove(self):
        if self.installedVesionList.currentItem():
            remove(self.installedVesionList.currentItem().text())
            self.installedVesionList.takeItem(self.installedVesionList.currentRow())
        else:
            self.statusbar.showMessage('Please select the installed package you want to delete', 2000)

    def use(self):
        if self.installedVesionList.currentItem():
            cleanPath()
            path = os.path.join(os.getcwd(), installDir, self.installedVesionList.currentItem().text())
            manage_registry_env_vars('+PATH', path)
            self.statusbar.showMessage('Updated', 2000)
        else:
            self.statusbar.showMessage('Please select the installed package you want to install', 2000)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
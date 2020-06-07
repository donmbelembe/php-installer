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
    def load(self):
        links = extractLinks(URL)
        releases = clearData(links, self.latestPatchcheckBox.isChecked())

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        for name, group in releases:
            version = StandardItem("PHP " + name)
            version.setSelectable(False)
            rootNode.appendRow(version)

            for index, serie in group.iterrows():
                r = StandardItem(serie["path"])
                version.appendRow(r)
        self.phpVersionsTreeView.setModel(treeModel)
        # self.phpVersionsTreeView.expandAll()
        self.phpVersionsTreeView.setHeaderHidden(True)
        self.statusbar.showMessage('100%', 2000)

    def install(self):
        if self.phpVersionsTreeView.selectedIndexes():
            name = self.phpVersionsTreeView.selectedIndexes()[0].data()
            download('{}{}.zip'.format(URL, name), name)
            self.statusbar.showMessage('Done!', 2000)
        else:
            self.statusbar.showMessage('Please select a package first', 2000)

# app = QtWidgets.QApplication(sys.argv)
# window = MainWindow()
# app.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
from tools import *
from PyQt5 import QtWidgets, uic, QtGui
import sys
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QUrl, pyqtSlot
from fileLoader import DownLoader

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
        self.progressBar = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.hide()

        # This is simply to show the bar
        self.progressBar.setGeometry(30, 40, 200, 25)

        self.filename = None

        self.versionsDownloader = DownLoader()
        self.versionsDownloader.downloaded.connect(self.versionsDownloaderResponse)
        self.phpDownLoader = DownLoader()
        self.phpFileName = None
        self.phpDownLoader.downloaded.connect(self.phpDownLoaderResponse)
        self.phpDownLoader.downloadProgress.connect(self.phpDownLoaderProgress)

        for i in installedPHP:
            self.installedVesionList.addItem(i)


        currentSetup = currentConfig()

        self.phpVersionTextbox.setText(currentSetup['version'])
        self.phpPathTextbox.setText(currentSetup['ini_path'][:-7])
        self.phpIniPathTextbox.setText(currentSetup['ini_path'])

        self.loadBtn.clicked.connect(self.load)
        self.installBtn.clicked.connect(self.install)
        self.removeBtn.clicked.connect(self.remove)
        self.useBtn.clicked.connect(self.use)
        self.configBtn.clicked.connect(lambda: os.startfile(currentSetup['ini_path']))
        self.browseBtn.clicked.connect(lambda: os.startfile(currentSetup['ini_path'][:-7]))

    def load(self):
        self.statusbar.showMessage('Loading PHP installations list...1%', 20000)
        self.versionsDownloader.doDownload(QUrl(URL))
        
    def versionsDownloaderResponse(self):
        HTML = str(self.versionsDownloader.downloadedData(), encoding='utf-8')
        links = extractLinks(HTML)
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
        self.statusbar.showMessage('Loading PHP installations list...100%', 2000)

    def phpDownLoaderResponse(self):
        self.progressBar.hide()
        self.statusbar.showMessage('Unzipping...', 20000)
        saveFile(self.phpDownLoader.downloadedData(), self.phpFileName)
        self.statusbar.showMessage('Done!', 2000)
        self.installedVesionList.addItem(self.phpFileName) 

    @pyqtSlot(int, int)
    def phpDownLoaderProgress(self, downloaded, total):
        percent = int(downloaded*100/total)
        self.statusbar.showMessage('Installing {}: {}%'.format(self.phpFileName, percent), 20000)
        self.progressBar.setValue(percent)

    def install(self):
        if self.phpVersionsTreeView.selectedIndexes():
            self.phpFileName = self.phpVersionsTreeView.selectedIndexes()[0].data()
            if any(self.phpFileName in s for s in installedPHP):
                self.alert('Attention', 'This package is already installed')
                return

            packageInfo = getPHPPackageInfoFromString(self.phpFileName)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setText("Do you want to install {}?".format(self.phpFileName))
            if not packageInfo['nts']:
                msgBox.setInformativeText("It is recommanded to use NTS (non-thread safe) binaries unless you know what you are doing")
            installButton = msgBox.addButton("Install", QtWidgets.QMessageBox.ActionRole)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(installButton)
            msgBox.setEscapeButton(QtWidgets.QMessageBox.Cancel)
            msgBox.exec()

            if msgBox.clickedButton() == installButton:
                self.progressBar.show()
                self.phpDownLoader.doDownload(QUrl('{}{}.zip'.format(URL, self.phpFileName)))
        else:
            self.alert('Attention', 'You must select an available PHP version in the list first')
    
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

    def alert(self, title, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
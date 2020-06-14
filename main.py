from tools import *
from PyQt5 import QtWidgets, uic, QtGui
import sys
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, QThread
from workers import loadPhpBinaryListWorker, phpBinaryDownloaderWorker
from hurry.filesize import size, alternative


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'design.ui'))

installDir = "PHP"
URL = 'https://windows.php.net/downloads/releases/archives/'
installedPHP = list(filter(lambda x: os.path.isdir(os.path.join(installDir, x)), os.listdir(installDir)))

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
    EXIT_CODE_REBOOT = -12345678

    def __init__(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.progressBar = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.hide()
        self.progressBar.setGeometry(30, 40, 200, 25)
        self.phpVersionsTreeView.setHeaderHidden(True)
        self.latestPatchcheckBox.stateChanged.connect(lambda: self.updatePhpVersionsTreeView())

        self.filename = None

        for i in installedPHP:
            self.installedVesionList.addItem(i)

        currentSetup = currentConfig()
        self.availableReleases = list()

        self.phpVersionTextbox.setText(currentSetup['version'])
        self.phpPathTextbox.setText(currentSetup['ini_path'][:-7])
        self.phpIniPathTextbox.setText(currentSetup['ini_path'])

        self.loadBtn.clicked.connect(self.load)
        self.installBtn.clicked.connect(self.install)
        self.removeBtn.clicked.connect(self.remove)
        self.useBtn.clicked.connect(self.use)
        self.configBtn.clicked.connect(lambda: os.startfile(currentSetup['ini_path']))
        self.browseBtn.clicked.connect(lambda: os.startfile(currentSetup['ini_path'][:-7]))

        # create Worker and Thread inside the Form
        # Load list PHP
        self.loadPhpBinaryListThread = QThread()
        self.loadingObj = loadPhpBinaryListWorker(URL)
        self.loadingObj.resp.connect(self.versionsDownloaderResponse)
        self.loadingObj.moveToThread(self.loadPhpBinaryListThread)
        self.loadingObj.finished.connect(self.loadPhpBinaryListThread.quit)
        self.loadPhpBinaryListThread.started.connect(self.loadingObj.getList)
        # 
        self.phpBinaryDownloaderThread = QThread()
        self.phpBinaryDownloaderObj = phpBinaryDownloaderWorker(URL)
        self.phpBinaryDownloaderObj.resp.connect(self.phpBinaryInstallationDone)
        self.phpBinaryDownloaderObj.progress.connect(self.phpDownLoaderProgress)
        self.phpBinaryDownloaderObj.moveToThread(self.phpBinaryDownloaderThread)
        self.phpBinaryDownloaderObj.finished.connect(self.phpBinaryDownloaderThread.quit)
        self.phpBinaryDownloaderThread.started.connect(self.phpBinaryDownloaderObj.download)

    def load(self):
        self.toggleButton(False)
        self.statusbar.showMessage('Loading PHP installations list...', 20000)
        self.loadPhpBinaryListThread.start()

    @pyqtSlot(list) 
    def versionsDownloaderResponse(self, releases):
        self.availableReleases = releases
        self.updatePhpVersionsTreeView()
        self.statusbar.showMessage('Done!', 2000)
        self.toggleButton(True)

    def updatePhpVersionsTreeView(self):
        if len(self.availableReleases):
            data = self.loadingObj.groupByMinorRelease(self.availableReleases, self.latestPatchcheckBox.isChecked())
            treeModel = QStandardItemModel()
            rootNode = treeModel.invisibleRootItem()

            for name, group in data.items():
                version = StandardItem("PHP " + name)
                version.setSelectable(False)
                rootNode.appendRow(version)

                for n, v in group:
                    r = StandardItem(n)
                    version.appendRow(r)

            self.phpVersionsTreeView.setModel(treeModel)

    def install(self):
        if self.phpVersionsTreeView.selectedIndexes():
            name = self.phpVersionsTreeView.selectedIndexes()[0].data()
            if any(name in s for s in installedPHP):
                self.alert('Attention', 'This package is already installed')
                return

            packageInfo = getPHPPackageInfoFromString(name)
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setText("Do you want to install {}?".format(name))
            if not packageInfo['nts']:
                msgBox.setInformativeText("It is recommanded to use NTS (non-thread safe) binaries unless you know what you are doing")
            installButton = msgBox.addButton("Install", QtWidgets.QMessageBox.ActionRole)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(installButton)
            msgBox.setEscapeButton(QtWidgets.QMessageBox.Cancel)
            msgBox.exec()

            if msgBox.clickedButton() == installButton:
                self.toggleButton(False)
                self.progressBar.show()
                self.phpBinaryDownloaderObj.setPkg(name)
                self.phpBinaryDownloaderThread.start()
        else:
            self.alert('Attention', 'You must select an available PHP version in the list first')
    
    @pyqtSlot(str, int)
    def phpBinaryInstallationDone(self, name, timelapse):
        self.progressBar.hide()
        self.toggleButton(True)
        self.statusbar.showMessage('{} installed successfully in {} ms'.format(name, timelapse), 2000)
        self.installedVesionList.addItem(name) 
        os.startfile('post-install.txt')

    @pyqtSlot(str, int, int)
    def phpDownLoaderProgress(self, name, done, bps):
        speed = 'Speed: ' + size(bps, system=alternative) + '/S'
        self.statusbar.showMessage('{} | {}'.format(name, speed), 20000)
        self.progressBar.setValue(done)

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
            QtWidgets.qApp.exit(MainWindow.EXIT_CODE_REBOOT)
        else:
            self.statusbar.showMessage('Please select the installed package you want to install', 2000)

    def alert(self, title, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec()

    def toggleButton(self, state):
        self.installBtn.setEnabled(state)
        self.loadBtn.setEnabled(state)

if __name__ == "__main__":
    currentExitCode = MainWindow.EXIT_CODE_REBOOT
    while currentExitCode == MainWindow.EXIT_CODE_REBOOT:
        a = QtWidgets.QApplication(sys.argv)
        w = MainWindow()
        w.show()
        currentExitCode = a.exec_()
        a = None  # delete the QApplication object

    sys.exit(currentExitCode)
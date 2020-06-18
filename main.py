from pyuac import isUserAdmin, runAsAdmin
from tools import *
from PyQt5 import QtWidgets, uic, QtGui
import sys
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, QThread
from workers import LoadPhpBinaryListWorker, PhpBinaryDownloaderWorker, UpdatePATHWorker
from hfilesize import FileSize
import traceback
import logging
logging.basicConfig(filename=log_file,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
logger = logging.getLogger('php-installer')
# handler = logging.FileHandler('php-installer.log')
# logger.addHandler(handler)

def log_exception(exc_type, exc_value, exc_traceback):
    logger.error("Uncaught exception occurred!",
                 exc_info=(exc_type, exc_value, exc_traceback))
    
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            logger.error(repr(line))


def attach_hook(hook_func, run_func):
    def inner(*args, **kwargs):
        if not (args or kwargs):
            # This condition is for sys.exc_info
            local_args = run_func()
            hook_func(*local_args)
        else:
            # This condition is for sys.excepthook
            hook_func(*args, **kwargs)
        return run_func(*args, **kwargs)
    return inner

if getattr(sys, 'frozen', False):
    # frozen
    dir_ = os.path.dirname(sys.executable)
else:
    # unfrozen
    dir_ = os.path.dirname(os.path.realpath(__file__))

FORM_CLASS, _ = uic.loadUiType(os.path.join(dir_, 'design.ui'))

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
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('PHP installer for windows - 2.0')
        self.progressBar = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.hide()
        self.progressBar.setGeometry(30, 40, 200, 25)
        self.phpVersionsTreeView.setHeaderHidden(True)
        self.latestPatchcheckBox.stateChanged.connect(lambda: self.updatePhpVersionsTreeView())

        self.filename = None

        for i in installedPHP:
            self.installedVesionList.addItem(i)

        self.currentSetup = currentConfig()
        self.availableReleases = list()

        if self.currentSetup:
            self.displayCurrentConfig()

        self.loadBtn.clicked.connect(self.load)
        self.installBtn.clicked.connect(self.install)
        self.removeBtn.clicked.connect(self.remove)
        self.useBtn.clicked.connect(self.use)
        self.configBtn.clicked.connect(lambda: os.startfile(self.currentSetup['ini_path']))
        self.browseBtn.clicked.connect(lambda: os.startfile(self.currentSetup['ini_path'][:-7]))

        # create Worker and Thread inside the Form
        # Load list PHP
        self.loadPhpBinaryListThread = QThread()
        self.loadingObj = LoadPhpBinaryListWorker(URL)
        self.loadingObj.resp.connect(self.versionsDownloaderResponse)
        self.loadingObj.moveToThread(self.loadPhpBinaryListThread)
        self.loadingObj.finished.connect(self.loadPhpBinaryListThread.quit)
        self.loadPhpBinaryListThread.started.connect(self.loadingObj.getList)
        # Download binary
        self.phpBinaryDownloaderThread = QThread()
        self.phpBinaryDownloaderObj = PhpBinaryDownloaderWorker(URL)
        self.phpBinaryDownloaderObj.resp.connect(self.phpBinaryInstallationDone)
        self.phpBinaryDownloaderObj.progress.connect(self.phpDownLoaderProgress)
        self.phpBinaryDownloaderObj.moveToThread(self.phpBinaryDownloaderThread)
        self.phpBinaryDownloaderObj.finished.connect(self.phpBinaryDownloaderThread.quit)
        self.phpBinaryDownloaderThread.started.connect(self.phpBinaryDownloaderObj.download)
        # Download binary
        self.updatePathThread = QThread()
        self.updatePathObj = UpdatePATHWorker()
        self.updatePathObj.moveToThread(self.updatePathThread)
        self.updatePathObj.finished.connect(self.pathUpdated)
        self.updatePathThread.started.connect(self.updatePathObj.update)
    
    def displayCurrentConfig(self):
        if isinstance(self.currentSetup, str):
            text = '''
                <html><head/><body>
                    <h4>PHP Says:</h4>
                    <p><span style=" color:#ff0000;">'''+self.currentSetup+'''</span></p>
                    <p>Note: You probably nedd to install Microsoft Visual C++ Redistributable for Visual Studio (vc15, vc14,...) please check
                    <a href="https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads">this link</a></p>
                </body></html>'''
            self.warningLabel.setText(text)
            self.phpVersionTextbox.setText('')
            self.phpPathTextbox.setText('')
            self.phpIniPathTextbox.setText('')
        else:
            self.warningLabel.setText('')
            self.phpVersionTextbox.setText(self.currentSetup['version'])
            self.phpPathTextbox.setText(self.currentSetup['ini_path'][:-7])
            self.phpIniPathTextbox.setText(self.currentSetup['ini_path'])

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
        self.progressBar.setValue(0)
        self.toggleButton(True)
        self.statusbar.showMessage('{} installed successfully in {} ms'.format(name, timelapse), 2000)
        self.installedVesionList.addItem(name) 
        os.startfile('post-install.txt')

    @pyqtSlot(str, int, int)
    def phpDownLoaderProgress(self, name, done, bps):
        speed = 'Speed: ' + '{:.02fH}'.format(FileSize(bps)) + '/S'
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
            name = self.installedVesionList.currentItem().text()
            path = os.path.join(os.getcwd(), installDir, name)
            self.updatePathObj.setPathToAdd(path)
            self.updatePathThread.start()
        else:
            self.statusbar.showMessage('Please select the installed package you want to install', 2000)

    def pathUpdated(self):
        self.updatePathThread.quit()
        self.statusbar.showMessage('Success', 2000)
        self.currentSetup = currentConfig()
        self.displayCurrentConfig()

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
    rc = 0
    if not isUserAdmin():
        rc = runAsAdmin()
        sys.exit(rc)

    sys.exc_info = attach_hook(log_exception, sys.exc_info)
    sys.excepthook = attach_hook(log_exception, sys.excepthook)
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
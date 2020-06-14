# https://stackoverflow.com/a/33453124/6210398
import threading
import sys
from requests import get as requests_get
from zipfile import ZipFile
import os
from shutil import copyfile
from bs4 import BeautifulSoup
from packaging.version import Version, parse
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import time


class loadPhpBinaryListWorker(QObject):
  finished = pyqtSignal()
  resp = pyqtSignal(list)

  def __init__(self, URL):
    super().__init__()
    self.URL = URL

  def extractLinks(self, HTML):
    soup = BeautifulSoup(HTML, 'html.parser')

    links = soup.find_all('a')
    links = [link.get('href').split('/')[-1] for link in links]
    return links

  def filterWindowsItems(self, data):
    data = [d for d in data if "Win" in d and d.endswith(".zip")]
    # remove .zip at the end     
    data = [d[:-4] for d in data]
    # transform to list of name, version
    newList = list()
    for i, d in enumerate(data):
        newList.append((d, d.split("-")[1]))
    # only keep those who have valid version
    newList = [i for i in newList if isinstance(parse(i[1]), Version)]
    # add minor version
    for i, d in enumerate(newList):
        newList[i] = d[0], d[1], "{}.{}".format(parse(d[1]).major,parse(d[1]).minor)
    return newList

  @staticmethod
  def groupByMinorRelease(data, patch):
      # group by minor version
      Output = {} 
      for x, y, z in data: 
        if z in Output: 
          if patch:
              if parse(y) == parse(Output[z][0][1]):
                  Output[z].append((x, y)) 
              elif parse(y) > parse(Output[z][0][1]):
                  Output[z] = [(x, y)]
          else:
              Output[z].append((x, y)) 
        else: 
            Output[z] = [(x, y)]
      return Output

  @pyqtSlot()
  def getList(self):
    response  = requests_get(self.URL)
    links = self.extractLinks(response.text)
    releases = self.filterWindowsItems(links)
    self.resp.emit(releases)
    self.finished.emit()

class phpBinaryDownloaderWorker(QObject):
  finished = pyqtSignal()
  resp = pyqtSignal(str)
  progress = pyqtSignal(str, int, int)

  def __init__(self, URL):
    super().__init__()
    self.URL = URL
    self.pkg = None

  def setPkg(self, pkg):
    self.pkg = pkg

  @pyqtSlot()
  def download(self):
    if self.pkg:
      url = '{}{}.zip'.format(self.URL, self.pkg)
      storagePath = 'PHP/' + self.pkg
      with open(storagePath + '.zip', 'wb') as f:
        start = time.process_time()
        response  = requests_get(url, stream=True)

        total_length = response.headers.get('content-length')
        dl = 0

        if total_length is None: # no content length header
          f.write(response.content)
        else:
          total_length = int(total_length)
          for chunk in response.iter_content(chunk_size = 4096):
              dl += len(chunk)
              f.write(chunk)
              done = int(100 * dl / total_length)
              # byte per seconds
              bps = dl//(time.process_time() - start)
              self.progress.emit(self.pkg, done, bps)

      with ZipFile(storagePath + '.zip', 'r') as zip_ref:
        zip_ref.extractall(storagePath)

      os.remove(storagePath + '.zip')
      copyfile(storagePath + '/php.ini-development', storagePath + '/php.ini')
    self.resp.emit(self.pkg)
    self.finished.emit()

import sys
import os

from PySide6 import QtUiTools, QtGui
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import win32api
import tkinter.messagebox as msgbox
import schedule
import time
import threading
import pickle

"""
pip install schedule
pip install Pyside6
pip install selenium
pip install pywin32      ## win32api
"""


global ep_Id, ep_pw, sdp_id, sdp_pw, prj

ep_Id = 'hyunho.bae'
ep_pw = 'karsian!23'
sdp_id = 'A80210'
sdp_pw = 'lge123'
prj ="WEEPPDEV"



# 파일 경로
# pyinstaller로 원파일로 압축할때 경로 필요함
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)




class MainView(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.lastNum = 1
        self.jiraCheckUrl = "http://hlm.lge.com/issue/projects/WEEPPDEV/issues?filter=allopenissues&orderby=created+DESC%2C+priority+DESC%2C+updated+DESC"
        self.setupUI()
        self.show()

    def setupUI(self):
        global UI_set
        UI_set = QtUiTools.QUiLoader().load(resource_path("C:\Python311\Lib\site-packages\PySide6\WEEPP 운영 Tool main.ui"))
        self.setCentralWidget(UI_set)
        self.setWindowTitle("WEE 통합 도구")
        self.setWindowIcon(QtGui.QPixmap(resource_path("./images/jbmpa.png")))
        self.setFixedSize(QSize(850, 550))
        UI_set.logPageBtn.clicked.connect(lambda : self.pageChange("selectServerForLog"))
        UI_set.JiraPageBtn.clicked.connect(lambda : self.pageChange("test"))
        menubar =self.menuBar()
        self.mainMenuBar = self.menuBar()
        self.show()

    def pageChange(self,page):
        # self.hide()
        ui_set = QtUiTools.QUiLoader().load(resource_path("C:\Python311\Lib\site-packages\PySide6\{0}.ui".format(page)))
        self.page_event_connect(ui_set, page)
        self.setCentralWidget(ui_set)
        self.setWindowTitle("WEE 통합 도구")
        self.setWindowIcon(QtGui.QPixmap(resource_path("./images/jbmpa.png")))
        self.setFixedSize(QSize(850, 550))
        # self.show()

    def page_event_connect(self,ui_set,page):
        match page:
            case "jiraPage":
                ui_set.debugChromeOpenBtn.clicked.connect(lambda: self.openDebbugChrome())
                ui_set.EnterEpCount.clicked.connect(lambda: self.enter_ep_account())
                ui_set.jiraCheckingBtn.clicked.connect(lambda: self.create_jira_thread())
            case "selectServerForLog":
                ui_set.webviewerBtn.clicked.connect(lambda: self.openDebbugChrome())
                #개발 서버
                ui_set.debAcsLoginBtn.clicked.connect(lambda: self.openDebbugChrome())
                ui_set.devValutLoginBtn.clicked.connect(lambda: self.openDebbugChrome())
                ui_set.debWebLoginBtn.clicked.connect(lambda: self.openDebbugChrome())
                ui_set.devWasLoginBtn.clicked.connect(lambda: self.openDebbugChrome())
                #운영 서버

    def openDebbugChrome(self):
        #윈도우 명령어로 크롬 디벙깅 모드 실행
        win32api.WinExec('C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"')
        self.connecting_Chrome()
        #self.driver.get('http://newep.lge.com/')

    def connecting_Chrome(self):
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def enter_ep_account(self):
        self.driver.get('http://newep.lge.com/')
        self.driver.find_element(By.ID, 'USER').send_keys(ep_Id)
        self.driver.find_element(By.ID, 'LDAPPASSWORD').send_keys(ep_pw)
        otp = input("OTP 입력 \n")
        self.driver.find_element(By.ID, 'OTPPASSWORD').send_keys(otp)
        self.driver.find_element(By.ID, 'loginSsobtn').click()

    def check_jira(self):
        self.driver.get(self.jiraCheckUrl)
        print(datetime.now().strftime('%Y-%m-%d %H시 %M분 Checking...'))
        curNum = self.driver.find_element(By.ID, 'key-val').get_attribute('text').split('-')[1]
        if curNum > self.lastNum:
            print(datetime.now().strftime('%Y-%m-%d %H시 %M분 {}').format("신규 지라 감지"))
            msgbox.showinfo('신규 지라 알림', '신규 지라가 있습니다.')
    def create_jira_thread(self):
        thread_1 = threading.Thread(target=self.scheduling_jira)
        thread_1.start()
    def scheduling_jira(self):
        if not hasattr(self, 'driver'):
            self.connecting_Chrome()
            if not hasattr(self, 'driver'):
                return
        print('start Jira Checking')
        self.driver.get(self.jiraCheckUrl)
        self.lastNum = self.driver.find_element(By.ID, 'key-val').get_attribute('text').split('-')[1]
        schedule.every(5).minutes.do(self.check_jira)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':

    # 계정 설정 관련 변수
    accountInfo = ["acsId", "acsPw", "devPuttyId", "prodPuttyId", "devPuttyPw"
        , "prodPuttyPw", "adId", "adPw","sdpId","sdpPw"]
    settingEntryDic = {}

    a =[
        {
            "account" : [
                {"acsId": ""}
                ,{"acsPw": ""}
                , {"devPuttyId": ""}
                , {"prodPuttyId": ""}
                , {"devPuttyPw": ""}
                , {"prodPuttyPw": ""}
                , {"adId": ""}
                , {"adPw": ""}
                , {"sdpId": ""}
                , {"sdpPw": ""}
            ]
        },{
            "server": [
                {"devWebServer": "10.150.95.228"}
                , {"devWasServer": "10.150.95.229"}
                , {"prodWebServer1": "10.150.95.71"}
                , {"prodWebServer2": "10.150.95.91"}
                , {"gateWay": "10.150.133.119"}
                , {"prodWasServer1":"10.150.95.74"}
                , {"prodWasServer2": "10.150.95.94"}
            ]
        }
    ]
    # 계정설정 파일 경로
    accountPath = "autoAcsConfig.txt"

    # 계정 세팅 정보 read
    if os.path.isfile(accountPath):
        with open(accountPath, "rb") as setFile:
            setdata = pickle.load(setFile)
        for k, v in setdata.items():
            globals()[k] = v
    else:
        for a in accountInfo:
            globals()[a] = ""

    app = QApplication(sys.argv)
    main = MainView()
    main.show()
    sys.exit(app.exec())

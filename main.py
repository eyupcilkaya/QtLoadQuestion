import sys
import time
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import pandas as pd
import thread
import variables
import firebase_process

obj = variables.Variables()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("load.ui", self)
        self.toDevice = "Tüm Cihazlar"
        self.theQuestion = "Tüm Sorular"
        self.devices = firebase_process.getDevices()
        self.loadQuestion()
        self.send.clicked.connect(self.sendQuestion)
        self.finish.clicked.connect(self.runStateUpdate)
        obj.runstate = True
        self.show()

    # runState function includes stop thread process, clear database process and exit process
    def runStateUpdate(self):
        obj.runstate = False
        time.sleep(1)
        firebase_process.clearDatabase()
        sys.exit()

    # sendQuestion function checks options
    def sendQuestion(self):
        thread.generateThread(obj, self.devices)
        if (self.toDevice == "Tüm Cihazlar") & (self.theQuestion != "Tüm Sorular"):
            for device in self.devices:
                obj.setQuestion(device, [self.df.iloc[int(self.theQuestion) - 1][0],
                                         self.df.iloc[int(self.theQuestion) - 1][1],
                                         self.df.iloc[int(self.theQuestion) - 1][2],
                                         self.df.iloc[int(self.theQuestion) - 1][3],
                                         self.df.iloc[int(self.theQuestion) - 1][4],
                                         self.df.iloc[int(self.theQuestion) - 1][5],
                                         self.df.iloc[int(self.theQuestion) - 1][6]])

        elif (self.toDevice == "Tüm Cihazlar") & (self.theQuestion == "Tüm Sorular"):
            for device in self.devices:
                for i in range(len(self.df)):
                    obj.setQuestion(device, [self.df.iloc[i][0],
                                             self.df.iloc[i][1],
                                             self.df.iloc[i][2],
                                             self.df.iloc[i][3],
                                             self.df.iloc[i][4],
                                             self.df.iloc[i][5],
                                             self.df.iloc[i][6]])

        elif (self.toDevice != "Tüm Cihazlar") & (self.theQuestion == "Tüm Sorular"):
            print("tüm sorular")
            for i in range(len(self.df)):
                obj.setQuestion(self.toDevice, [self.df.iloc[i][0],
                                                self.df.iloc[i][1],
                                                self.df.iloc[i][2],
                                                self.df.iloc[i][3],
                                                self.df.iloc[i][4],
                                                self.df.iloc[i][5],
                                                self.df.iloc[i][6]])

        else:
            obj.setQuestion(self.toDevice, [self.df.iloc[int(self.theQuestion) - 1][0],
                                            self.df.iloc[int(self.theQuestion) - 1][1],
                                            self.df.iloc[int(self.theQuestion) - 1][2],
                                            self.df.iloc[int(self.theQuestion) - 1][3],
                                            self.df.iloc[int(self.theQuestion) - 1][4],
                                            self.df.iloc[int(self.theQuestion) - 1][5],
                                            self.df.iloc[int(self.theQuestion) - 1][6]])

    def loadQuestion(self):
        self.df = pd.read_excel("doc.xlsx")
        self.questionBox.addItem("Tüm Sorular")
        self.deviceBox.addItem("Tüm Cihazlar")
        for i in range(len(self.df)):
            self.questionBox.addItem(str(i + 1))
        for i in self.devices:
            self.deviceBox.addItem(str(i))

        self.questionBox.activated[str].connect(self.onActivatedQuestion)
        self.deviceBox.activated[str].connect(self.onActivatedDevice)

    def onActivatedQuestion(self, text):

        if (text == "Tüm Sorular"):
            self.theQuestion = text
            pass
        else:
            self.theQuestion = text
            self.question.setText(self.df["question"][(int(text)) - 1])
            self.a.setText(f"A) {self.df['a'][(int(text)) - 1]}")
            self.b.setText(f"B) {self.df['b'][(int(text)) - 1]}")
            self.c.setText(f"C) {self.df['c'][(int(text)) - 1]}")
            self.d.setText(f"D) {self.df['d'][(int(text)) - 1]}")
            self.e.setText(f"E) {self.df['e'][(int(text)) - 1]}")
            self.image.setStyleSheet(
                f'border-image : url({"image/" + self.df["image"][(int(text)) - 1]}) 0 0 0 0 strech strech')

    def onActivatedDevice(self, text):
        self.toDevice = text


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()

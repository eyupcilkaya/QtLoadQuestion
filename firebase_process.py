import time

import xlsxwriter
from pyrebase import pyrebase
import firebaseConfigFile
import xlwt
from xlwt import Workbook

firebase = pyrebase.initialize_app(firebaseConfigFile.firebaseConfig)
storage = firebase.storage()
db = firebase.database()

workbook = xlsxwriter.Workbook('Answer.xlsx')
worksheet = workbook.add_worksheet("Answer")


def writeFirebase(obj, device):
    i = 0
    j = 1
    worksheet.write(0, deviceNum.index(device), str(device))
    while obj.runstate:
        questionarray = obj.getQuestion(device)
        print(questionarray)

        if (db.child(f"state/{device}").get().val() == 0) & (len(questionarray) > i):
            print(i)

            answer = db.child(f"answers/{device}").get().val()
            print(answer)

            print(deviceNum.index(device))
            worksheet.write(j, deviceNum.index(device), str(answer))

            db.child(f"questions/{device}/question").set(questionarray[i][0])
            db.child(f"questions/{device}/a").set(questionarray[i][1])
            db.child(f"questions/{device}/b").set(questionarray[i][2])
            db.child(f"questions/{device}/c").set(questionarray[i][3])
            db.child(f"questions/{device}/d").set(questionarray[i][4])
            db.child(f"questions/{device}/e").set(questionarray[i][5])

            storage.child(f"{device}/1.jpg").put(f"image/{questionarray[i][6]}")
            db.child(f"state/{device}").set(1)

            i = i + 1
            j = j + 1

        else:
            time.sleep(0.5)
    print("yes")

    answer = db.child(f"answers/{device}").get().val()
    worksheet.write(j, deviceNum.index(device), str(answer))
    workbook.close()


def getDevices():
    dev = db.child("state/").get().val()
    return list(dev.keys())


def clearDatabase():
    db.child("state").remove()
    db.child("questions").remove()
    db.child("answers").remove()


deviceNum = getDevices()

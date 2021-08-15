import time
import xlsxwriter
from pyrebase import pyrebase
import firebaseConfigFile

# connect firebase
firebase = pyrebase.initialize_app(firebaseConfigFile.firebaseConfig)
storage = firebase.storage()
db = firebase.database()

# create excel file for answers
workbook = xlsxwriter.Workbook('Answer.xlsx')
worksheet = workbook.add_worksheet("Answer")


def writeFirebase(obj, device):
    i = 0
    j = 1
    # write device names to excel
    worksheet.write(0, deviceNum.index(device), str(device))
    # if runstate is true,
    while obj.runstate:
        questionarray = obj.getQuestion(device)

        if (db.child(f"state/{device}").get().val() == 0) & (len(questionarray) > i):

            # get last answer from firebase
            answer = db.child(f"answers/{device}").get().val()
            # write answer to excel
            worksheet.write(j, deviceNum.index(device), str(answer))

            # write question to firebase
            db.child(f"questions/{device}/question").set(questionarray[i][0])
            db.child(f"questions/{device}/a").set(questionarray[i][1])
            db.child(f"questions/{device}/b").set(questionarray[i][2])
            db.child(f"questions/{device}/c").set(questionarray[i][3])
            db.child(f"questions/{device}/d").set(questionarray[i][4])
            db.child(f"questions/{device}/e").set(questionarray[i][5])
            # load question image to firebase
            storage.child(f"{device}/1.jpg").put(f"image/{questionarray[i][6]}")
            # set question state
            db.child(f"state/{device}").set(1)

            i = i + 1
            j = j + 1

        else:
            time.sleep(0.5)

    answer = db.child(f"answers/{device}").get().val()
    worksheet.write(j, deviceNum.index(device), str(answer))
    workbook.close()


def getDevices():
    # get all devices from firebase
    dev = db.child("state/").get().val()
    return list(dev.keys())


def clearDatabase():
    # clear all database
    db.child("state").remove()
    db.child("questions").remove()
    db.child("answers").remove()


deviceNum = getDevices()

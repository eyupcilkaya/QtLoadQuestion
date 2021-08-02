import time
from pyrebase import pyrebase
import firebaseConfigFile

firebase = pyrebase.initialize_app(firebaseConfigFile.firebaseConfig)
storage = firebase.storage()
db = firebase.database()


def writeFirebase(obj, device):
    i = 0
    while True:
        questionarray = obj.getQuestion(device)
        print(questionarray)

        if (db.child(f"state/{device}").get().val() == 0) & (len(questionarray) > i):

            answer = db.child(f"answers/{device}").get().val()
            print(answer)

            db.child(f"questions/{device}/question").set(questionarray[i][0])
            db.child(f"questions/{device}/a").set(questionarray[i][1])
            db.child(f"questions/{device}/b").set(questionarray[i][2])
            db.child(f"questions/{device}/c").set(questionarray[i][3])
            db.child(f"questions/{device}/d").set(questionarray[i][4])
            db.child(f"questions/{device}/e").set(questionarray[i][5])

            storage.child(f"{device}/1.jpg").put(f"image/{questionarray[i][6]}")
            db.child(f"state/{device}").set(1)

            i = i + 1

        else:
            time.sleep(1)


def getDevices():
    dev = db.child("state/").get().val()
    return list(dev.keys())

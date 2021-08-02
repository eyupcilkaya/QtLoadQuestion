import threading
import firebase_process


def generateThread(obj,devices):
    for i in devices:
        obj.setQuestion(i,[])
        t = threading.Thread(target=firebase_process.writeFirebase, args=(obj,i,))
        t.start()

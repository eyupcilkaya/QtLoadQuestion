class Variables():
    def __init__(self):
        self.questions = {}
        self.runstate=True

    def setQuestion(self, device, quest):
        if device in self.questions.keys():
            self.questions[device].append(quest)
        else:
            self.questions[device]=quest

    def getQuestion(self, device):
        return self.questions[device]

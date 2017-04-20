class Notes:
    def __init__(self, main, noteList, noteCount):
        self.main = main
        self.noteList = noteList
        self.count = 1
        self.noteCount = noteCount
        self.value = ""
    def addCount(self):
        self.count += 1
    def printData(self):
        print "main = " + self.main
        for note in self.noteList:
            print "note = " + note
        print "count = " + repr(self.count)
        print "value = " + self.value + "\n"

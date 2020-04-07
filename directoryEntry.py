class DirectoryEntry:
    def __init__(self, tagIDArray, tagTypeArray, countArray, offsetArray):
        self.tagIDArray = tagIDArray
        self.tagTypeArray = tagTypeArray
        self.countArray = countArray
        self.offsetArray = offsetArray

    def getOffset(self):
        offset = int((self.offsetArray[3] | (self.offsetArray[2]<<8) | (self.offsetArray[1]<<16) | (self.offsetArray[0]<<24)))
        return offset

    def getCount(self):
        count = int((self.countArray[3] | (self.countArray[2]<<8) | (self.countArray[1]<<16) | (self.countArray[0]<<24)))
        return count

    def getDEsize(self):
        tagTypeNumber = self.tagTypeArray[1] | (self.tagTypeArray[0]<<8)

        if(tagTypeNumber == 1 or 
            tagTypeNumber == 2 or 
            tagTypeNumber == 6 or
            tagTypeNumber == 7):
            return 1
        elif(tagTypeNumber == 3 or
            tagTypeNumber == 8):
            return 2
        elif(tagTypeNumber == 4 or
            tagTypeNumber == 9 or
            tagTypeNumber == 11 or
            tagTypeNumber == 13):
            return 4
        elif(tagTypeNumber == 5 or
            tagTypeNumber == 10 or
            tagTypeNumber == 12):
            return 8

    def getDataLength(self):
        size = self.getDEsize()
        count = self.getCount()

        return size*count

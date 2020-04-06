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

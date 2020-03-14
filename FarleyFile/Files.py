import os


class Files():

    def __init__(self):
        'Initialization'
        self.directory = 'files'

    def getFileNames(self):
        'gets a list of filenames'
        fileNames = os.listdir(self.directory)
        fileNames.remove('.gitignore')
        return fileNames

    def getNextFileID(self):
        'gets the next expected fileID'
        def getID(fileName):
            pieces = fileName.split('.')
            return int(pieces[0])
        fileIDs = list(map(getID, self.getFileNames()))
        fileIDs.sort()
        lastFileID = fileIDs.pop()
        return lastFileID + 1

    def getNextFileName(self):
        'gets the next expected fileName'
        return '{}.json'.format(self.getNextFileID())

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

    def getNextFileName(self):
        'gets the next expected fileName'
        lastFileName = self.getFileNames()
        #return lastFileName
        return 12

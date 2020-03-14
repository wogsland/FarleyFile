import os


class Files():
    def getFileNames(self):
        'gets a list of filenames'
        fileNames = os.listdir('files')
        fileNames.remove('.gitignore')
        return fileNames

    def getNextFileName(self):
        'gets the next expected fileName'
        print('wait')

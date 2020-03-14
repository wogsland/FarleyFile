from unittest import TestCase
from FarleyFile.Files import Files


class TestFiles(TestCase):

    def test_init(self):
        files = Files()

    def test_getFileNames(self):
        files = Files()
        fileNames = files.getFileNames()
        self.assertEqual(1, len(fileNames))
        self.assertEqual('1.json', fileNames[0])

    def test_getNextFileName(self):
        files = Files()
        nextFileName = files.getNextFileName()
        self.assertEqual('2.json', nextFileName)

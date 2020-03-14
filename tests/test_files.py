from unittest import TestCase
from FarleyFile import Files


class TestFiles(TestCase):

    def test_getFileNames(self):
        print('test')
        files = new Files()
        fileNames = files.getFileNames()
        self.assertEqual(1, len(fileNames))
        self.assertEqual('1.json', fileNames[0])

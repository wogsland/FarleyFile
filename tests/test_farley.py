from unittest import TestCase
import farley


class TestFarley(TestCase):

    def test_getFileNames(self):
        fileNames = farley.getFileNames()
        self.assertEqual(1, len(fileNames))
        self.assertEqual('1.json', fileNames[0])

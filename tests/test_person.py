from unittest import TestCase
from FarleyFile.Person import Person


class TestPerson(TestCase):

    def test_init(self):
        person = Person(1)
        self.assertNotEqual(person.json, None)
        self.assertEqual('files/1.json', person.fileName)

    def test_email(self):
        person = Person(1)
        email = 'peter.parker@gmail.com'
        person.addEmail(email)
        self.assertEqual(1, len(person.json['emails']))
        email2 = 'pparker@oscorp.biz'
        person.addEmail(email2)
        self.assertEqual(2, len(person.json['emails']))
        self.assertEqual(person.json['emails'][0], email)
        self.assertEqual(person.json['emails'][1], email2)

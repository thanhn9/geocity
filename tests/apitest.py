import unittest
import requests
import json

class TestGeocityMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print '**Hello world!!'
        cls.url = 'http://localhost:5000/'
        cls.geonameid = '2932924' 

    def test_100_serverup(self):
        r = requests.get(self.url)
        self.assertEqual(r.status_code, 200, r.content)

    def test_110_getone(self):
        '''
        Test sample to retrieve a single city profile with its id.
        '''
        r = requests.get(self.url + self.geonameid)
        self.assertEqual(r.status_code, 200, r.content)
        js = json.loads(r.content)
        self.assertEqual(js.get('name'), 'Ehingen')
        self.assertEqual(js.get('admin3_code'), '08425')

    def test_120_longitude(self):
        r = requests.get(self.url + self.geonameid + '/longitude')
        self.assertEqual(r.status_code, 200, r.content)
        js = json.loads(r.content)
        self.assertEqual(js, '9.72749')

    def test_120_latitude(self):
        r = requests.get(self.url + self.geonameid + '/latitude')
        self.assertEqual(r.status_code, 200, r.content)
        js = json.loads(r.content)
        self.assertEqual(js, '48.28259')

    @classmethod
    def tearDownClass(cls):
        print "**Bye world!!"
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)

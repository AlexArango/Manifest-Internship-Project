import unittest

import ManifestProject

class MyTests(unittest.TestCase):
    def testfindColumnNumberSuccess(self):
       testData = [
           ['id', 'title', 'description', 'category', 'google_product_category', 'link', 'image_link', 'price'],
       ]
       result = ManifestProject.find_column_number('price', testData)
       self.assertTrue(result, msg = "Find column number is supposed to be the right column number price is found in")

    def testfindColumnNumberFail(self):
       testData = [
           ['id', 'title', 'description', 'category', 'google_product_category', 'link', 'image_link'],
       ]
       result = ManifestProject.find_column_number('price', testData)
       self.assertFalse(result, msg = "Find column number is supposed to be the right column number price is found in")
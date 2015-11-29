import unittest
import app

class TestDemo(unittest.TestCase):
  def setUp(self):
    print "Before a test"
  
  def tearDown(self):
    print "After a test"
  
  #define the test for whoQuery by comparing whether the string matches a possible answer.
  def testWho(self):
    r = app.whoSearch("Who is the lead singer in Radiohead?")
    self.assertEqual(r[0], "Thom Yorke")
    
  #define the test for whenQuery by comparing whether the string matches a possible answer.
  def testWhen(self):
    r = app.whenSearch("When is Christmas?")
    self.assertEqual(r[0], "25/12/2014")
    
if __name__ == "__main__":

  suite = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
  
  # 0 (quiet): you just get the total numbers of tests executed and the global result
  # 1 (default): you get the same plus a dot for every successful test or a F for every failure
  # 2 (verbose): you get the help string of every test and the result
  unittest.TextTestRunner(verbosity=2).run(suite)

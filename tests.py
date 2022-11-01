import unittest
import sys
import program.events as events

class TestStringMethods(unittest.TestCase):
    def test_getMinutesToNextEvent(self):
        event = dict(                    
            name="Evening",
            timeInMin = 1230,
            timeStr = "20:30",
            color = "ebb63e",
            brightness = 10,
            lamps = ["65546"])
        minutesToNextEvent = events.getsMinutesToNextEvent(event)
        print(minutesToNextEvent, " fesfes")

if __name__ == '__main__':
    unittest.main()
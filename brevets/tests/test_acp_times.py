"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging
#import sys
#sys.path.append('../brevets')
from acp_times import open_time, close_time
from flask_brevets import storageMongo, display_data
import arrow
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_first():
    assert  open_time(200, 200, arrow.now()) == arrow.now().shift(hours = 200/34)
    assert  close_time(200, 200, arrow.now()) == arrow.now().shift(hours = 200/15)

def test_greater():
    assert open_time(205, 200, arrow.now()) == arrow.now().shift(hours = 200/34)

def test_less():
    assert open_time(190, 200, arrow.now()) == arrow.now().shift(hours = 190/34)

def test_bigger():
    assert open_time(300, 300, arrow.now()) == arrow.now().shift(hours = (200/34+100/32))

def test_eBigger():
    assert open_time(600, 600, arrow.now()) == arrow.now().shift(hours = (200/34+200/32+200/30))

def test_store():
    assert storageMongo("controls", 200, "2023-01-01T00:00")

def test_open():
    assert display_data()

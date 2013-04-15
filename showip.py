#!/usr/bin/python


from Adafruit_ADS1x15 import ADS1x15
import time, math
import datetime
from Adafruit_8x8 import EightByEight
import Adafruit_LEDBackpack
from subprocess import *
from time import sleep, strftime
from datetime import datetime
from Alpha8x8 import Alpha8x8

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
grid = EightByEight(address=0x70)
led = Adafruit_LEDBackpack.LEDBackpack(0x70)
led.setBrightness=1

print "Press CTRL+C to exit"

display=0

cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
 
def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

ip = run_cmd(cmd)

def type(theString):
  for i in theString.strip():
    print "Showing %s" % str(i)
    show(i)

def show(letter):
  grid.clear()
  for i in Alpha8x8.letters[letter]:
    grid.setPixel(*i)
  time.sleep(1)

for i in range(0,3):
  type("..." + ip)

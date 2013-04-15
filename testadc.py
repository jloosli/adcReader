#!/usr/bin/python


from Adafruit_ADS1x15 import ADS1x15
import time, math, sqlite3, os, signal,sys
import datetime
from Adafruit_8x8 import EightByEight
import Adafruit_LEDBackpack

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
grid = EightByEight(address=0x70)
led = Adafruit_LEDBackpack.LEDBackpack(0x70)
led.setBrightness = 1

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

display = 0

# ============================================================================
# Example Code
# ============================================================================
ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01  # 16-bit ADC

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ToDo: Change the value below depending on which chip you're using!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ADS_Current = ADS1115

# Initialise the ADC using the default mode (use default I2C address)
adc = ADS1x15(ic=ADS_Current)

theDir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(theDir, 'data/samples.db')
conn = sqlite3.connect(filename)
c = conn.cursor()
# c.execute('SHOW databases')
# print c.fetchall()

c.execute('SELECT max(dataset) FROM samples')
results = c.fetchone()
print results
dataset = results[0] if results[0] is not None else -1
print dataset
dataset += 1
c.execute('SELECT * FROM samples WHERE dataset = ?', (dataset - 1,))
for row in c.fetchall():
  print row
conn.commit()
conn.close()

while 1:
  ch = [0,0,0,0]
  for i in range(0,4):
    result = adc.readADCSingleEnded(i,5000)
    print i, result,
    ch[i]=result
  print ""

  conn = sqlite3.connect(filename)
  c = conn.cursor()
  ts = datetime.datetime.now()
  c.execute("insert into samples(dataset,date,ch0,ch1,ch2,ch3) values (?, ?, ?, ?, ?, ?)", 
      (dataset, ts, ch[0],ch[1],ch[2],ch[3]))
  conn.commit()
  conn.close()


  steps = math.floor(ch[0] / 5000 * 64)
  print "Channels: %.3f, %.3f, %.3f, %.3f V" % (ch[0],ch[1],ch[2],ch[3])
  print "Steps = %d" % (steps)
  grid.clear()
  i=0
  for x in range(0, 8):
    for y in range(0, 8):
      if i < steps:
        grid.setPixel(x, y)
      i += 1

  #time.sleep(1)

#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
GPS Tracking
"""

import sys
import os
import traceback
import argparse
import time
import re
import serial
import sqlite3 as db
import random, datetime

def debug(*vals):
    global args
    if args.verbose:
        print [i for i in vals]

class GPS:
    formats = {
        # Recommended minimum specific GPS/Transit data
        '$GPRMC':('format', 'time', 'validity', 'lat', 'ns', 'lng', 'ew',
                  'speed','course','date','var','ew_checksum'),
        # GPS DOP and active satellites
        '$GPGSA' : ('format','mode','mode_fix','sv0','sv1','sv2','sv3','sv4','sv5','sv6','sv7',
                    'sv8','sv9','sv10','sv11','pdop','hdop','vdop'),
        # Global Positioning System Fix Data
        '$GPGGA' : ('format','time','lat','ns','lng','ew','quality','satellites',
                    'dilution','alt','geo_sep','meters','age','diff_id','checksum')
        # GPS Satellites in view
        #'$GPGSV' : ()
    }

    data={}

    def __init__(self, dev='/dev/ttyUSB0', speed=4800, timeout=1):
        self.input = serial.Serial(dev, speed, timeout=timeout)

    def decode(self,gpsString):
        parts = gpsString.split(',');
        if parts[0] in self.formats.keys():
            return dict(zip(self.formats[parts[0]], parts))
        #raise Exception("Can't find format")
        return None

    def read(self,formatType='$GPRMC', maxTries = 100):
        for i in range(maxTries):
            data=self.input.readline()
            if data: 
                if data.startswith(formatType):
                    decoded=self.decode(data) 
                    self.data[formatType] = decoded
                    if data.startswith('$GPRMC'):
                        debug ("Data is %s" % ("valid" if decoded['validity']=="A" else "not valid"))
                        debug ("Speed is %s " % decoded['speed'])
                        debug (data)
                    return decoded
        return False

    def getLast(self,formatType='$GPRMC'):
        try:
            return self.data[formatType]
        except Exception as e:
            return False



class DataLog:

    def __init__(self):
        thisDir = os.path.dirname(__file__)
        dbname = 'gps.db'
        datapath = os.path.join('data/', dbname)
        print datapath
    
        self.con=db.connect(datapath)
        self.cur = self.con.cursor()
        self.currentSet = None
        self.g=GPS()

    def log(self, vals):
        if not self.currentSet: self.newSet()
        sql = "INSERT INTO gps_datum(dataset_id,gpsstring,speed) values (?,?,?)"
        self.cur.execute(sql, (self.currentSet,vals,self.g.decode(vals)['speed']))
        self.con.commit()

    def newSet(self):
        sql = "INSERT INTO gps_dataset(start) VALUES (?)"
        self.cur.execute(sql, (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
        self.con.commit()
        self.currentSet=self.cur.lastrowid

    def __del__(self):
        self.cur.close()
        self.con.close()

class Display():
    g=GPS()
    l=DataLog()
    def run(self):
        while True:
            data=self.input.readline()
            if data: 
                if data.startswith('$GPRMC'):
                    decoded=self.g.decode(data) 
                    print decoded
                    print ("Data is %s" % ("valid" if decoded['validity']=="A" else "not valid"))
                    print ("Speed is %s " % decoded['speed'])
                    print(data)
                    self.l.log(data)
            # sleep(1)





def main():

    global args
    t=Display()
    t.input= serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
    t.run()


if __name__ == '__main__':
    try:
        start_time = time.time()
        # Parser: See http://docs.python.org/dev/library/argparse.html
        parser = argparse.ArgumentParser(description='GPS Module')
        parser.add_argument(
            '-v', '--verbose', action='store_true',
            default=False, help='verbose output')
        parser.add_argument(
            '-ver', '--version', action='version',
            version='1.0')
        args = parser.parse_args()
        debug(time.asctime())
        main()
        debug(time.asctime())
        debug("Total time in seconds: ", end="")
        debug((time.time() - start_time))
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

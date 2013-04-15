#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Database setup
"""

import sys
import os
import traceback
import argparse
import time
import re
import sqlite3
import random
import datetime
#from pexpect import run, spawn


def debug(*params):
    global args
    if args.verbose:
        print(*params)


class Db:

    def __init__(self, dbpath):
        ''' use path relative to this file '''
        theDir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(theDir, dbpath)
        debug(filename)
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()

    def getDatasets(self):
        self.c.execute("SELECT Distinct dataset from samples ORDER BY dataset")
        for i in self.c.fetchall():
            yield i

    def getSetData(self,dataset):
        self.c.execute("SELECT * FROM samples WHERE dataset = ?", (dataset,))
        return self.c.fetchall()

    def getLatestDataset(self):
        self.c.execute('SELECT max(dataset) FROM samples')
        results = self.c.fetchone()
        if results:
            print(results)
            dataset = results[0] if results[0] is not None else -1
            print(dataset)
            dataset += 1
            print("getLatestDataset: ",dataset)
        return dataset

    def writeToSet(self,dataset,ch0,ch1,ch2,ch3):
        ts = datetime.datetime.now()
        self.c.execute("INSERT INTO samples(dataset,date,ch0,ch1,ch2,ch3) VALUES (?, ?, ?, ?, ?, ?)", 
            (dataset, ts, ch0,ch1,ch2,ch3))

    def create(self):
        self.c.execute('''CREATE TABLE samples 
            (dataset numeric, date text, ch0 real, ch1 real, ch2 real, ch3 real)''')

    def writeDummy(self, records=100):
        ds = self.getLatestDataset()
        print("DS: ")
        print(ds)
        for i in range(records):
            print("Writing: %d to %d" % (i,ds))
            self.writeToSet(ds,random.uniform(0,5),random.uniform(0,5),random.uniform(0,5),random.uniform(0,5))





def main():

    global args
    db = Db('data/samples.db')
    #db.create()
    db.writeDummy()
    #print(db.getSetData(0))


    print("Enter dataset:")

    for i in db.getDatasets():
        print (i[0])
    

if __name__ == '__main__':
    try:
        start_time = time.time()
        # Parser: See http://docs.python.org/dev/library/argparse.html
        parser = argparse.ArgumentParser(description='Database connections')
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_argument('-ver', '--version', action='version', version='1.0')
        args = parser.parse_args()
        if args.verbose:
            print(time.asctime())
        main()
        if args.verbose:
            print(time.asctime())
        if args.verbose:
            print("Total time in minutes: ", end="")
        if args.verbose:
            print((time.time() - start_time) / 60.0)
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

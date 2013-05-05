#!/usr/bin/python
# -*- coding: utf8 -*-

import zipfile
import sqlite3
import tempfile
import csv


class zipData:

    def setFile(self, name):
        self.filename = name

    def setData(self, data):
        self.data = data

    def selfwrite(self):
        print "here"
        print self.filename
        csvfile = tempfile.NamedTemporaryFile()
        writer = csv.writer(csvfile)
        writer.writerows(self.data)
        with zipfile.ZipFile(self.filename, 'w') as theZip:
            theZip.write(csvfile.name)

        csvfile.close()


def main():
    z = zipData()
    z.setData([[0,1,2,3], [4,5,6,7]])
    z.setFile('temp.zip')
    z.selfwrite()

if __name__ == '__main__':
    main()

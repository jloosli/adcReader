#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('data/samples.db')
c = conn.cursor()

# c.execute('DROP TABLE samples')

# c.execute('''CREATE TABLE samples
#              (dataset numeric, date text, ch0 real, ch1 real, ch2 real, ch3 real)''')

# c.execute('INSERT INTO samples(dataset) VALUES (0)')

#c.execute('DELETE FROM samples WHERE 1')
c.execute('SELECT max(dataset) FROM samples')
results = c.fetchone()
print results
print results[0]

c.execute('SELECT * FROM samples')
print c.fetchall()
conn.commit()
conn.close()

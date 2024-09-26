from lib import *
import random

the = o(buckets = 8,
        seed    = 1234567891,
        train   = "../moot/optimize/misc/auto93.csv")

def bins(data):
  for col in data.cols.x:
    for row in data.rows:
      row[col.at] = col.bin(row[col.at], the.buckets)

def headers(data):
  names = data.cols.names[:]
  for col in data.cols.x:
    names[col.at] = names[col.at].lower()
  return names 

cli(the.__dict__)
random.seed(the.seed)
data =  DATA().adds(csv(the.train)).sort()
bins(data)
random.shuffle(data.rows)
[print(','.join([str(x) for x in row])) for row in [headers(data)] + data.rows]

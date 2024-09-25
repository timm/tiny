from lib import *
import random,math

the = o(buckets = 8,
        seed    = 1234567891,
        train   = "../moot/optimize/misc/auto93.csv")

def bins(data):
  for col in data.cols.x:
    if col.this is NUM:
      for row in data.rows:
        row[col.at] = bin(col,row[col.at])

def bin(col,x): 
    return x if x=="?" else int(cdf(col,x) * the.buckets + 0.5)

def cdf(col,x):
  fun = lambda x: 1 - 0.5 * math.exp(-0.717*x - 0.416*x*x) 
  z   = (x - col.mu) / col.sd
  return  fun(x) if z>=0 else 1 - fun(-z) 

random.seed(the.seed)
if __name__ == "__main__": 
  cli(the.__dict__)
  random.seed(the.seed)
  data = adds( DATA(), csv(the.train))
  bins(data)
  #random.shuffle(data.rows)
  [print(','.join([str(x) for x in row])) for row in [data.cols.names] + data.rows]




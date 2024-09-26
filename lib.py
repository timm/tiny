from __future__ import annotations
from typing import List, Dict, Type, Callable, Generator, Iterator
from fileinput import FileInput as file_or_stdin
import random,math,sys,ast,re

#------------------------------------------------
# ## Types
class o:
  def __init__(i,**d): i.__dict__.update(**d)
  def has(i,**d)     : i.__dict__.update(**d)
  def __repr__(i)    : return  i.__class__.__name__ + str(i.__dict__)
  def adds(i,src)    : [i.add(x) for x in src]; return i

number  = float  | int   #
atom    = number | bool | str # and sometimes "?"
row     = list[atom]
rows    = list[row]
classes = dict[str,rows] # `str` is the class name
COL     = 0
NUM     = COL
SYM     = COL
#------------------------------------------------
# ## Classes

class COL(o):
  def add(i:COl,x):
    if x != "?": 
      i.n += 1
      i.add1(x)
    return x

#--------------
class SYM(COL):
  def __init__(i:SYM,at=0,txt=" "):  
     i.has(at=at,txt=txt,n=0,seen={}, most=0, mode=None)

  def add1(i:SYM,x):
    i.seen[x] = 1 + i.seen.get(x,0)
    if i.seen[x] > i.most: i.most, i.mode = i.seen[x], x

  def bin(i:SYM,x,_): return x

  def like(i:SYM, x, prior:float, m:int=2) -> float:
    return (i.seen.get(x,0) + m*prior) / (i.n + m)

#--------------
class NUM(COL):
  def __init__(i,at=0,txt=" "): 
    i.has(at=at,txt=txt,n=0, mu=0, m2=0, sd=0,
            lo=1E32, hi=-1E32, goal = 0 if txt[-1]=="-" else 1)

  def add1(i:NUM,x):
    d     = x - i.mu
    i.mu += d/i.n
    i.m2 += d*(x-i.mu)
    i.sd  = 0 if i.n<2 else (i.m2/(i.n - 1))**.5
    if x < i.lo: i.lo=x
    if x > i.hi: i.hi=x

  def bin(i:NUM,x,buckets): 
    return x if x=="?" else int(cdf(x,i.mu,i.sd) * buckets + 0.5)

  def norm(i:NUM,x):
    return x if x=="?" else (x - i.lo)/(i.hi - i.lo + 1E-32)

#-------------
class COLS(o):
  def __init__(i,names):
    i.has(names=names, all=[], x=[], y=[])
    for at,txt in enumerate(i.names):
      a,z = txt[0], txt[-1]
      col= (NUM if a.isupper() else SYM)(at,txt) 
      i.all += [col]
      if z != "X":
        (i.y if z in "+-!" else i.x).append(col)

#--------------
class DATA(o): 
  def __init__(i): 
    i.has(rows=[], cols=None)

  def add(i:DATA, row):
    "stash the row in DATA, update the summarises of the columns (in i.cols.all)"
    if i.cols: 
      i.rows += [row]
      [col.add(row[col.at]) for col in i.cols.all]
    else:
      i.cols = COLS(row)

  def sort(i):
    i.rows = sorted(i.rows,key=i.yDist)
    return i

  def xDist(i:DATA,row1,row2,p=2:
    d = n = 0
    for col in i.cols.all:
      n += 1
      d += col.dist(row1[col.at], row2[col.at]) ** p
    return (d/n)**(1/p)

  def yDist(i:DAtA,row):
    return max(abs(col.goal - col.norm(row[col.at])) for col in i.cols.y)

#------------------------------------------------
# ## Misc
    
def cdf(x,mu,sd):
  fun = lambda x: 1 - 0.5 * math.exp(-0.717*x - 0.416*x*x) 
  z   = (x - mu) / sd
  return  fun(x) if z>=0 else 1 - fun(-z) 

#------------------------------------------------
# ## Read csv
def cli(d):
  for k,v in d.items():
    v = str(v)
    for c,arg in enumerate(sys.argv):
      after = sys.argv[c+1] if c < len(sys.argv) - 1 else ""
      if arg in ["-"+k[0], "--"+k]:
        d[k] = coerce("False" if v=="True" else ("True" if v=="False" else after))
  return d

def coerce(s):
  try: return ast.literal_eval(s)
  except Exception: return s

def csv(file):
  with file_or_stdin(None if file=="−" else file) as src: 
    for line in src:
      line = re.sub(r"([\n\t\r ]|\#.*)", "", line)
      if line:
        yield [coerce(s.strip()) for s in line.split(",")]

#!/usr/bin/env python3
import sys

#doesnt do anything just gets it ready for reducer 3
# split based on tab
#output taxi id, sqaured deviation, mean, count
for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) < 5:
        continue
    taxi = parts[0]
    sq_dev = parts[2]   # skip the "S"
    mean = parts[3]
    count = parts[4]
    print(f"{taxi}\t{sq_dev}\t{mean}\t{count}")


    #task4 mapper5.py
    #job 3

#!/usr/bin/env python3
import sys

# here we tried to isolate taxi_id and distance
#for each line split based by , if less than 4
for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) < 4:
        # Skips the lines that don’t have enough fields being 4
        # if missing values
        continue
    try:
        taxi_id = fields[1]# labeling fields
        distance = float(fields[3])
        # Key = taxi_id, Value = distance
        print(f"{taxi_id}\t{distance}")
    except ValueError:
        # Ignore rows with non-numeric distance
        continue

    #task 4 mapper1.py
    #job 1


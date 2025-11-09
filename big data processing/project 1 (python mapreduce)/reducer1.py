#!/usr/bin/env python3
import sys

# use our current key made in the mapper and the stats
#used float as said the tutor said in lab
current_key = None
count, maxf, minf, total = 0, float('-inf'), float('inf'), 0.0
#for each line..
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
#split based on tab
    parts = line.split("\t")
    if len(parts) != 5:
        continue
# create attributes for each part and label them
    key = parts[0]
    try:
        c = int(parts[1])
        mx = float(parts[2])
        mn = float(parts[3])
        s = float(parts[4])
    except:
        continue

    if current_key == key:
        # update stats if same key
        count += c
        maxf = max(maxf, mx)
        minf = min(minf, mn)
        total += s
    else:
        # emit result for previous key
        if current_key:
            taxi, trip_type = current_key.split("_")
            avg = total / count if count > 0 else 0
            print('%s\t%s\t%d\t%.2f\t%.2f\t%.2f' % (taxi, trip_type, count, maxf, minf, avg))
        # reset for new key
        current_key = key
        count, maxf, minf, total = c, mx, mn, s

# we print the final output!!!
# we calcuater average total/ count 
#count needs to be bigger than 0
if current_key:
    taxi, trip_type = current_key.split("_")
    avg = total / count if count > 0 else 0
    print('%s\t%s\t%d\t%.2f\t%.2f\t%.2f' % (taxi, trip_type, count, maxf, minf, avg))

    #task1 reducer1.py

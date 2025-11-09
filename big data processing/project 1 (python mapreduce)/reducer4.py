#!/usr/bin/env python3
import sys

#perfrom squsred operation using mean and disatnce
#create attributes and set to null

current_taxi = None
mean = None
count = None

# extra running totals so order doesn't matter (no arrays, just sums)
sum_x = 0.0
sum_x2 = 0.0

def emit(taxi, mean, count, sum_x, sum_x2):
    # output a single aggregated record per taxi for the next job
    if taxi is None or mean is None or count in (None, 0):
        return
    sum_sq = sum_x2 - 2.0 * mean * sum_x + count * (mean * mean)
    # output 
    print(f"{taxi}\tS\t{sum_sq}\t{mean}\t{count}")

#for each line split based on tab
for line in sys.stdin:
    parts = line.strip().split("\t")
    if not parts or len(parts) < 2:
        continue
    taxi = parts[0]

    # If taxi changes, reset stored info
    if current_taxi is not None and taxi != current_taxi:
        emit(current_taxi, mean, count, sum_x, sum_x2)
        current_taxi = taxi
        mean, count = None, None
        sum_x = 0.0
        sum_x2 = 0.0
    elif current_taxi is None:
        current_taxi = taxi

    # handles tags
    if parts[1] == "0":   # mean + count
        try:
            mean = float(parts[2])
            count = int(parts[3])
        except:
            mean, count = None, None
            continue
    elif parts[1] == "1":  # distance
        try:
            dist = float(parts[2])
        except:
            continue
        # accumulate sums regardless of whether mean arrived yet
        sum_x += dist
        sum_x2 += dist * dist

    # keep current_taxi updated
    current_taxi = taxi

# for the last taxi
emit(current_taxi, mean, count, sum_x, sum_x2)


    #task4 reducer4.py
    #job 2

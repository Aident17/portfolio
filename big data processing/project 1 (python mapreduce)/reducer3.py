#!/usr/bin/env python3
import sys

# using mapper 1 we calcate sum of dtances and trip count to get mean
#set attributes to null/ 0
current_taxi = None
sum_dist = 0.0
trip_count = 0
#for each line split based on tab
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        taxi, dist = line.split("\t")
        dist = float(dist)
    except ValueError:
        continue

    # if taxi doesnt eqwual current taxi, output the previous taxi’s result
    #calcate mean
    if taxi != current_taxi and current_taxi is not None:
        mean = sum_dist / trip_count
        # Tag with M and N so mapper4 can identify mean records
        print(f"{current_taxi}\tM\t{mean}\tN\t{trip_count}")
        # Reset for the new taxi
        current_taxi = taxi
        sum_dist = 0.0
        trip_count = 0
#assign values back to the attributes
    current_taxi = taxi
    sum_dist += dist
    trip_count += 1

# for the last taxi
if current_taxi:
    mean = sum_dist / trip_count
    print(f"{current_taxi}\tM\t{mean}\tN\t{trip_count}")



    #task1 reducer3.py
    #job 1

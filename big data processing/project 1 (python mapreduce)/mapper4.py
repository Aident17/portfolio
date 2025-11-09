#!/usr/bin/env python3
import sys

# we get the mean from job 1 and the orginal dtsance
# we then output it for the reducer

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split("\t")

    #if else to split mean and distance recieved first. 
    # Handle tagged mean lines from reducer3: taxi \t M \t mean \t N \t count
    if len(parts) >= 5 and parts[1] == "M":
        try:
            taxi = parts[0]
            mean = float(parts[2])
            count = int(float(parts[4]))  # safe cast if it came as "2.0"
        except ValueError:
            continue
        # tag "0" for mean, as in your style
        print(f"{taxi}\t0\t{mean}\t{count}")
        continue

    # Otherwise treat as a raw trip line from Trips.txt (CSV)
    fields = line.split(",")
    if len(fields) < 4:
        continue
    # simple header guard
    if fields[3].lower() in {"distance", "trip_distance", "dist"}:
        continue
    try:
        taxi = fields[1]
        dist = float(fields[3])
        # tag "1" for distance, as in your style
        print(f"{taxi}\t1\t{dist}")
    except ValueError:
        continue


        #task4 mapper4.py
        #job 2

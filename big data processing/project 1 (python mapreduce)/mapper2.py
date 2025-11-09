#!/usr/bin/env python3
"""mapper2.py"""
__authors__ = "PAM Clustering Implementation"

import sys
from math import sqrt

# function to get initial medoids from initialization.txt
def getMedoids():
    meds = []
    try:
        # try reading from medoids.txt (This is after updated each iteration)
        with open("medoids.txt") as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) == 2:
                    # convert x and y into float and append to list
                    meds.append([float(parts[0]), float(parts[1])])
        return meds
    except FileNotFoundError:
        # first iteration: fall back to initialization.txt (skip v)
        with open("initialization.txt") as fp:
            lines = fp.readlines()[1:]  # skip v
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                # appends x,y coordinates as floats
                meds.append([float(parts[0]), float(parts[1])])
        return meds
# function to assign each point to the closest medoid
def createClusters(medoids):
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        # input file is Trips.txt, split on commas
        cord = line.split(',')  
        # skip header line (Trip#) and any bad rows
        if cord[0] == "Trip#" or len(cord) < 8:
            continue

        try:
            # take dropoff x and y coordinates 
            x = float(cord[6])   # dropoff_x
            y = float(cord[7])   # dropoff_y
        except ValueError:
            # skip rows that cannot be converted
            continue

        # set up minimum distance as infinity
        min_dist = float("inf")
        index = -1
        # calculate distance to each medoid
        for m in medoids:
            cur_dist = sqrt((x - m[0])**2 + (y - m[1])**2)
            # if closer than previous, update min_dist and index
            if cur_dist < min_dist:
                min_dist = cur_dist
                index = medoids.index(m)  
        # emit cluster assignment: medoid_index, x, y
        print(f"{index}\t{x}\t{y}")
# main driver
if __name__ == "__main__":
    medoids = getMedoids() # load medoids from file
    createClusters(medoids) # assign each point to nearest medoid

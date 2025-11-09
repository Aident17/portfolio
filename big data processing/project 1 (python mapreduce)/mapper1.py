#!/usr/bin/env python3
import sys

# we use list to store results to esnure we have in-mapper combining
mylist = []

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("Trip#"):   # skipping the header line
        continue
# split ","
    parts = line.split(",")
    if len(parts) < 4:
        continue
#strip field 1
    taxi = parts[1].strip()
    try:
        fare = float(parts[2].strip())
        distance = float(parts[3].strip())
    except:
        continue

    # classfication algorithm for the trip type usinf if condtiond
    #less than or eual to 200,100 ottherwise short
    if distance >= 200:
        trip_type = "long"
    elif distance >= 100:
        trip_type = "medium"
    else:
        trip_type = "short"

    key = taxi + "_" + trip_type

    #checks if the key already exists in mylist 
    #ensures no repeats
    flag = False
    i = 0
    for x in mylist:
        item = x.split(" ")
        k = item[0]
        count = int(item[1]) 
        maxf = float(item[2]) #use float(decimal for calcuations)
        minf = float(item[3])
        total = float(item[4])

        if key == k:
            # create / update count, max, min, and total
            count = count + 1
            maxf = max(maxf, fare)
            minf = min(minf, fare)
            total = total + fare
            mylist[i] = k + " " + str(count) + " " + str(maxf) + " " + str(minf) + " " + str(total)
            flag = True
            break
        i = i + 1

    # key error handling
    if not flag:
        mylist.append(key + " " + "1" + " " + str(fare) + " " + str(fare) + " " + str(fare))

# printing the results for the reducer
#0-4 for each attribute inthe array
# split on whitespace
for x in mylist:
    item = x.split(" ")
    k = item[0]  # this is the taxi_triptype
    count = item[1]
    maxf = item[2]
    minf = item[3]
    total = item[4]
    print('%s\t%s\t%s\t%s\t%s' % (k, count, maxf, minf, total))


#task1 mapper1.py

#!/usr/bin/env python3
import sys, math

# final reducer: compute sigma from aggregated values
for line in sys.stdin:
    taxi, sq_dev, mu, cnt = line.strip().split("\t")
    try:
        sq_dev = float(sq_dev)
        mu = float(mu)
        cnt = int(cnt)
        if cnt > 0:
            sigma = math.sqrt(sq_dev / cnt)
            print(f"{taxi}\t{mu:.2f}\t{sigma:.2f}")
    except:
        continue

#task4 reducer5.py
#job 3

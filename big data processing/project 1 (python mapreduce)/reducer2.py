#!/usr/bin/env python3

import sys
from math import sqrt

def euclidean_distance(p1, p2):
    """Compute Euclidean distance between two points."""
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def avg_cost(candidate, cluster_points):
    """Compute average distance between candidate medoid and all cluster points."""
    if not cluster_points:
        return float("inf")
    total = sum(euclidean_distance(candidate, q) for q in cluster_points)
    return total / len(cluster_points)

def calculateNewMedoids():
    current_cluster = None
    cluster_points = []

    # New medoids will be stored here
    results = {}

    # Input format: cluster_id \t x \t y
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 3:
            continue

        cluster_id, x, y = parts
        try:
            x, y = float(x), float(y)
        except ValueError:
            continue

        # Group points by cluster id (Hadoop ensures sorted by key)
        if current_cluster is None:
            current_cluster = cluster_id
            cluster_points = [(x, y)]
        elif cluster_id == current_cluster:
            cluster_points.append((x, y))
        else:
            # Process the finished cluster
            best = min(cluster_points, key=lambda p: avg_cost(p, cluster_points))
            results[current_cluster] = best

            # Start a new cluster
            current_cluster = cluster_id
            cluster_points = [(x, y)]

    # Process last cluster
    if cluster_points:
        best = min(cluster_points, key=lambda p: avg_cost(p, cluster_points))
        results[current_cluster] = best

    # Output exactly one medoid per cluster
    for cluster_id in sorted(results.keys(), key=lambda k: int(k)):
        x, y = results[cluster_id]
        print(f"{x}\t{y}")

if __name__ == "__main__":
    calculateNewMedoids()
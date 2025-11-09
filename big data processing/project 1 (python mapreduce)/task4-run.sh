#!/bin/bash

# Removes any existing outputs/ input directory
hdfs dfs -rm -r -f /Output/Task4_step1
hdfs dfs -rm -r -f /Output/Task4_step2
hdfs dfs -rm -r -f /Output/Task4_step3
hdfs dfs -rm -r -f /Output/Task4
hdfs dfs -rm -r -f /Input

# Creates an input directory and then put Trips.txt into it
hdfs dfs -mkdir -p /Input
hdfs dfs -put -f Trips.txt /Input/

# Job 1 this calculates the means for each taxi

hadoop jar hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \
    -input /Input/Trips.txt \
    -output /Output/Task4_step1 \
    -file mapper3.py \
    -mapper mapper3.py \
    -file reducer3.py \
    -reducer reducer3.py

# Job 2 this computes the squared deviations using the means in job 1

hadoop jar hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \
    -input /Input/Trips.txt -input /Output/Task4_step1 \
    -output /Output/Task4_step2 \
    -file mapper4.py \
    -mapper mapper4.py \
    -file reducer4.py \
    -reducer reducer4.py

# Job 3 aggregates/ squares to get the final standadrd deviation

hadoop jar hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \
    -input /Output/Task4_step2 \
    -output /Output/Task4 \
    -file mapper5.py \
    -mapper mapper5.py \
    -file reducer5.py \
    -reducer reducer5.py
